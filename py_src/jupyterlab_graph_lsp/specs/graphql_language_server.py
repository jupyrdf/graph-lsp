# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.

from jupyter_lsp.specs.utils import PythonModuleSpec

URL = "https://github.com/stardog-union/stardog-language-servers"


class GRAPHQLLanguageServer(PythonModuleSpec):
    """Supports GRAPHQL language"""

    python_module = "jupyterlab_graph_lsp.servers.graphql"
    key = "stardog-graphql-language-server"
    script = ["dist", "cli.js"]
    languages = ["graphql", "graphqls"]
    args = ["--stdio"]
    spec = dict(
        display_name="graphql-language-server",
        mime_types=["application/graphql"],
        urls=dict(
            home=f"{URL}/tree/master/packages/{key}",
            issues=f"{URL}/issues",
        ),
        install=dict(
            npm=f"npm install --save-dev {key}",
            yarn=f"yarn add --dev {key}",
            jlpm=f"jlpm add --dev {key}",
        ),
    )
