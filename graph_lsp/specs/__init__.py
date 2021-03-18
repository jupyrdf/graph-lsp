""" default specs
"""
# flake8: noqa: F401

from .graphql_language_server import GRAPHQLLanguageServer
from .sparql_language_server import SPARQLLanguageServer
from .turtle_language_server import TurtleLanguageServer

graphql = GRAPHQLLanguageServer()
sparql = SPARQLLanguageServer()
turtle = TurtleLanguageServer()
