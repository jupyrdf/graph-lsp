""" important project paths

    this should not import anything not in py37+ stdlib, or any local paths
"""

# Copyright (c) 2022 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

import configparser
import json
import os
import platform
import re
import shutil
from pathlib import Path

PY_PKG = "jupyterlab_graph_lsp"

# platform
PLATFORM = os.environ.get("FAKE_PLATFORM", platform.system())
WIN = PLATFORM == "Windows"
OSX = PLATFORM == "Darwin"
LINUX = PLATFORM == "Linux"
UNIX = not WIN

CI = bool(json.loads(os.environ.get("CI", "false")))
WIN_CI = bool(json.loads(os.environ.get("WIN_CI", "false")))
TESTING_IN_CI = bool(json.loads(os.environ.get("TESTING_IN_CI", "false")))

# CI jank
SKIP_CONDA_PREFLIGHT = bool(json.loads(os.environ.get("SKIP_CONDA_PREFLIGHT", "false")))
FORCE_SERIAL_ENV_PREP = bool(
    json.loads(os.environ.get("FORCE_SERIAL_ENV_PREP", "true"))
)
# one of: None, wheel or sdist
INSTALL_ARTIFACT = os.environ.get("INSTALL_ARTIFACT")
UTEST_PROCESSES = os.environ.get(
    "UTEST_PROCESSES", os.environ.get("ATEST_PROCESSES", "")
)

# find root
SCRIPTS = Path(__file__).parent.resolve()
ROOT = SCRIPTS.parent

# top-level stuff
SETUP_PY = ROOT / "setup.py"
SETUP_CFG = ROOT / "setup.cfg"

_SETUP_DATA = configparser.ConfigParser()
_SETUP_DATA.read(SETUP_CFG)
SETUP_DATA = {key: dict(_SETUP_DATA.items(key)) for key in _SETUP_DATA.sections()}

MANIFEST_IN = ROOT / "MANIFEST.in"
NODE_MODULES = ROOT / "node_modules"
PACKAGE_JSON = ROOT / "package.json"
JS_PACKAGE_DATA = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
JS_NEEDS_INSTALL_KEYS = [
    "dependencies",
    "devDependencies",
    "peerDependencies",
    "version",
]
JS_PKG = JS_PACKAGE_DATA["name"]
JS_VERSION = JS_PACKAGE_DATA["version"]
JS_VERSION_MANGLED = re.sub(r"([ab])(\d+)", "-\\1\\2", JS_VERSION)
YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"
YARN_LOCK = ROOT / "yarn.lock"
CI = ROOT / ".github"
DODO = ROOT / "dodo.py"
BUILD = ROOT / "build"
DIST = ROOT / "dist"
ENVS = ROOT / "envs"
PROJ_LOCK = ROOT / "anaconda-project-lock.yml"
CHANGELOG = ROOT / "CHANGELOG.md"
CONDARC = CI / ".condarc"
README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"
BINDER = ROOT / ".binder"
POSTBUILD = BINDER / "postBuild"

# tools
PY = ["python"]
PYM = [*PY, "-m"]
PIP = [*PYM, "pip"]

JLPM = ["jlpm"]
NPM = ["npm"]
JLPM_INSTALL = [*JLPM, "--prefer-offline"]
PREFLIGHT = ["python", "-m", "scripts.preflight"]
YARN = [shutil.which("yarn") or shutil.which("yarn.cmd")]
LAB_EXT = ["jupyter", "labextension"]
CONDA_BUILD = ["conda-build"]
LAB = ["jupyter", "lab"]
AP = ["anaconda-project"]
AP_PREP = [*AP, "prepare", "--env-spec"]
APR = [*AP, "run", "--env-spec"]
APR_DEFAULT = [*APR, "default"]
APR_ATEST = [*APR, "atest"]
PRETTIER = [*JLPM, "--silent", "prettier"]

JUPYTERLAB_EXE = [
    "conda",
    "run",
    "-p",
    (ROOT / "envs/default"),
    "python",
    "-m",
    "jupyter",
    "lab",
]

# env stuff
OK_ENV = {env: BUILD / f"prep_{env}.ok" for env in ["default", "atest"]}

# python stuff
PY_SRC = ROOT / "py_src" / PY_PKG


# js stuff
JS_LIB = ROOT / "lib"
TSBUILDINFO = ROOT / ".tsbuildinfo"
TS_SRC = ROOT / "src"
STYLE = ROOT / "style"
EXT_PACKAGE_JSON = PY_SRC / "labextension/package.json"

# tests
EXAMPLES = ROOT / "examples"
EXAMPLE_IPYNB = [
    p for p in EXAMPLES.rglob("*.ipynb") if ".ipynb_checkpoints" not in str(p)
]
EXAMPLE_JSON = [
    p for p in EXAMPLES.rglob("*.json") if ".ipynb_checkpoints" not in str(p)
]
EXAMPLE_PY = [*EXAMPLES.rglob("*.py")]
EXAMPLE_INDEX = EXAMPLES / "_index.ipynb"
BUILD_NBHTML = BUILD / "nbsmoke"

# mostly linting
ALL_PY_SRC = [*PY_SRC.rglob("*.py")]
ALL_PY = [
    *ALL_PY_SRC,
    *EXAMPLE_PY,
    *SCRIPTS.rglob("*.py"),
    DODO,
    SETUP_PY,
]
ALL_YML = [*ROOT.glob("*.yml"), *CI.rglob("*.yml")]
ALL_JSON = [*ROOT.glob("*.json"), *EXAMPLE_JSON]
ALL_TS = [*TS_SRC.rglob("*.ts")]
ALL_CSS = [*STYLE.rglob("*.css")]
ALL_MD = [*ROOT.glob("*.md")]
PRETTIER_IGNORE = ROOT / ".prettierignore"
ALL_PRETTIER = [*ALL_YML, *ALL_JSON, *ALL_TS, *ALL_CSS, *ALL_MD]

# built files
OK_RELEASE = BUILD / "release.ok"
OK_PREFLIGHT_CONDA = BUILD / "preflight.conda.ok"
OK_PREFLIGHT_BUILD = BUILD / "preflight.build.ok"
OK_PREFLIGHT_KERNEL = BUILD / "preflight.kernel.ok"
OK_PREFLIGHT_LAB = BUILD / "preflight.lab.ok"
OK_PREFLIGHT_RELEASE = BUILD / "preflight.release.ok"
OK_BLACK = BUILD / "black.ok"
OK_FLAKE8 = BUILD / "flake8.ok"
OK_ROBOT_LINT = BUILD / "robot.lint.ok"
OK_LINT = BUILD / "lint.ok"
OK_PYFLAKES = BUILD / "pyflakes.ok"
OK_NBLINT = {nb.name: BUILD / f"nblint.{nb.name}.ok" for nb in EXAMPLE_IPYNB}
OK_PIP_INSTALL = BUILD / "pip_install.ok"
OK_PRETTIER = BUILD / "prettier.ok"
OK_INDEX = BUILD / "index.ok"
OK_LABEXT = BUILD / "labext.ok"
OK_LINKS = BUILD / "links.ok"

HTMLCOV = BUILD / "htmlcov"
HTMLCOV_INDEX = HTMLCOV / "index.html"
PYTEST_COV_THRESHOLD = 100
PYTEST_HTML = BUILD / "pytest.html"
PYTEST_XUNIT = BUILD / "pytest.xunit.xml"

# derived info
PY_VERSION = JS_PACKAGE_DATA["version"]

# built artifacts
SDIST = DIST / f"{PY_PKG.replace('_', '-')}-{PY_VERSION}.tar.gz"
WHEEL = DIST / f"{PY_PKG}-{PY_VERSION}-py3-none-any.whl"
NPM_TGZ_STEM = JS_PKG.replace("@", "").replace("/", "-")
NPM_TGZ = DIST / f"{NPM_TGZ_STEM}-{JS_VERSION_MANGLED}.tgz"
EXAMPLE_HTML = [BUILD_NBHTML / p.name.replace(".ipynb", ".html") for p in EXAMPLE_IPYNB]
HASH_DEPS = sorted([SDIST, NPM_TGZ, WHEEL])
SHA256SUMS = DIST / "SHA256SUMS"


# servers
SERVERS = PY_SRC / "servers"
SERVER_STATIC = SERVERS / "static"
BUNDLED_SERVERS = [
    "turtle-language-server",
    "stardog-graphql-language-server",
    "sparql-language-server",
]

# robot testing
ATEST = ROOT / "atest"
ALL_ROBOT = [*ATEST.rglob("*.robot")]
ATEST_OUT = ATEST / "output"
ATEST_CANARY = BUILD / f"robot.{PLATFORM.lower()}_success.ok"
