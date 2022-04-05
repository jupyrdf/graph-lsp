# Copyright (c) 2022 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


from jupyter_lsp.specs.utils import PythonModuleSpec

URL = "https://github.com/stardog-union/stardog-language-servers"


class TurtleLanguageServer(PythonModuleSpec):
    """Supports rdf turtle serialization"""

    python_module = "jupyterlab_graph_lsp.servers.turtle"
    key = "turtle-language-server"
    languages = ["turtle", "ttl"]
    args = ["--stdio"]
    spec = dict(
        display_name=key,
        mime_types=["text/turtle"],
        urls=dict(
            home=f"{URL}/tree/master/packages/{key}",
            issues=f"{URL}/issues",
        ),
    )
