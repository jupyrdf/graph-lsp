import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { DEFAULT_TRANSCLUSIONS } from './transclusions/defaults';

const plugins: JupyterFrontEndPlugin<any>[] = [...DEFAULT_TRANSCLUSIONS];

/**
 * Export the plugins as default.
 */
export default plugins;
