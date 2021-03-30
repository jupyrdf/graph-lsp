// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICodeMirror, Mode } from '@jupyterlab/codemirror';
import { ILSPCodeExtractorsManager } from '@krassowski/jupyterlab-lsp';
import { graphExtractors } from './extractors';
import { PLUGIN_ID } from './tokens';

export const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  requires: [ILSPCodeExtractorsManager, ICodeMirror],
  activate: (app, codeExtractors: ILSPCodeExtractorsManager, cm: ICodeMirror) => {
    import('./modes')
      .then((modes) => {
        modes.graphqlMode(cm.CodeMirror);
        cm.CodeMirror.defineMIME('application/graphql', 'graphql');
        cm.CodeMirror.modeInfo.push({
          ext: ['graphql', '.graphql'],
          mime: 'application/graphql',
          mode: 'graphql',
          name: 'graphql',
        });
        Mode.ensure('graphql').catch(console.warn);
      })
      .catch(console.warn);

    for (const [language, extractors] of Object.entries(graphExtractors)) {
      for (const extractor of extractors) {
        codeExtractors.register(extractor, language);
        if (extractor.language !== 'graphql') {
          Mode.ensure(extractor.language).catch(console.warn);
        }
      }
    }
  },
  autoStart: true,
};

export default plugin;
