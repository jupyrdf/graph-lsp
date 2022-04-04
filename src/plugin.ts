// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICodeMirror, Mode } from '@jupyterlab/codemirror';
import {
  ILSPCodeExtractorsManager,
  ILSPFeatureManager,
} from '@krassowski/jupyterlab-lsp';
import { graphExtractors } from './extractors';
import { MODES_PLUGIN_ID, EXTRACTOR_PLUGIN_ID, graphqlIcon, sparqlIcon, sparulIcon, turtleIcon, DEBUG } from './tokens';

export const extractorPlugin: JupyterFrontEndPlugin<void> = {
  id: EXTRACTOR_PLUGIN_ID,
  requires: [ILSPCodeExtractorsManager, ILSPFeatureManager],
  activate: async (
    app,
    codeExtractors: ILSPCodeExtractorsManager,
    lspf: ILSPFeatureManager
  ) => {
    // rely on LSPF to ensure plugin ordering
    if (DEBUG) {
      console.warn('loaded LSP features', lspf);
    }

    // install lsp extractors for magics
    const promises = [];
    for (const [language, extractors] of Object.entries(graphExtractors)) {
      for (const extractor of extractors) {
        codeExtractors.register(extractor, language);
        promises.push(Mode.ensure(extractor.language));
      }
    }

    Promise.all(promises).then((results) => console.table(results)).catch(console.warn);
  },
};

export const modesPlugin: JupyterFrontEndPlugin<void> = {
  id: MODES_PLUGIN_ID,
  autoStart: true,
  requires: [ICodeMirror],
  activate: async (
    app,
    cm: ICodeMirror,
  ) => {
    // ensures file type are available for documents
    const { installModes } = await import('./modes');

    await installModes(cm.CodeMirror);

    // add lab-specific files
    app.docRegistry.addFileType({
      name: 'GraphQL',
      mimeTypes: ['application/graphql'],
      extensions: ['.graphql'],
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
  },
};

export default [modesPlugin, extractorPlugin];
