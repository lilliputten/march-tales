// @ts-check

/** @module Webpack params
 *  @since 2024.10.07, 00:00
 *  @changed 2024.12.14, 19:22
 */

const fs = require('fs');
const path = require('path');

const packageData = require(path.resolve(__dirname, 'package.json'));

const isDev = getTruthy(process.env.DEV);
const isDebug = getTruthy(process.env.DEBUG);

/** Use locally served assets (only for debug mode) */
const useLocallyServedDevAssets = true;

/** Use inlined (with base64 encoding) assets (only for production mode) */
const useInlineProdAssets = true;

const useInlineSourceMaps = !useLocallyServedDevAssets;

/** Create source maps for production mode (not dev) */
const generateSourcesForProduction = true;

// const includeTemplateFile = 'src/include-template.html';
// const previewTemplateFile = 'src/preview-template-base.html';

const projectName = packageData.name;

const projectInfoFile = 'static/project-info.txt';
const projectHashFile = 'static/project-hash.txt';
const projectInfo = fs
  .readFileSync(path.resolve(__dirname, projectInfoFile), { encoding: 'utf8' })
  .trim();
const projectHash = fs
  .readFileSync(path.resolve(__dirname, projectHashFile), { encoding: 'utf8' })
  .trim();
const outPath = 'static/assets';

// Sync with `src/variables/variables.scss`
const appId = 'delivery-options';
const appFolder = `page-${appId}`;
/** A folder to deploy all automatically and manually generated assets */
// const uploadsFolder = `upload/${appFolder}`;

/** Assets target path */
const assetsPath = ''; // `${uploadsFolder}/`;

const scriptsAssetFile = assetsPath + 'scripts.js';
const stylesAssetFile = assetsPath + 'styles.css';

const localServerPrefix = '/'; // http://localhost:3000/';

// @see https://webpack.js.org/configuration/devtool/#devtool
const devtool = isDev
  ? useInlineSourceMaps
    ? 'inline-source-map'
    : 'source-map'
  : generateSourcesForProduction
    ? 'source-map'
    : undefined;
const minimizeAssets = !isDev || !useLocallyServedDevAssets;

// Inluce other resources here, to protect webpack from changing the urls (and trying to find the resource and include to the build)
const customResources = [
  // '<link rel="stylesheet" type="text/css" href="/assets/b7f4f2a8/css/about.css">',
  // '<script src="https://cdn.jsdelivr.net/npm/bootstrap3@3.3.5/dist/js/bootstrap.min.js"></script>',
]
  .filter(Boolean)
  .join('\n');

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

  useLocallyServedDevAssets,
  useInlineProdAssets,

  // includeTemplateFile,
  // previewTemplateFile,

  generateSourcesForProduction,

  // projectInfoFile,
  projectName,
  projectInfo,
  projectHash,
  outPath,

  appId,
  appFolder,
  // uploadsFolder,

  scriptsAssetFile,
  stylesAssetFile,

  localServerPrefix,

  devtool,
  minimizeAssets,

  customResources,
};
