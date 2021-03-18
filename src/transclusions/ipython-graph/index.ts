import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import {
  ILSPCodeExtractorsManager,
  PLUGIN_ID
} from '@krassowski/jupyterlab-lsp';
import { foreign_code_extractors } from './extractors';
import { ICodeMirror, Mode } from '@jupyterlab/codemirror';

export const IPYTHON_GRAPH_TRANSCLUSIONS: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID + ':ipython-graph',
  requires: [ILSPCodeExtractorsManager, ICodeMirror],
  activate: (
    app,
    extractors_manager: ILSPCodeExtractorsManager,
    cm: ICodeMirror
  ) => {
    import('./modes')
      .then(modes => {
        modes.graphqlMode(cm.CodeMirror);
        cm.CodeMirror.defineMIME('application/graphql', 'graphql');
        cm.CodeMirror.modeInfo.push({
          ext: ['graphql', '.graphql'],
          mime: 'application/graphql',
          mode: 'graphql',
          name: 'graphql'
        });
        Mode.ensure('graphql').catch(console.warn);
      })
      .catch(console.warn);

    for (let language of Object.keys(foreign_code_extractors)) {
      for (let extractor of foreign_code_extractors[language]) {
        extractors_manager.register(extractor, language);
        if (extractor.language !== 'graphql') {
          Mode.ensure(extractor.language).catch(console.warn);
          console.log('ensuring', extractor);
        }
      }
    }
  },
  autoStart: true
};
