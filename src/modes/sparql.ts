// Copyright (c) 2022 jupyterlab-graph-lsp contributors.
// Distributed under the terms of the Modified BSD License.

/**
 * Add additional mappings for SPARQL.
 */
export async function installSPARQL(_CodeMirror: any) {
  _CodeMirror.modeInfo.push({
    ext: ['sparul', '.sparul'],
    mime: 'application/sparql-query',
    mode: 'sparql',
    name: 'sparul',
  });
}
