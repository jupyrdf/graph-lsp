# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

import pytest
from jupyter_lsp.schema import LANGUAGE_SERVER_SPEC

from jupyterlab_graph_lsp.specs import graphql, sparql, turtle


@pytest.mark.parametrize("spec", [graphql, sparql, turtle])
def test_spec(spec):
    """is the spec a thing?"""
    LANGUAGE_SERVER_SPEC.validate(spec)
