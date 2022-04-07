# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.

from ._version import __js__, __version__

__all__ = ["__version__", "__js__"]


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": __js__["name"]}]
