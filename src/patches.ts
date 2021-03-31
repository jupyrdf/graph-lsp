// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import { ILSPFeatureManager } from '@krassowski/jupyterlab-lsp';
import { ICodeMirror } from '@jupyterlab/codemirror';

const SYNTAX = '@krassowski/jupyterlab-lsp:syntax_highlighting';
const CME = 'CodeMirrorEditor';

/** patch get_mode to use The One True CodeMirror
 */
export function patchSyntaxMode(cm: ICodeMirror, lspf: ILSPFeatureManager) {
  for (const feature of lspf.features) {
    if (feature.id !== SYNTAX) {
      continue;
    }
    const factory = feature.editorIntegrationFactory.get(CME);
    if (factory?.prototype == null) {
      return;
    }

    class PatchedCMSyntaxHighlighting extends factory {
      get_mode(language: string): any {
        let mimetype = (this as any).lab_integration.mimeTypeService.getMimeTypeByLanguage(
          {
            name: language,
          }
        );

        if (!mimetype || mimetype == 'text/plain') {
          // if a mimetype cannot be found it will be 'text/plain', therefore do
          // not change mode to text/plain, as this could be a step backwards for
          // the user experience
          console.warn(`no CodeMirror mode for ${language}`);
          return;
        }

        const mode = cm.CodeMirror.findModeByMIME(mimetype);
        console.warn(`found CodeMirror mode for ${language}`, mode);
        return mode;
      }
    }

    feature.editorIntegrationFactory.set(CME, PatchedCMSyntaxHighlighting as any);
    console.warn(`Patched ${SYNTAX}`);
    return;
  }
}
