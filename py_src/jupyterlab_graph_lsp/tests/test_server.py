""" Smoke test the language servers starting
"""
# Copyright (c) 2022 jupyterlab-graph-lsp contributors.
# Distributed under the terms of the Modified BSD License.

import asyncio

import pytest
from jupyter_lsp.tests.test_session import assert_status_set


@pytest.mark.asyncio
async def test_start_known(known_server, handlers, jsonrpc_init_msg):
    """will a process start for a known server if a handler starts?"""
    handler, ws_handler = handlers
    manager = handler.manager

    manager.initialize()

    assert_status_set(handler, {"not_started"})

    ws_handler.open(known_server)
    session = manager.sessions[ws_handler.language_server]
    assert session.process is not None

    assert_status_set(handler, {"started"}, known_server)

    await ws_handler.on_message(jsonrpc_init_msg)

    try:
        await asyncio.wait_for(
            ws_handler._messages_wrote.get(),
            120,
        )
        ws_handler._messages_wrote.task_done()
    finally:
        ws_handler.on_close()

    assert not session.handlers
    assert not session.process

    assert_status_set(handler, {"stopped"}, known_server)
    assert_status_set(handler, {"stopped", "not_started"})
