"""Pytest fixtures and configuration
"""
# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.


import pytest
from jupyter_lsp.tests.conftest import handlers, jsonrpc_init_msg, manager

__all__ = ["handlers", "jsonrpc_init_msg", "manager"]

KNOWN_SERVERS = [
    "sparql-language-server",
    "stardog-graphql-language-server",
    "turtle-language-server",
]


@pytest.fixture(params=sorted(KNOWN_SERVERS))
def known_server(request):
    return request.param
