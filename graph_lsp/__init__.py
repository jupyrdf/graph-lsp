# flake8: noqa: F401
from ._version import __version__

__all__ = [
    "__version__",
]


def _jupyter_labextension_paths():
    return [
        {
            "src": "labextensions/@krassowski/jupyterlab-lsp",
            "dest": "@krassowski/jupyterlab-lsp",
        }
    ]
