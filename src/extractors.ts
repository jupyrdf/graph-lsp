// Copyright (c) 2021 Dane Freeman.
// Distributed under the terms of the Modified BSD License.

import {
  IForeignCodeExtractorsRegistry,
  RegExpForeignCodeExtractor,
} from '@jupyter-lsp/jupyterlab-lsp';

export const graphExtractors: IForeignCodeExtractorsRegistry = {
  // general note: to match new lines use [^] instead of dot, unless the target is ES2018, then use /s
  python: [
    new RegExpForeignCodeExtractor({
      language: 'sparql',
      pattern: '^%%(sparql|sparul)( .*?)?\\n([^]*)',
      foreignCaptureGroups: [3],
      isStandalone: true,
      fileExtension: 'sparql',
    }),
    new RegExpForeignCodeExtractor({
      language: 'turtle',
      pattern: '^%%(ttl|turtle)( .*?)?\n([^]*)',
      foreignCaptureGroups: [3],
      isStandalone: true,
      fileExtension: 'ttl',
    }),
    new RegExpForeignCodeExtractor({
      language: 'graphql',
      pattern: '^%%(graphql)( .*?)?\n([^]*)',
      foreignCaptureGroups: [3],
      isStandalone: true,
      fileExtension: 'graphql',
    }),
  ],
};
