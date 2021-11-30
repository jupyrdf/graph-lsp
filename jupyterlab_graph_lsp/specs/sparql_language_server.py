# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


from jupyter_lsp.specs.utils import PythonModuleSpec

REPO = (
    "https://github.com/stardog-union/stardog-language-servers/tree/master/packages/{}"
)


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
            home=REPO.format(key),
            issues="https://github.com/stardog-union/stardog-language-servers/issues",
        ),
        install=dict(
            npm="npm install --save-dev {}".format(key),
            yarn="yarn add --dev {}".format(key),
            jlpm="jlpm add --dev {}".format(key),
        ),
    )
