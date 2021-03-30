# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


import jupyterlab_graph_lsp


def test_meta():
    assert jupyterlab_graph_lsp.__version__ == jupyterlab_graph_lsp.__js__["version"]
