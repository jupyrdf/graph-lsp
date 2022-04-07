# jupyterlab-graph-lsp

> Graph Language Server extensions for [jupyterlab-lsp].

[jupyterlab-lsp]: https://github.com/jupyter-lsp/jupyterlab-lsp

[![PyPI][pypi-badge]][pypi] [![Conda][conda-badge]][conda-forge]
[![CI status][ci-badge]][ci]

[pypi]: https://pypi.org/project/jupyterlab-graph-lsp
[conda-forge]: https://anaconda.org/conda-forge/jupyterlab-graph-lsp
[pypi-badge]: https://img.shields.io/pypi/v/jupyterlab-graph-lsp
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/jupyterlab-graph-lsp
[ci-badge]: https://img.shields.io/github/checks-status/jupyrdf/graph-lsp/master
[ci]: https://github.com/jupyrdf/graph-lsp/actions

## Prerequisites

- Python >=3.7
- JupyterLab >=3.1
- NodeJS LTS

## Install

```bash
pip install jupyterlab-graph-lsp
```

or

```bash
conda install -c conda-forge jupyterlab-graph-lsp
```

## Usage

- open `.graphql`, `.graphqls`, `.sparql`, `.sparul` and `.ttl` files to get:
  - syntax highlighting
  - additional language features, including hover and completion
- write `%%sparql`, `%%turtle`, and `%%graphql` in python documents
  - kernel-side implementations not provided: see `Magics.ipynb` in the project
    repository for very simple examples

## Uninstall

```bash
pip uninstall jupyterlab-graph-lsp
```

or

```bash
conda uninstall jupyterlab-graph-lsp
```

## Open Source

> Copyright (c) 2022 jupyterlab-graph-lsp contributors.
>
> Distributed under the terms of the Modified BSD License.

### Third-Party Software

This package includes a number of third-party javascript extensions, including the
Stardog language servers themselves, which are licensed under the [Apache-2.0] license.

[apache-2.0]:
  https://github.com/stardog-union/stardog-language-servers/blob/master/LICENSE
