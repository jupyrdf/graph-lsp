import re
import sys
from pathlib import Path

import setuptools

setuptools.setup(
    version=re.findall(
        r"""__version__ = "([^"]+)"$""",
        (Path(__file__).parent / "graph_lsp" / "_version.py").read_text(
            encoding="utf-8"
        ),
    )[0],
    setup_requires=["pytest-runner"] if "test" in sys.argv else [],
)
