import pytest

from jupyterlab_graph_lsp.specs import graphql, sparql, turtle


@pytest.mark.parametrize("spec", [graphql, sparql, turtle])
def test_spec(spec):
    assert spec
