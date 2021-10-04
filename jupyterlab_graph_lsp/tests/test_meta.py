# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.


import jupyterlab_graph_lsp


def test_meta():
    """the version is the same between the frontend pacage and the python package"""
    assert jupyterlab_graph_lsp.__version__ == jupyterlab_graph_lsp.__js__["version"]


def test_labext():
    """we ship exactly one extension"""
    assert len(jupyterlab_graph_lsp._jupyter_labextension_paths()) == 1
