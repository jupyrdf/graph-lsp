// Copyright (c) 2022 Dane Freeman.
// Distributed under the terms of the Modified BSD License.
import { Token } from '@lumino/coreutils';

/** The package namespace */
export const NS = '@jupyrdf/jupyterlab-graph-lsp';

/** The plugin ID for the language extractors (magic support) */
export const EXTRACTOR_PLUGIN_ID = `${NS}:ipython-graph`;

/** The plugin ID for the CodeMirror modes */
export const MODES_PLUGIN_ID = `${NS}:graph-modes`;

/** The plugin ID for the CodeMirror modes */
export const IGraphModes = new Token<IGraphModes>(MODES_PLUGIN_ID);

/** The public interface for the graph modes. */
export interface IGraphModes {
  /** A promise that resolves when the modes are installed. */
  ready: Promise<void>;
}

/** A live debugging tool which increases verbosity. */
export const DEBUG = window.location.href.indexOf('GRAPH_LSP_DEBUG') > -1;

DEBUG && console.warn('GRAPH_LSP_DEBUG active');
