# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional, TypeVar

import pyarrow
import ruamel.yaml

from dyff.client import Client
from dyff.schema import ids
from dyff.schema.dataset import arrow, binary
from dyff.schema.platform import (
    Analysis,
    Artifact,
    DataSchema,
    Dataset,
    Digest,
    EntityStatus,
    Evaluation,
    ForeignInferenceService,
    ForeignMethod,
    InferenceInterface,
    InferenceSessionSpec,
    Measurement,
    Method,
    MethodInputKind,
    Module,
    Report,
    SafetyCase,
)
from dyff.schema.requests import (
    AnalysisCreateRequest,
    DatasetCreateRequest,
    EvaluationCreateRequest,
    MethodCreateRequest,
    ModuleCreateRequest,
    ReportCreateRequest,
)

from ..analysis import run_analysis, run_report
from ..workflows import local_evaluation

T = TypeVar("T")


def _once(x: T) -> Iterable[T]:
    yield x


class _Datasets:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, dataset_request: DatasetCreateRequest) -> Dataset:
        id = ids.generate_entity_id()
        dataset_dict = dataset_request.dict()
        dataset_dict["id"] = id
        dataset_dict["account"] = self._platform.account
        dataset_dict["status"] = EntityStatus.ready
        dataset_dict["creationTime"] = datetime.now()
        dataset = Dataset.parse_obj(dataset_dict)

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".dataset.json", "w") as fout:
            fout.write(dataset.json())
        return dataset

    def get(self, id: str) -> Dataset:
        file = self._platform.entity_path(id) / ".dataset.json"
        return Dataset.parse_file(file)

    def create_arrow_dataset(
        self, dataset_directory: str, *, account: str, name: str
    ) -> Dataset:
        """Create a Dataset resource describing an existing Arrow dataset.

        Internally, constructs a ``DatasetCreateRequest`` using information
        obtained from the Arrow dataset, then calls ``create()`` with the
        constructed request.

        Typical usage::

            dataset = client.datasets.create_arrow_dataset(dataset_directory, ...)
            client.datasets.upload_arrow_dataset(dataset, dataset_directory)

        :param dataset_directory: The root directory of the Arrow dataset.
        :type dataset_directory: str
        :keyword account: The account that will own the Dataset resource.
        :type account: str
        :keyword name: The name of the Dataset resource.
        :type name: str
        :returns: The complete Dataset resource.
        :rtype: Dataset
        """
        dataset_path = Path(dataset_directory)
        ds = arrow.open_dataset(str(dataset_path))
        file_paths = list(ds.files)
        artifact_paths = [
            str(Path(file_path).relative_to(dataset_path)) for file_path in file_paths
        ]
        artifacts = [
            Artifact(
                kind="parquet",
                path=artifact_path,
                digest=Digest(
                    md5=binary.encode(binary.file_digest("md5", file_path)),
                ),
            )
            for file_path, artifact_path in zip(file_paths, artifact_paths)
        ]
        schema = DataSchema(
            arrowSchema=arrow.encode_schema(ds.schema),
        )
        request = DatasetCreateRequest(
            account=account,
            name=name,
            artifacts=artifacts,
            schema=schema,
        )
        return self.create(request)

    def upload_arrow_dataset(self, dataset: Dataset, dataset_directory: str) -> None:
        """Uploads the data files in an existing Arrow dataset for which a Dataset
        resource has already been created.

        Typical usage::

            dataset = client.datasets.create_arrow_dataset(dataset_directory, ...)
            client.datasets.upload_arrow_dataset(dataset, dataset_directory)

        :param dataset: The Dataset resource for the Arrow dataset.
        :type dataset: Dataset
        :param dataset_directory: The root directory of the Arrow dataset.
        :type dataset_directory: str
        """
        if any(artifact.digest.md5 is None for artifact in dataset.artifacts):
            raise ValueError("artifact.digest.md5 must be set for all artifacts")
        for artifact in dataset.artifacts:
            assert artifact.digest.md5 is not None
            file_path = Path(dataset_directory) / artifact.path
            cache_path = self._platform.storage_root / dataset.id / artifact.path
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as fin:
                with open(cache_path, "wb") as fout:
                    fout.write(fin.read())


class _Evaluations:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def import_data(
        self,
        dataset_directory: Path | str,
        *,
        id: Optional[str] = None,
        evaluation_request: Optional[EvaluationCreateRequest] = None,
    ) -> Evaluation:
        """Imports existing data into the local cache under a newly-generated ID. Useful
        when you already have evaluation data and you want to make it available to other
        workflows using the local platform.

        :param dataset_directory: The root directory of the Arrow dataset.
        :type dataset_directory: str
        :returns: The ID of the imported data in the local platform.
        :rtype: str
        """
        dataset_path = Path(dataset_directory)
        ds = arrow.open_dataset(str(dataset_path))
        file_paths = list(ds.files)

        replications = set()
        for row in ds.to_table().to_pylist():
            replications.add(row["_replication_"])

        evaluation_dict: dict[str, Any] = {}
        evaluation_dict["id"] = id or ids.generate_entity_id()
        evaluation_dict["account"] = (
            evaluation_request and evaluation_request.account
        ) or ids.null_id()
        evaluation_dict["dataset"] = (
            evaluation_request and evaluation_request.dataset
        ) or ids.null_id()
        evaluation_dict["replications"] = len(replications)

        service_id = (
            evaluation_request and evaluation_request.inferenceSession.inferenceService
        ) or ids.null_id()
        session_spec = InferenceSessionSpec(
            inferenceService=ForeignInferenceService(
                id=service_id,
                name="",
                account=ids.null_id(),
                interface=InferenceInterface(
                    endpoint="",
                    outputSchema=DataSchema(arrowSchema=arrow.encode_schema(ds.schema)),
                ),
            )
        )
        evaluation_dict["inferenceSession"] = session_spec.dict()
        evaluation = Evaluation.parse_obj(evaluation_dict)

        cache_dir = self._platform.entity_path(evaluation.id)
        cache_dir.mkdir()
        with open(cache_dir / ".evaluation.json", "w") as fout:
            fout.write(evaluation.json())

        artifact_paths = [
            str(Path(file_path).relative_to(dataset_path)) for file_path in file_paths
        ]
        artifacts = [
            Artifact(
                kind="parquet",
                path=artifact_path,
                digest=Digest(
                    md5=binary.encode(binary.file_digest("md5", file_path)),
                ),
            )
            for file_path, artifact_path in zip(file_paths, artifact_paths)
        ]
        for artifact in artifacts:
            assert artifact.digest.md5 is not None
            file_path = Path(dataset_directory) / artifact.path
            cache_path = self._platform.entity_path(evaluation.id) / artifact.path
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as fin:
                with open(cache_path, "wb") as fout:
                    fout.write(fin.read())
        return evaluation

    def local_evaluation(self, *, dataset: str, inferencesession: str) -> str:
        client = self._platform._require_client()
        session = client.inferencesessions.get(inferencesession)
        id = ids.generate_entity_id()
        return local_evaluation(
            client,
            session,
            input_dataset_path=self._platform.entity_path(dataset),
            # workflows.local_evaluation() creates an /id subdirectory for the output
            output_dataset_path=self._platform.storage_root,
            id=id,
        )

    def get(self, id: str) -> Evaluation:
        file = self._platform.entity_path(id) / ".evaluation.json"
        return Evaluation.parse_file(file)


class _Measurements:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, analysis_request: AnalysisCreateRequest) -> Measurement:
        id = ids.generate_entity_id()

        method_id = analysis_request.method
        method = self._platform.methods.get(method_id)

        # Create an entity representing the output of the Analysis
        measurement_spec = method.output.measurement
        if measurement_spec is None:
            raise ValueError("Method spec violates constraints")

        measurement = Measurement(
            account=analysis_request.account,
            id=id,
            creationTime=datetime.now(),
            status=EntityStatus.complete,
            scope=analysis_request.scope,
            method=ForeignMethod.parse_obj(method.dict()),
            arguments=analysis_request.arguments,
            inputs=analysis_request.inputs,
            **measurement_spec.dict(),
        )

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".measurement.json", "w") as fout:
            fout.write(measurement.json())

        analysis = Analysis.parse_obj(measurement.dict())
        # This fixes some things that YAML can't parse (like Enums)
        analysis_dict = json.loads(analysis.json())
        analysis_dict["id"] = id
        # Code expects a full k8s manifest
        # TODO: Should only pass the 'spec' part in the first place from
        # dyff-operator, but that requires figuring out how to manipulate YAML in Go
        analysis_dict = {"spec": analysis_dict}
        config_file = cache_dir / ".analysis.yaml"
        yaml = ruamel.yaml.YAML()
        with open(config_file, "w") as fout:
            yaml.dump(analysis_dict, fout)

        run_analysis(
            method,
            storage_root=self._platform.storage_root,
            config_file=config_file,
        )

        return measurement

    def get(self, id: str) -> Measurement:
        file = self._platform.entity_path(id) / ".measurement.json"
        return Measurement.parse_file(file)


class _Methods:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, method_request: MethodCreateRequest) -> Method:
        id = ids.generate_entity_id()
        method_dict = method_request.dict()
        method_dict["id"] = id
        method_dict["account"] = self._platform.account
        method_dict["status"] = EntityStatus.ready
        method_dict["creationTime"] = datetime.now()
        method = Method.parse_obj(method_dict)

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".method.json", "w") as fout:
            fout.write(method.json())
        return method

    def get(self, id: str) -> Method:
        file = self._platform.entity_path(id) / ".method.json"
        return Method.parse_file(file)


class _Modules:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, module_request: ModuleCreateRequest) -> Module:
        id = ids.generate_entity_id()
        module_dict = module_request.dict()
        module_dict["id"] = id
        module_dict["account"] = self._platform.account
        module_dict["status"] = EntityStatus.ready
        module_dict["creationTime"] = datetime.now()
        module = Module.parse_obj(module_dict)

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".module.json", "w") as fout:
            fout.write(module.json())
        return module

    def get(self, id: str) -> Module:
        file = self._platform.entity_path(id) / ".module.json"
        return Module.parse_file(file)

    def create_package(
        self, package_directory: str, *, account: str, name: str
    ) -> Module:
        """Create a Module resource describing a package structured as a directory tree.

        Internally, constructs a ``ModuleCreateRequest`` using information
        obtained from the directory tree, then calls ``create()`` with the
        constructed request.

        Typical usage::

            module = client.modules.create_package(package_directory, ...)
            client.modules.upload_package(module, package_directory)

        :param package_directory: The root directory of the package.
        :type package_directory: str
        :keyword account: The account that will own the Module resource.
        :type account: str
        :keyword name: The name of the Module resource.
        :type name: str
        :returns: The complete Module resource.
        :rtype: Module
        """
        package_root = Path(package_directory)
        file_paths = [path for path in package_root.rglob("*") if path.is_file()]
        if not file_paths:
            raise ValueError(f"package_directory is empty: {package_directory}")
        artifact_paths = [
            str(Path(file_path).relative_to(package_root)) for file_path in file_paths
        ]
        artifacts = [
            Artifact(
                # FIXME: Is this a useful thing to do? It's redundant with
                # information in 'path'. Maybe it should just be 'code' or
                # something generic.
                kind="".join(file_path.suffixes),
                path=artifact_path,
                digest=Digest(
                    md5=binary.encode(binary.file_digest("md5", str(file_path))),
                ),
            )
            for file_path, artifact_path in zip(file_paths, artifact_paths)
        ]
        request = ModuleCreateRequest(
            account=account,
            name=name,
            artifacts=artifacts,
        )
        return self.create(request)

    def upload_package(self, module: Module, package_directory: str) -> None:
        """Uploads the files in a package directory for which a Module resource has
        already been created.

        Typical usage::

            module = client.modules.create_package(package_directory, ...)
            client.modules.upload_package(module, package_directory)

        :param module: The Module resource for the package.
        :type module: Module
        :param package_directory: The root directory of the package.
        :type package_directory: str
        """
        if any(artifact.digest.md5 is None for artifact in module.artifacts):
            raise ValueError("artifact.digest.md5 must be set for all artifacts")
        for artifact in module.artifacts:
            assert artifact.digest.md5 is not None
            file_path = Path(package_directory) / artifact.path
            cache_path = self._platform.storage_root / module.id / artifact.path
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as fin:
                with open(cache_path, "wb") as fout:
                    fout.write(fin.read())


class _Reports:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, report_request: ReportCreateRequest) -> Report:
        id = ids.generate_entity_id()
        report_dict = report_request.dict()
        report_dict["id"] = id
        report_dict["account"] = self._platform.account
        report_dict["status"] = EntityStatus.ready
        report_dict["creationTime"] = datetime.now()

        evaluation = self._platform.evaluations.get(report_request.evaluation)
        report_dict["dataset"] = evaluation.dataset
        report_dict["inferenceService"] = (
            evaluation.inferenceSession.inferenceService.id
        )

        report = Report.parse_obj(report_dict)

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".report.json", "w") as fout:
            fout.write(report.json())

        run_report(report, storage_root=self._platform.storage_root)

        return report

    def get(self, id: str) -> Module:
        file = self._platform.entity_path(id) / ".module.json"
        return Module.parse_file(file)


class _SafetyCases:
    def __init__(self, platform: DyffLocalPlatform):
        self._platform = platform

    def create(self, analysis_request: AnalysisCreateRequest) -> SafetyCase:
        id = ids.generate_entity_id()

        method_id = analysis_request.method
        method = self._platform.methods.get(method_id)

        # Create an entity representing the output of the Analysis
        safetycase_spec = method.output.safetyCase
        if safetycase_spec is None:
            raise ValueError("Method spec violates constraints")

        safetycase = SafetyCase(
            account=analysis_request.account,
            id=id,
            creationTime=datetime.now(),
            status=EntityStatus.complete,
            scope=analysis_request.scope,
            method=ForeignMethod.parse_obj(method.dict()),
            arguments=analysis_request.arguments,
            inputs=analysis_request.inputs,
            # This covers: .name, .description
            **safetycase_spec.dict(),
        )

        cache_dir = self._platform.entity_path(id)
        cache_dir.mkdir()
        with open(cache_dir / ".safetycase.json", "w") as fout:
            fout.write(safetycase.json())

        analysis = Analysis.parse_obj(safetycase.dict())
        # This fixes some things that YAML can't parse (like Enums)
        analysis_dict = json.loads(analysis.json())
        analysis_dict["id"] = id
        # Code expects a full k8s manifest
        # TODO: Should only pass the 'spec' part in the first place from
        # dyff-operator, but that requires figuring out how to manipulate YAML in Go
        analysis_dict = {"spec": analysis_dict}
        config_file = cache_dir / ".analysis.yaml"
        yaml = ruamel.yaml.YAML()
        with open(config_file, "w") as fout:
            yaml.dump(analysis_dict, fout)

        run_analysis(
            method,
            storage_root=self._platform.storage_root,
            config_file=config_file,
        )

        return safetycase

    def get(self, id: str) -> SafetyCase:
        file = self._platform.entity_path(id) / ".safetycase.json"
        return SafetyCase.parse_file(file)


class DyffLocalPlatform:
    """Emulates a subset of Dyff Platform operations locally.

    This class is intended to aid in local development and debugging of code
    and data that will run on the Dyff Platform. The inferface mirrors that of
    ``dyff.client.Client`` and should have similar behavior.

    Entities created on the local platform are stored in a local cache. You can
    optionally provide a ``dyff.client.Client`` instance, in which case "read"
    calls like ``get`` and ``data`` will forward to a remote Dyff Platform
    instance if the requested entity is not available locally. API calls that
    modify the platform state are **never** forwarded to a remote instance.
    """

    def __init__(
        self,
        storage_root: Path,
        *,
        remote_client: Optional[Client] = None,
    ):
        self._storage_root = storage_root
        self._client = remote_client

        self._datasets = _Datasets(self)
        self._evaluations = _Evaluations(self)
        self._measurements = _Measurements(self)
        self._methods = _Methods(self)
        self._modules = _Modules(self)
        self._reports = _Reports(self)
        self._safetycases = _SafetyCases(self)

        self._storage_root.mkdir(exist_ok=True)

    def _require_client(self) -> Client:
        if not self._client:
            raise ValueError("remote client not available")
        return self._client

    @property
    def remote(self) -> Client | None:
        return self._client

    @property
    def datasets(self) -> _Datasets:
        return self._datasets

    @property
    def evaluations(self) -> _Evaluations:
        return self._evaluations

    @property
    def measurements(self) -> _Measurements:
        return self._measurements

    @property
    def methods(self) -> _Methods:
        return self._methods

    @property
    def modules(self) -> _Modules:
        return self._modules

    @property
    def reports(self) -> _Reports:
        return self._reports

    @property
    def safetycases(self) -> _SafetyCases:
        return self._safetycases

    @property
    def storage_root(self) -> Path:
        return self._storage_root

    @property
    def account(self) -> str:
        return "local"

    def entity_path(self, id: str) -> Path:
        """Returns the path to the local directory that stores information about the
        entity with the given ID."""
        return self.storage_root / id

    def link_entity(self, package: Path, id: Optional[str] = None) -> str:
        """Creates a symlink in the local storage tree pointing to a directory on the
        file system. You can either provide an ID or let the platform generate one.
        Returns the assigned ID.

        This can be used to create an "editable" package so that you can refer to the
        package at a stable ID while still changing the contents of the files in it.

        :param package: The path to the directory to symlink to.
        :param id: If provided, becomes the ID of the linked package in the platform.
            Otherwise, a new ID is generated.
        :return: The ID of the linked entity.
        """
        package = package.resolve()
        id = id or ids.generate_entity_id()
        cache_path = self.storage_root / id
        if not cache_path.exists():
            cache_path.symlink_to(package)
        elif cache_path.is_symlink():
            target = cache_path.resolve()
            if target != package:
                raise ValueError(f"{id} -> {target}: conflict")
        else:
            raise ValueError(f"{cache_path} exists and is not a symlink")
        return id

    def _download_data(self, kind: MethodInputKind, id: str, path: Path):
        assert self._client is not None
        if kind == MethodInputKind.Dataset:
            dataset = self._client.datasets.get(id)
            dataset_data = self._client.datasets.data(dataset)
            arrow.write_dataset(
                dataset_data.to_batches(),
                output_path=str(path),
                feature_schema=dataset_data.dataset_schema,
                existing_data_behavior="error",
            )
        elif kind == MethodInputKind.Evaluation:
            raise NotImplementedError()
        elif kind == MethodInputKind.Measurement:
            raise NotImplementedError()
        elif kind == MethodInputKind.Report:
            report = self._client.reports.get(id)
            report_data = self._client.reports.data(report)
            record_batch = pyarrow.RecordBatch.from_pandas(report_data)
            arrow.write_dataset(
                _once(record_batch),
                output_path=str(path),
                feature_schema=record_batch.schema,
                existing_data_behavior="error",
            )
        else:
            raise ValueError(f"MethodInputKind {kind}")
