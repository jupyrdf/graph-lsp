import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IPYTHON_GRAPH_TRANSCLUSIONS } from './ipython-graph';

export const DEFAULT_TRANSCLUSIONS: JupyterFrontEndPlugin<void>[] = [
  IPYTHON_GRAPH_TRANSCLUSIONS
];
