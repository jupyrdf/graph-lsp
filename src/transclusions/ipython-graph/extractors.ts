import {
  IForeignCodeExtractorsRegistry
  // RegExpForeignCodeExtractor
} from '@krassowski/jupyterlab-lsp/lib';

export let foreign_code_extractors: IForeignCodeExtractorsRegistry = {
  // general note: to match new lines use [^] instead of dot, unless the target is ES2018, then use /s
  python: [
    // new RegExpForeignCodeExtractor({
    //   language: 'sparql',
    //   pattern: '^%%(sparql)( .*?)?\n([^]*)',
    //   extract_to_foreign: '$3',
    //   is_standalone: true,
    //   file_extension: 'rq'
    // }),
    // new RegExpForeignCodeExtractor({
    //   language: 'turtle',
    //   pattern: '^%%(ttl)( .*?)?\n([^]*)',
    //   extract_to_foreign: '$3',
    //   is_standalone: true,
    //   file_extension: 'ttl'
    // }),
    // new RegExpForeignCodeExtractor({
    //   language: 'graphql',
    //   pattern: '^%%(graphql)( .*?)?\n([^]*)',
    //   extract_to_foreign: '$3',
    //   is_standalone: true,
    //   file_extension: 'graphql'
    // })
  ]
};
