# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.


from jupyter_lsp.specs.utils import PythonModuleSpec

REPO = "https://github.com/stardog-union/stardog-language-servers"


class SPARQLLanguageServer(PythonModuleSpec):
    """Supports SPARQL language"""

    python_module = "jupyterlab_graph_lsp.servers.sparql"
    key = "sparql-language-server"
    script = ["dist", "cli.js"]
    languages = ["sparql", "sparul", "sparql-query", "sparql-update"]
    args = ["--stdio"]
    spec = dict(
        display_name=key,
        mime_types=["application/sparql-query", "application/sparql-update"],
        urls=dict(
            home=f"{REPO}/tree/master/packages/{key}",
            issues=f"{REPO}/issues",
        ),
        install=dict(
            npm=f"npm install --save-dev {key}",
            yarn=f"yarn add --dev {key}",
            jlpm=f"jlpm add --dev {key}",
        ),
    )
