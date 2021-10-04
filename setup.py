# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

import json
from pathlib import Path

HERE = Path(__file__).parent


SRC = Path("jupyterlab_graph_lsp")
EXT_SRC = SRC / "labextension"
PKG = EXT_SRC / "package.json"
INSTALL = SRC / "install.json"

__js__ = json.loads(PKG.read_text(encoding="utf-8"))
__install__ = json.loads(INSTALL.read_text(encoding="utf-8"))

EXT_DEST = Path("share/jupyter/labextensions") / __js__["name"]


DATA_FILES = [(str(EXT_DEST.as_posix()), ["jupyterlab_graph_lsp/install.json"])] + [
    (
        str((EXT_DEST / path.relative_to(EXT_SRC).parent).as_posix()),
        [str(path.as_posix())],
    )
    for path in EXT_SRC.rglob("*")
    if not path.is_dir()
]

setup_args = dict(
    name=__install__["packageName"],
    version=__js__["version"],
    license=__js__["license"],
    description=__js__["description"],
    data_files=DATA_FILES,
)


if __name__ == "__main__":
    import setuptools

    setuptools.setup(
        **setup_args,
        packages=setuptools.find_packages(exclude=["scripts.*", "scripts"])
    )
