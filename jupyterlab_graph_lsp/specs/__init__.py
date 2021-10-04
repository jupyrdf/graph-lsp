""" default specs
"""

# Copyright (c) 2021 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

from .graphql_language_server import GRAPHQLLanguageServer
from .sparql_language_server import SPARQLLanguageServer
from .turtle_language_server import TurtleLanguageServer

graphql = GRAPHQLLanguageServer()
sparql = SPARQLLanguageServer()
turtle = TurtleLanguageServer()

__all__ = ["graphql", "sparql", "turtle"]
