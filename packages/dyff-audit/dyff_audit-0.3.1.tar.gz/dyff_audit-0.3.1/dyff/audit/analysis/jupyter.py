# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0


import nbconvert
import nbformat

from dyff.audit.analysis.context import AnalysisContext
from dyff.schema.platform import MethodImplementationKind, MethodOutputKind


def run_jupyter_notebook() -> None:
    ctx = AnalysisContext()

    implementation = ctx.analysis.method.implementation
    if (
        implementation.kind != MethodImplementationKind.JupyterNotebook
        or implementation.jupyterNotebook is None
    ):
        raise ValueError("expected method.implementation as JupyterNotebook")
    output = ctx.analysis.method.output
    if output.kind != MethodOutputKind.SafetyCase or output.safetyCase is None:
        raise ValueError("expected method.output as SafetyCase")

    notebook_path = (
        ctx.local_storage_root
        / implementation.jupyterNotebook.notebookModule
        / implementation.jupyterNotebook.notebookPath
    )
    with open(str(notebook_path), "r") as fin:
        notebook = nbformat.read(fin, as_version=4)

    resources: dict = {}
    clear_output_preprocessor = nbconvert.preprocessors.ClearOutputPreprocessor()
    notebook, resources = clear_output_preprocessor.preprocess(notebook, resources)

    execute_preprocessor = nbconvert.preprocessors.ExecutePreprocessor()
    notebook, resources = execute_preprocessor.preprocess(notebook, resources)

    html_exporter = nbconvert.HTMLExporter(exclude_input=True)
    html_body, resources = html_exporter.from_notebook_node(notebook, resources)

    ctx.output_path.mkdir(parents=True, exist_ok=True)
    with open(ctx.output_path / "index.html", "w") as fout:
        fout.write(html_body)
