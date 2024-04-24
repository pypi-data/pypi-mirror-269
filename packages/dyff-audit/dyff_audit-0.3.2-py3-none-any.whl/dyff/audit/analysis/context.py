# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
import os
from pathlib import Path
from typing import Optional

import pyarrow
import ruamel.yaml

from dyff.schema import ids
from dyff.schema.dataset import arrow
from dyff.schema.platform import Analysis


def _analysis_from_yaml(analysis_yaml: dict) -> Analysis:
    if "spec" in analysis_yaml:
        analysis_yaml = analysis_yaml["spec"]
    analysis_yaml["method"]["id"] = ids.null_id()
    analysis_yaml["method"]["account"] = ids.null_id()
    return Analysis.parse_obj(analysis_yaml)


class AnalysisContext:
    """AnalysisContext is Dyff's mechanism for making input data available to user-
    authored analysis Methods.

    When the Method is implemented in a framework such as Jupyter that does not support
    "arguments", the implementation accesses its inputs by instantiating an
    AnalysisContext. The AnalysisContext gets its configuration information from
    environment variables. The runners for analyses implemented in other ways also use
    AnalysisContext under the hood.
    """

    def __init__(
        self,
        *,
        analysis_config_file: Optional[str] = None,
        local_storage_root: Optional[str] = None,
        analysis: Optional[Analysis] = None,
        id: Optional[str] = None,
        allow_override_from_environment: bool = False,
    ):
        """When running an analysis on the Dyff Platform, the platform provides the
        ``analysis_config_file`` and the ``local_storage_root`` arguments via the
        environment variables ``DYFF_AUDIT_ANALYSIS_CONFIG_FILE`` and
        ``DYFF_AUDIT_LOCAL_STORAGE_ROOT``.

        .. note::

            If you are creating an ``AnalysisContext`` instance in code that
            will run on the Dyff Platform, you must call the constructor
            with **no arguments**, e.g., ``ctx = AnalysisContext()``.

        :param analysis_config_file: The path to a YAML-format specification of
        an Analysis. If not specified, it is read from the
        ``DYFF_AUDIT_ANALYSIS_CONFIG_FILE`` environment variable.
        :param local_storage_root: The root directory for local storage of
        entity data. If not specified, it is read from the
        ``DYFF_AUDIT_LOCAL_STORAGE_ROOT`` environment variable.
        :param analysis: You can also specify the analysis as an Analysis
        instance. If you do, you must also specify the ``id``. This is mainly
        useful for debugging.
        :param id: The ID of the analysis, which is needed when instantiating
        from an Analysis instance, because Analysis doesn't have an ``.id``
        field.
        """
        if id is not None and analysis is not None:
            if analysis_config_file is not None:
                raise ValueError(
                    "'(id, analysis)' and 'analysis_config_file' are mutually exclusive"
                )
            self._id = id
            self._analysis = analysis
        else:
            if allow_override_from_environment:
                analysis_config_file = (
                    os.environ.get("DYFF_AUDIT_ANALYSIS_CONFIG_FILE")
                    or analysis_config_file
                )
            else:
                analysis_config_file = analysis_config_file or os.environ.get(
                    "DYFF_AUDIT_ANALYSIS_CONFIG_FILE"
                )
            if analysis_config_file is None:
                raise ValueError(
                    "Must provide '(id, analysis)' or 'analysis_config_file'"
                    " or set DYFF_AUDIT_ANALYSIS_CONFIG_FILE environment variable"
                )
            if id is not None or analysis is not None:
                raise ValueError(
                    "'(id, analysis)' and 'analysis_config_file' are mutually exclusive"
                )

            yaml = ruamel.yaml.YAML()
            with open(analysis_config_file, "r") as fin:
                analysis_yaml = yaml.load(fin)
            self._id = analysis_yaml["spec"]["id"]
            self._analysis = _analysis_from_yaml(analysis_yaml)

        if allow_override_from_environment:
            local_storage_root = (
                os.environ.get("DYFF_AUDIT_LOCAL_STORAGE_ROOT") or local_storage_root
            )
        else:
            local_storage_root = local_storage_root or os.environ.get(
                "DYFF_AUDIT_LOCAL_STORAGE_ROOT"
            )
        if local_storage_root is None:
            raise ValueError(
                "Must provide local_storage_root"
                " or set DYFF_AUDIT_LOCAL_STORAGE_ROOT environment variable."
            )
        self._local_storage_root = Path(local_storage_root)
        if not self._local_storage_root.is_absolute():
            raise ValueError("local_storage_root must be an absolute path")

        self._parameters = {p.keyword: p for p in self.analysis.method.parameters}
        self._arguments = {a.keyword: a.value for a in self.analysis.arguments}
        self._inputs = {i.keyword: i.entity for i in self.analysis.inputs}
        self._input_kinds = {i.keyword: i.kind for i in self.analysis.method.inputs}
        self._input_paths = {
            e.keyword: str(self._local_storage_root / e.entity)
            for e in self.analysis.inputs
        }

    @property
    def analysis(self) -> Analysis:
        return self._analysis

    @property
    def local_storage_root(self) -> Path:
        return self._local_storage_root

    @property
    def output_path(self) -> Path:
        return self._local_storage_root / self._id

    @property
    def arguments(self) -> dict[str, str]:
        return self._arguments.copy()

    @property
    def inputs(self) -> list[str]:
        return list(self._inputs.keys())

    def get_argument(self, keyword: str) -> str:
        return self._arguments[keyword]

    def open_input_dataset(self, keyword: str) -> pyarrow.dataset.Dataset:
        entity = self._inputs[keyword]
        path = self._local_storage_root / entity
        return arrow.open_dataset(str(path))
