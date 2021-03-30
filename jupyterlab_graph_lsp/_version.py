""" single source of truth for jupyterlab-graph-lsp version and metadata
"""

# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

import json
from pathlib import Path

HERE = Path(__file__).parent
__js__ = json.loads((HERE / "labextension/package.json").read_text(encoding="utf-8"))
__version__ = __js__["version"]
