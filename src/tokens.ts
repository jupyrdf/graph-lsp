// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

export const NS = '@jupyrdf/jupyterlab-graph-lsp';
export const EXTRACTOR_PLUGIN_ID = `${NS}:ipython-graph`;
export const MODES_PLUGIN_ID = `${NS}:modes`;

import { LabIcon } from '@jupyterlab/ui-components';

import graphqlSvg from '../style/img/graphql.svg';
import rdfSvg from '../style/img/rdf.svg';

const BASE_COLOR_CLASS = 'jp-icon-contrast3';

export const graphqlIcon = new LabIcon({ svgstr: graphqlSvg, name: `${NS}:graphql` });
export const turtleIcon = new LabIcon({
  svgstr: rdfSvg.replace('RDF', 'TTL').replace(BASE_COLOR_CLASS, 'jp-icon-contrast1'),
  name: `${NS}:turtle`,
});
export const sparqlIcon = new LabIcon({
  svgstr: rdfSvg.replace('RDF', 'SPARQL'),
  name: `${NS}:sparql`,
});
export const sparulIcon = new LabIcon({
  svgstr: rdfSvg
    .replace('RDF', 'SPARUL')
    .replace(BASE_COLOR_CLASS, 'jp-icon-contrast2'),
  name: `${NS}:sparul`,
});
