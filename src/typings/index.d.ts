// Copyright (c) 2022 jupyterlab-graph-lsp contributors.
// Distributed under the terms of the Modified BSD License.

/// <reference path="../node_modules/@krassowski/jupyterlab-lsp/src/typings.d.ts"/>
/// <reference path="../typings/codemirror/codemirror.d.ts"/>

declare module 'codemirror/mode/sparql/sparql' {}
declare module 'codemirror/mode/turtle/turtle' {}

declare module '*.svg' {
  const script: string;
  export default script;
}
