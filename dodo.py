""" doit tasks for graph-lsp

    Generally, you'll just want to `doit`.

    `doit release` does pretty much everything.

    See `doit list` for more options.
"""

# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.

import json
import os
import shutil
import subprocess
from hashlib import sha256

from doit.action import CmdAction
from doit.tools import PythonInteractiveAction, config_changed, create_folder

from scripts import project as P
from scripts import reporter
from scripts import utils as U

os.environ.update(
    NODE_OPTS="--max-old-space-size=4096",
    PYTHONIOENCODING="utf-8",
    PIP_DISABLE_PIP_VERSION_CHECK="1",
    MAMBA_NO_BANNER="1",
    CONDA_EXE=os.environ.get("CONDA_EXE", "mamba"),
)

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
    "reporter": reporter.GithubActionsReporter,
}

COMMIT = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()


def task_all():
    """do everything except start lab"""

    file_dep = [
        *P.EXAMPLE_HTML,
        P.HTMLCOV_INDEX,
        P.PYTEST_HTML,
    ]

    if not P.TESTING_IN_CI:
        file_dep += [
            P.OK_RELEASE,
            P.SHA256SUMS,
        ]

    return dict(
        file_dep=file_dep,
        task_dep=["test"],
        actions=([_echo_ok("ALL GOOD")]),
    )


def task_preflight():
    """ensure a sane development environment"""
    file_dep = [P.PROJ_LOCK, P.SCRIPTS / "preflight.py"]

    yield _ok(
        dict(
            uptodate=[config_changed({"commit": COMMIT})],
            name="conda",
            doc="ensure the conda envs have a chance of working",
            file_dep=file_dep,
            actions=(
                [_echo_ok("skipping preflight, hope you know what you're doing!")]
                if P.SKIP_CONDA_PREFLIGHT
                else [[*P.PREFLIGHT, "conda"]]
            ),
        ),
        P.OK_PREFLIGHT_CONDA,
    )

    yield _ok(
        dict(
            name="kernel",
            doc="ensure the kernel has a chance of working",
            file_dep=[*file_dep, P.OK_ENV["default"]],
            actions=[[*P.APR_DEFAULT, *P.PREFLIGHT, "kernel"]],
        ),
        P.OK_PREFLIGHT_KERNEL,
    )

    yield _ok(
        dict(
            name="lab",
            file_dep=[*file_dep, P.OK_LABEXT, P.OK_ENV["default"]],
            actions=[[*P.APR_DEFAULT, *P.PREFLIGHT, "lab"]],
        ),
        P.OK_PREFLIGHT_LAB,
    )

    yield _ok(
        dict(
            name="build",
            doc="ensure the build has a chance of succeeding",
            file_dep=[*file_dep, P.YARN_LOCK, P.OK_ENV["default"]],
            actions=[[*P.APR_DEFAULT, *P.PREFLIGHT, "build"]],
        ),
        P.OK_PREFLIGHT_BUILD,
    )

    yield _ok(
        dict(
            name="release",
            file_dep=[
                P.CHANGELOG,
                P.SDIST,
                P.WHEEL,
                P.NPM_TGZ,
            ],
            actions=[[*P.APR_DEFAULT, *P.PREFLIGHT, "release"]],
        ),
        P.OK_PREFLIGHT_RELEASE,
    )


def task_binder():
    """get to a minimal interactive environment"""
    return dict(
        file_dep=[
            P.OK_PIP_INSTALL,
            P.OK_PREFLIGHT_KERNEL,
            P.OK_PREFLIGHT_LAB,
        ],
        actions=[_echo_ok("ready to run JupyterLab with:\n\n\tdoit lab\n")],
    )


def task_env():
    """prepare project envs"""
    envs = ["default"]
    for i, env in enumerate(envs):
        file_dep = [P.PROJ_LOCK, P.OK_PREFLIGHT_CONDA]
        if P.FORCE_SERIAL_ENV_PREP and i:
            file_dep += [P.OK_ENV[envs[i - 1]]]
        yield _ok(
            dict(
                name=env,
                file_dep=file_dep,
                actions=[
                    (create_folder, [P.ENVS]),
                    [*P.AP_PREP, env],
                ],
            ),
            P.OK_ENV[env],
        )


def task_release():
    """everything we'd need to do to release (except release)"""
    return _ok(
        dict(
            file_dep=[
                P.OK_LINT,
                P.OK_PREFLIGHT_RELEASE,
                P.SHA256SUMS,
            ],
            actions=[_echo_ok("ready to release")],
        ),
        P.OK_RELEASE,
    )


def task_setup():
    """perform all setup activities"""

    _install = ["--no-deps", "--ignore-installed", "-vv"]

    if P.TESTING_IN_CI:
        if P.INSTALL_ARTIFACT == "wheel":
            _install += [P.WHEEL]
        elif P.INSTALL_ARTIFACT == "sdist":
            _install += [P.SDIST]
        else:
            raise RuntimeError(f"Don't know how to install {P.INSTALL_ARTIFACT}")
    else:
        _install += ["-e", "."]

    file_dep = [
        P.NPM_TGZ,
        P.OK_ENV["default"],
        P.SDIST,
        P.WHEEL,
    ]

    if not P.TESTING_IN_CI:
        file_dep += [P.SETUP_CFG, P.MANIFEST_IN, P.SETUP_PY, P.EXT_PACKAGE_JSON]
        file_dep += [
            P.SERVER_STATIC / server / "package.json" for server in P.BUNDLED_SERVERS
        ]

    py_task = _ok(
        dict(
            name="py",
            uptodate=[config_changed({"artifact": P.INSTALL_ARTIFACT})],
            file_dep=file_dep,
            actions=[
                [*P.APR_DEFAULT, *P.PIP, "install", *_install],
                # [*P.APR_DEFAULT, *P.PIP, "check"],
            ],
        ),
        P.OK_PIP_INSTALL,
    )

    if P.TESTING_IN_CI and P.INSTALL_ARTIFACT:
        py_task = _ok(py_task, P.OK_LABEXT)

    yield py_task

    if not P.TESTING_IN_CI:

        js_deps = [P.PACKAGE_JSON, P.OK_ENV["default"]]
        js_targets = [P.YARN_INTEGRITY]

        if P.YARN_LOCK.exists():
            js_deps += [P.YARN_LOCK]
        else:
            js_targets += [P.YARN_LOCK]

        yield dict(
            name="js",
            file_dep=js_deps,
            actions=[[*P.APR_DEFAULT, *P.JLPM_INSTALL]],
            targets=js_targets,
        )
        yield dict(
            name="dedupe",
            file_dep=js_deps,
            actions=[[*P.APR_DEFAULT, *P.JLPM, "deduplicate"]],
        )
        yield _ok(
            dict(
                name="labext",
                actions=[
                    [
                        *P.APR_DEFAULT,
                        *P.LAB_EXT,
                        "develop",
                        ".",
                        "--overwrite",
                        "--debug",
                    ]
                ],
                file_dep=[P.OK_PIP_INSTALL],
            ),
            P.OK_LABEXT,
        )


if not P.TESTING_IN_CI:

    def task_build():
        """build packages"""

        yield dict(
            name="ts",
            file_dep=[
                *P.ALL_TS,
                P.LICENSE,
                P.OK_ENV["default"],
                P.OK_PRETTIER,
                P.PACKAGE_JSON,
                P.README,
                P.YARN_INTEGRITY,
            ],
            actions=[[*P.APR_DEFAULT, *P.JLPM, "build"]],
            targets=[P.TSBUILDINFO, P.EXT_PACKAGE_JSON],
        )

        yield dict(
            name="pack",
            file_dep=[P.TSBUILDINFO, P.PACKAGE_JSON, P.LICENSE, P.README, *P.ALL_CSS],
            actions=[(create_folder, [P.DIST]), [*P.APR_DEFAULT, "ext:pack"]],
            targets=[P.NPM_TGZ],
        )

        deployed_servers = []

        def _copy_with_no_return(src, dest):
            shutil.copytree(src, dest)

        for server in P.BUNDLED_SERVERS:
            deployed_servers += [P.SERVER_STATIC / server / "package.json"]
            yield dict(
                name=f"server:{server}",
                file_dep=[P.NODE_MODULES / server / "package.json", P.YARN_INTEGRITY],
                targets=[P.SERVER_STATIC / server / "package.json"],
                actions=[
                    (create_folder, [P.SERVER_STATIC]),
                    (
                        shutil.rmtree,
                        [P.SERVER_STATIC / server],
                        dict(ignore_errors=True),
                    ),
                    (
                        (
                            _copy_with_no_return,
                            [P.NODE_MODULES / server, P.SERVER_STATIC / server],
                        )
                    ),
                ],
            )

        yield dict(
            name="py",
            file_dep=[
                *P.ALL_PY_SRC,
                P.EXT_PACKAGE_JSON,
                P.LICENSE,
                P.MANIFEST_IN,
                P.OK_ENV["default"],
                P.OK_LINT,
                P.README,
                P.SETUP_CFG,
                P.SETUP_PY,
                *deployed_servers,
            ],
            actions=[
                [*P.APR_DEFAULT, *P.PY, "setup.py", "sdist"],
                [*P.APR_DEFAULT, *P.PY, "setup.py", "bdist_wheel"],
            ],
            targets=[P.WHEEL, P.SDIST],
        )

        def _run_hash():
            # mimic sha256sum CLI
            if P.SHA256SUMS.exists():
                P.SHA256SUMS.unlink()

            lines = []

            for p in P.HASH_DEPS:
                lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

            output = "\n".join(lines)
            print(output)
            P.SHA256SUMS.write_text(output)

        yield dict(
            name="hash",
            file_dep=P.HASH_DEPS,
            targets=[P.SHA256SUMS],
            actions=[_run_hash],
        )


def task_test():
    """run all the notebooks"""

    def _nb_test(nb):
        def _test():
            env = dict(os.environ)
            args = [
                *P.APR_DEFAULT,
                "jupyter",
                "nbconvert",
                "--to",
                "html",
                "--output-dir",
                P.BUILD_NBHTML,
                "--execute",
                "--ExecutePreprocessor.timeout=1200",
                nb,
            ]
            return CmdAction(args, env=env, shell=False)

        file_dep = [
            *P.ALL_PY_SRC,
            *P.EXAMPLE_IPYNB,
            *P.EXAMPLE_JSON,
            P.OK_ENV["default"],
            P.OK_PIP_INSTALL,
            P.OK_PREFLIGHT_KERNEL,
            *([] if P.TESTING_IN_CI else [P.OK_NBLINT[nb.name]]),
        ]

        return dict(
            name=f"nb:{nb.name}".replace(" ", "_").replace(".ipynb", ""),
            file_dep=file_dep,
            actions=[_test()],
            targets=[P.BUILD_NBHTML / nb.name.replace(".ipynb", ".html")],
        )

    for nb in P.EXAMPLE_IPYNB:
        yield _nb_test(nb)

    utest_args = [
        *P.APR_DEFAULT,
        "pytest",
        "--cov-fail-under",
        str(P.PYTEST_COV_THRESHOLD),
    ]

    if P.UTEST_PROCESSES:
        utest_args += ["-n", P.UTEST_PROCESSES]

    pytest_args = os.environ.get("PYTEST_ARGS", "").strip()

    if pytest_args:
        try:
            utest_args += json.loads(pytest_args)
        except Exception as err:
            print(err)

    yield dict(
        name="utest",
        doc="run unit tests with pytest",
        uptodate=[config_changed(COMMIT)],
        file_dep=[*P.ALL_PY_SRC, P.SETUP_CFG, P.OK_PIP_INSTALL],
        targets=[P.HTMLCOV_INDEX, P.PYTEST_HTML, P.PYTEST_XUNIT],
        actions=[
            utest_args,
            lambda: U.strip_timestamps(
                *P.HTMLCOV.rglob("*.html"), P.PYTEST_HTML, slug=COMMIT
            ),
        ],
    )

    raw_eps = P.SETUP_DATA["options.entry_points"]["console_scripts"]
    for ep in raw_eps.strip().splitlines():
        script, tgt = ep.split("=")
        script = script.strip()
        yield dict(
            name=f"cli:{script}",
            doc="smoke test the CLI",
            actions=[
                [*P.APR_DEFAULT, script, "--help"],
                [*P.APR_DEFAULT, script, "--version"],
            ],
            file_dep=[P.SETUP_CFG, P.OK_PIP_INSTALL],
        )


if not P.TESTING_IN_CI:

    def task_lint():
        """format all source files"""

        yield _ok(
            dict(
                name="black",
                file_dep=[*P.ALL_PY, P.OK_ENV["default"], P.SETUP_CFG],
                actions=[
                    [*P.APR_DEFAULT, "isort", "--quiet", "--ac", *P.ALL_PY],
                    [*P.APR_DEFAULT, "black", "--quiet", *P.ALL_PY],
                ],
            ),
            P.OK_BLACK,
        )
        yield _ok(
            dict(
                name="flake8",
                file_dep=[*P.ALL_PY, P.OK_BLACK],
                actions=[[*P.APR_DEFAULT, "flake8", *P.ALL_PY]],
            ),
            P.OK_FLAKE8,
        )
        yield _ok(
            dict(
                name="pyflakes",
                file_dep=[*P.ALL_PY, P.OK_BLACK],
                actions=[[*P.APR_DEFAULT, "pyflakes", *P.ALL_PY]],
            ),
            P.OK_PYFLAKES,
        )
        yield _ok(
            dict(
                name="prettier",
                uptodate=[
                    config_changed(
                        dict(
                            conf=P.JS_PACKAGE_DATA["prettier"],
                            script=P.JS_PACKAGE_DATA["scripts"]["lint:prettier"],
                        )
                    )
                ],
                file_dep=[
                    *P.ALL_PRETTIER,
                    P.OK_ENV["default"],
                    P.PRETTIER_IGNORE,
                    P.YARN_INTEGRITY,
                ],
                actions=[[*P.APR_DEFAULT, *P.JLPM, "lint:prettier"]],
            ),
            P.OK_PRETTIER,
        )

        for nb in P.EXAMPLE_IPYNB:
            yield _ok(
                dict(
                    name=f"nblint:{nb.name}".replace(" ", "_").replace(".ipynb", ""),
                    file_dep=[P.YARN_INTEGRITY, nb, P.OK_ENV["default"], P.OK_BLACK],
                    actions=[[*P.APR_DEFAULT, *P.PYM, "scripts.nblint", nb]],
                ),
                P.OK_NBLINT[nb.name],
            )

        yield _ok(
            dict(
                name="all",
                actions=[_echo_ok("all ok")],
                file_dep=[
                    P.OK_BLACK,
                    P.OK_FLAKE8,
                    P.OK_PRETTIER,
                    P.OK_PYFLAKES,
                ],
            ),
            P.OK_LINT,
        )


def task_lab():
    """run JupyterLab "normally" (not watching sources)"""

    def lab():
        proc = subprocess.Popen(
            list(
                map(str, [*P.APR_DEFAULT, "jupyter", "lab", "--no-browser", "--debug"])
            ),
            stdin=subprocess.PIPE,
        )

        try:
            proc.wait()
        except KeyboardInterrupt:
            print("attempting to stop lab, you may want to check your process monitor")
            proc.terminate()
            proc.communicate(b"y\n")

        proc.wait()
        return True

    return dict(
        uptodate=[lambda: False],
        file_dep=[P.OK_PIP_INSTALL, P.OK_PREFLIGHT_LAB],
        actions=[PythonInteractiveAction(lab)],
    )


if not P.TESTING_IN_CI:

    def task_watch():
        """watch typescript sources, launch lab, rebuilding as files change"""

        def _watch():
            lib = subprocess.Popen(
                list(map(str, [*P.APR_DEFAULT, *P.JLPM, "watch:lib"]))
            )
            ext = subprocess.Popen(
                list(map(str, [*P.APR_DEFAULT, *P.JLPM, "watch:ext"]))
            )

            try:
                lib.wait()
            except KeyboardInterrupt:
                pass
            finally:
                lib.terminate()
                ext.terminate()

            return True

        return dict(
            uptodate=[lambda: False],
            file_dep=[P.OK_PREFLIGHT_LAB],
            actions=[PythonInteractiveAction(_watch)],
        )


def _echo_ok(msg):
    def _echo():
        print(msg, flush=True)
        return True

    return _echo


def _ok(task, ok):
    task.setdefault("targets", []).append(ok)
    task["actions"] = [
        lambda: [ok.exists() and ok.unlink(), True][-1],
        *task["actions"],
        lambda: [
            ok.parent.mkdir(exist_ok=True),
            ok.write_text("ok", encoding="utf-8"),
            True,
        ][-1],
    ]
    return task


def _call(args, **kwargs):
    if "cwd" in kwargs:
        kwargs["cwd"] = str(kwargs["cwd"])
    if "env" in kwargs:
        kwargs["env"] = {k: str(v) for k, v in kwargs["env"].items()}
    args = list(map(str, args))
    print("\n>>>", " ".join(args), "\n", flush=True)
    return subprocess.call(args, **kwargs)
