// Copyright (c) 2022 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICodeMirror, Mode } from '@jupyterlab/codemirror';
import {
  ILSPCodeExtractorsManager,
  ILSPFeatureManager,
} from '@krassowski/jupyterlab-lsp';
import { graphExtractors } from './extractors';
import { MODES_PLUGIN_ID, EXTRACTOR_PLUGIN_ID, DEBUG, IGraphModes } from './tokens';
import { graphqlIcon, sparqlIcon, sparulIcon, turtleIcon } from './icons';

/** Plugin metadata for @jupyrdf/jupyterlab-graph-lsp:ipython-graph */
export const extractorPlugin: JupyterFrontEndPlugin<void> = {
  id: EXTRACTOR_PLUGIN_ID,
  autoStart: true,
  requires: [ILSPCodeExtractorsManager, ILSPFeatureManager, IGraphModes],
  activate: activateExtractors,
};

/** Activation for @jupyrdf/jupyterlab-graph-lsp:ipython-graph */
function activateExtractors(
  app: JupyterFrontEnd,
  codeExtractors: ILSPCodeExtractorsManager,
  lspf: ILSPFeatureManager,
  modes: IGraphModes
) {
  // rely on LSPF to ensure plugin ordering
  DEBUG && console.warn('loaded LSP features', lspf);

  modes.ready
    .then(async () => {
      DEBUG && console.warn('adding extractors');
      // install lsp extractors for magics
      const promises = [];
      for (const [language, extractors] of Object.entries(graphExtractors)) {
        for (const extractor of extractors) {
          codeExtractors.register(extractor, language);
          promises.push(Mode.ensure(extractor.language));
        }
      }
      const results = await Promise.all(promises);
      DEBUG && console.table(results);
    })
    .catch((err) => console.error('Failed to install extractors', err));
}

/** Plugin metadata for @jupyrdf/jupyterlab-graph-lsp:graph-modes */
export const modesPlugin: JupyterFrontEndPlugin<IGraphModes> = {
  autoStart: true,
  id: MODES_PLUGIN_ID,
  provides: IGraphModes,
  requires: [ICodeMirror],
  activate: activateModes,
};

/** Activation for @jupyrdf/jupyterlab-graph-lsp:graph-modes */
function activateModes(app: JupyterFrontEnd, cm: ICodeMirror): IGraphModes {
  // add lab-specific files
  app.docRegistry.addFileType({
    name: 'GraphQL',
    mimeTypes: ['application/graphql'],
    extensions: ['.graphql', '.graphqls'],
    icon: graphqlIcon,
  });
  app.docRegistry.addFileType({
    name: 'SPARQL',
    mimeTypes: ['application/sparql-query'],
    extensions: ['.sparql'],
    icon: sparqlIcon,
  });
  app.docRegistry.addFileType({
    name: 'sparul',
    mimeTypes: ['application/sparql-update'],
    extensions: ['.sparul'],
    icon: sparulIcon,
  });
  app.docRegistry.addFileType({
    name: 'Turtle',
    mimeTypes: ['text/turtle'],
    extensions: ['.ttl'],
    icon: turtleIcon,
  });

  /** add the modes */
  async function addModes() {
    DEBUG && console.warn('adding modes');
    // ensures file type are available for documents
    const { installModes } = await import('./modes');
    await installModes(cm.CodeMirror);
    DEBUG && console.warn('modes added');
  }

  return { ready: addModes() };
}

const plugins: JupyterFrontEndPlugin<any>[] = [modesPlugin, extractorPlugin];

DEBUG && console.warn('plugins', plugins);

export default plugins;
