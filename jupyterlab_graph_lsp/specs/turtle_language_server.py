# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


from jupyter_lsp.specs.utils import NodeModuleSpec

URL = "https://github.com/stardog-union/stardog-language-servers/"


class TurtleLanguageServer(NodeModuleSpec):
    """Supports rdf turtle serialization"""

    node_module = key = "turtle-language-server"
    script = ["dist", "cli.js"]
    languages = ["turtle"]
    args = ["--stdio"]
    spec = dict(
        display_name=key,
        mime_types=["text/turtle"],
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
