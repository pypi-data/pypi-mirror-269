# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
from pathlib import Path
from typing import Any

import pydantic
import pytest

from dyff.audit.local.platform import DyffLocalPlatform
from dyff.schema import ids
from dyff.schema.base import int32
from dyff.schema.dataset import ReplicatedItem, arrow
from dyff.schema.platform import *
from dyff.schema.requests import *


class BlurstCountScoredItem(ReplicatedItem):
    blurstCount: int32() = pydantic.Field(  # type: ignore
        description="Number of times the word 'blurst' is used in the response."
    )
    cromulent: int32() = pydantic.Field(  # type: ignore
        description="Whether the text is cromulent."
    )
    embiggen: str = pydantic.Field(description="Which man to embiggen.")


DATA_DIR = Path(__file__).parent.resolve() / "data"


@pytest.fixture(scope="session")
def local_platform(pytestconfig, tmp_path_factory):
    """Creates a DyffLocalPlatform that is shared by all tests.

    This is needed because a workflow's dependencies must be present before we can test
    the workflow.
    """
    storage_root = pytestconfig.getoption("storage_root")
    if storage_root is not None:
        storage_root_path = Path(storage_root).resolve()
        yield DyffLocalPlatform(storage_root_path)
    else:
        yield DyffLocalPlatform(tmp_path_factory.mktemp("dyff"))


@pytest.fixture(scope="session")
def ctx():
    """Shared dict for storing the workflow dependencies that we add incrementally as
    testing progresses."""
    d: dict[str, Any] = {
        "account": ids.generate_entity_id(),
        "inference_service": ids.generate_entity_id(),
        "model": ids.generate_entity_id(),
    }
    yield d


@pytest.mark.datafiles(DATA_DIR)
def test_datasets_create(local_platform: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    dataset_dir = datafiles / "dataset"
    dataset = local_platform.datasets.create_arrow_dataset(
        dataset_dir, account=account, name="dataset"
    )
    local_platform.datasets.upload_arrow_dataset(dataset, dataset_dir)
    ctx["dataset"] = dataset


@pytest.mark.datafiles(DATA_DIR)
def test_evaluations_import_data(local_platform: DyffLocalPlatform, ctx, datafiles):
    account = ctx["account"]
    dataset = ctx["dataset"]

    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(inferenceService=""),
    )
    evaluation = local_platform.evaluations.import_data(
        datafiles / "evaluation", evaluation_request=evaluation_request
    )
    ctx["evaluation"] = evaluation


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_jupyter_notebook(
    local_platform: DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    module_jupyter_notebook_dir = datafiles / "module_jupyter_notebook"
    module_jupyter_notebook = local_platform.modules.create_package(
        module_jupyter_notebook_dir, account=account, name="module_jupyter_notebook"
    )
    local_platform.modules.upload_package(
        module_jupyter_notebook, module_jupyter_notebook_dir
    )
    ctx["module_jupyter_notebook"] = module_jupyter_notebook


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_function(
    local_platform: DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    module_python_function_dir = datafiles / "module_python_function"
    module_python_function = local_platform.modules.create_package(
        module_python_function_dir, account=account, name="module_python_function"
    )
    local_platform.modules.upload_package(
        module_python_function, module_python_function_dir
    )
    ctx["module_python_function"] = module_python_function


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_rubric(
    local_platform: DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    module_python_rubric_dir = datafiles / "module_python_rubric"
    module_python_rubric = local_platform.modules.create_package(
        module_python_rubric_dir, account=account, name="module_python_rubric"
    )
    local_platform.modules.upload_package(
        module_python_rubric, module_python_rubric_dir
    )
    ctx["module_python_rubric"] = module_python_rubric


@pytest.mark.depends(
    on=[
        "test_modules_create_jupyter_notebook",
    ]
)
def test_methods_create_jupyter_notebook(local_platform: DyffLocalPlatform, ctx):
    account = ctx["account"]
    module_jupyter_notebook = ctx["module_jupyter_notebook"]
    method_jupyter_notebook_request = MethodCreateRequest(
        name="method_notebook",
        scope=MethodScope.InferenceService,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.JupyterNotebook,
            jupyterNotebook=MethodImplementationJupyterNotebook(
                notebookModule=module_jupyter_notebook.id,
                notebookPath="test-notebook.ipynb",
            ),
        ),
        parameters=[MethodParameter(keyword="trueName", description="His real name")],
        inputs=[
            MethodInput(kind=MethodInputKind.Measurement, keyword="cromulence"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.SafetyCase,
            safetyCase=SafetyCaseSpec(
                name="safetycase_notebook",
                description="""# Markdown Description""",
            ),
        ),
        modules=[module_jupyter_notebook.id],
        account=account,
    )
    method_jupyter_notebook = local_platform.methods.create(
        method_jupyter_notebook_request
    )
    ctx["method_jupyter_notebook"] = method_jupyter_notebook


@pytest.mark.depends(
    on=[
        "test_modules_create_python_function",
    ]
)
def test_methods_create_python_function(local_platform: DyffLocalPlatform, ctx):
    account = ctx["account"]
    module_python_function = ctx["module_python_function"]
    method_python_function_request = MethodCreateRequest(
        account=account,
        modules=[module_python_function.id],
        name="method_python_function",
        scope=MethodScope.Evaluation,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.PythonFunction,
            pythonFunction=MethodImplementationPythonFunction(
                fullyQualifiedName="dyff.fake.method.blurst_count",
            ),
        ),
        parameters=[
            MethodParameter(keyword="embiggen", description="Who is being embiggened")
        ],
        inputs=[
            MethodInput(kind=MethodInputKind.Dataset, keyword="dataset"),
            MethodInput(kind=MethodInputKind.Evaluation, keyword="outputs"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.Measurement,
            measurement=MeasurementSpec(
                name="example.dyff.io/blurst-count",
                description="The number of times the word 'blurst' appears in the text.",
                level=MeasurementLevel.Instance,
                schema=DataSchema(
                    arrowSchema=arrow.encode_schema(
                        arrow.arrow_schema(BlurstCountScoredItem)
                    )
                ),
            ),
        ),
    )
    method_python_function = local_platform.methods.create(
        method_python_function_request
    )
    ctx["method_python_function"] = method_python_function


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_import_data",
        "test_methods_create_python_function",
    ]
)
def test_measurements_create_python_function(local_platform: DyffLocalPlatform, ctx):
    account = ctx["account"]
    evaluation = ctx["evaluation"]
    inference_service = ctx["inference_service"]
    model = ctx["model"]
    dataset = ctx["dataset"]
    method_python_function = ctx["method_python_function"]
    measurement_python_function_request = AnalysisCreateRequest(
        account=account,
        method=method_python_function.id,
        scope=AnalysisScope(
            evaluation=evaluation.id,
            dataset=dataset.id,
            inferenceService=inference_service,
            model=model,
        ),
        arguments=[
            AnalysisArgument(keyword="embiggen", value="smallest"),
        ],
        inputs=[
            AnalysisInput(keyword="dataset", entity=dataset.id),
            AnalysisInput(keyword="outputs", entity=evaluation.id),
        ],
    )
    measurement_python_function = local_platform.measurements.create(
        measurement_python_function_request
    )
    print(f"measurement_python_function.id: {measurement_python_function.id}")
    ctx["measurement_python_function"] = measurement_python_function


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_import_data",
        "test_modules_create_python_rubric",
    ]
)
def test_reports_create(local_platform: DyffLocalPlatform, ctx):
    account = ctx["account"]
    evaluation = ctx["evaluation"]
    module = ctx["module_python_rubric"]
    report_request = ReportCreateRequest(
        account=account,
        rubric="dyff.fake.rubric.BlurstCount",
        evaluation=evaluation.id,
        modules=[module.id],
    )
    report = local_platform.reports.create(report_request)
    print(f"report.id: {report.id}")
    ctx["report"] = report


@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook",
        "test_measurements_create_python_function",
    ]
)
def test_safetycase(local_platform: DyffLocalPlatform, ctx):
    account = ctx["account"]
    inference_service = ctx["inference_service"]
    model = ctx["model"]
    method_jupyter_notebook = ctx["method_jupyter_notebook"]
    measurement_python_function = ctx["measurement_python_function"]

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inference_service,
            model=model,
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
        ],
        inputs=[
            AnalysisInput(keyword="cromulence", entity=measurement_python_function.id),
        ],
    )
    safetycase_jupyter_notebook = local_platform.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(f"safetycase_jupyter_notebook.id: {safetycase_jupyter_notebook.id}")
    ctx["safetycase_jupyter_notebook"] = safetycase_jupyter_notebook
