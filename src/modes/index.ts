// Copyright (c) 2022 jupyterlab-graph-lsp contributors.
// Distributed under the terms of the Modified BSD License.

/**
 * Install all of the modes.
 */
export async function installModes(_CodeMirror: any) {
  const { installGraphQL } = await import('./graphql');
  const { installSPARQL } = await import('./sparql');
  const { installTurtle } = await import('./turtle');

  await installGraphQL(_CodeMirror);
  await installSPARQL(_CodeMirror);
  await installTurtle(_CodeMirror);
}
