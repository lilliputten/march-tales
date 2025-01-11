// @ts-check
/** @module Webpack params
 *  @since 2024.10.07, 00:00
 *  @changed 2024.12.31, 12:58
 */

const fs = require('fs');
const path = require('path');

const isDev = getTruthy(process.env.DEV);
const isDebug = getTruthy(process.env.DEBUG) || isDev;

/** Use locally served assets (only for debug mode) */
const useLocallyServedDevAssets = true;

const useInlineSourceMaps = !useLocallyServedDevAssets;

/** Create source maps for production mode (not dev) */
const generateSourcesForProduction = true;

const projectInfoFile = 'static/project-info.txt';
const projectInfo = fs
  .readFileSync(path.resolve(__dirname, projectInfoFile), { encoding: 'utf8' })
  .trim();
const outPath = 'static/compiled';

/** Assets target path */
const assetsPath = '';

const scriptsAssetFile = assetsPath + 'scripts.js';
const stylesAssetFile = assetsPath + 'styles.css';

// @see https://webpack.js.org/configuration/devtool/#devtool
const devtool = isDev
  ? useInlineSourceMaps
    ? 'inline-source-map'
    : 'source-map'
  : generateSourcesForProduction
    ? 'source-map'
    : undefined;
const minimizeAssets = !isDev || !useLocallyServedDevAssets;

// Info:
console.log('DEV:', isDev); // eslint-disable-line no-console
console.log('DEBUG:', isDebug); // eslint-disable-line no-console
console.log('VERSION:', projectInfo); // eslint-disable-line no-console
console.log('devtool:', devtool); // eslint-disable-line no-console
console.log('outPath:', outPath); // eslint-disable-line no-console

// Core helpers...

/** @param {boolean|string|number|undefined|null} val */
function getTruthy(val) {
  if (!val || val === 'false' || val === '0') {
    return false;
  }
  return true;
}

// Export parameters...
module.exports = {
  isDev,
  isDebug,
  projectInfo,
  outPath,
  devtool,
  minimizeAssets,
  scriptsAssetFile,
  stylesAssetFile,
};
