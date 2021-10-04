# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

from jupyter_lsp.specs.utils import PythonModuleSpec

URL = "https://github.com/stardog-union/stardog-language-servers/"


class GRAPHQLLanguageServer(PythonModuleSpec):
    """Supports GRAPHQL language"""

    python_module = "jupyterlab_graph_lsp.servers.graphql"
    key = "stardog-graphql-language-server"
    script = ["dist", "cli.js"]
    languages = ["graphql"]
    args = ["--stdio"]
    spec = dict(
        display_name="graphql-language-server",
        mime_types=["application/graphql"],
        urls=dict(
            home=URL + "tree/master/packages/{}".format(key),
            issues=URL + "issues",
        ),
        install=dict(
            npm="npm install --save-dev {}".format(key),
            yarn="yarn add --dev {}".format(key),
            jlpm="jlpm add --dev {}".format(key),
        ),
    )
