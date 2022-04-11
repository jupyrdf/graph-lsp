// Copyright (c) 2022 jupyterlab-graph-lsp contributors.
// Distributed under the terms of the Modified BSD License.

import {
  IForeignCodeExtractorsRegistry,
  RegExpForeignCodeExtractor,
} from '@krassowski/jupyterlab-lsp';

export const graphExtractors: IForeignCodeExtractorsRegistry = {
  // general note: to match new lines use [^] instead of dot, unless the target is ES2018, then use /s
  python: [
    new RegExpForeignCodeExtractor({
      language: 'sparql',
      pattern: '^%%(sparql|sparul)( .*?)?\\n([^]*)',
      foreign_capture_groups: [3],
      is_standalone: true,
      file_extension: 'sparql',
    }),
    new RegExpForeignCodeExtractor({
      language: 'turtle',
      pattern: '^%%(ttl|turtle)( .*?)?\n([^]*)',
      foreign_capture_groups: [3],
      is_standalone: true,
      file_extension: 'ttl',
    }),
    new RegExpForeignCodeExtractor({
      language: 'graphql',
      pattern: '^%%(graphql)( .*?)?\n([^]*)',
      foreign_capture_groups: [3],
      is_standalone: true,
      file_extension: 'graphql',
    }),
  ],
};
