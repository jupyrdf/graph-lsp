// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICodeMirror, Mode } from '@jupyterlab/codemirror';
import {
  ILSPCodeExtractorsManager,
  ILSPFeatureManager,
} from '@krassowski/jupyterlab-lsp';
import { graphExtractors } from './extractors';
import { PLUGIN_ID, graphqlIcon, sparqlIcon, sparulIcon, turtleIcon } from './tokens';

export const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  requires: [ICodeMirror, ILSPCodeExtractorsManager, ILSPFeatureManager],
  activate: async (
    app,
    cm: ICodeMirror,
    codeExtractors: ILSPCodeExtractorsManager,
    lspf: ILSPFeatureManager
  ) => {
    // ensures file type is available for documents
    const { installModes } = await import('./modes');

    console.warn(lspf);
    await installModes(cm.CodeMirror);

    /* do lab-specific files */
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

    /* install lsp extractors for magics */
    const promises = [];
    for (const [language, extractors] of Object.entries(graphExtractors)) {
      for (const extractor of extractors) {
        codeExtractors.register(extractor, language);
        promises.push(Mode.ensure(extractor.language));
      }
    }

    console.table(await Promise.all(promises));
  },
  autoStart: true,
};

export default plugin;
