// @ts-check

/** @module Webpack config
 *  @since 2024.10.07, 00:00
 *  @changed 2024.12.14, 18:10
 */

const fs = require('fs');
const path = require('path');

// eslint-disable-next-line no-unused-vars
const webpack = require('webpack'); // Used only for typings

const {
  scriptsAssetFile,
  stylesAssetFile,
  localServerPrefix,
  customResources,
  includeTemplateFile,
  projectHash,
  appId,
  appFolder,
  uploadsFolder,
  useInlineProdAssets,
} = require('./webpack.params');

/** @param {webpack.sources.Source | webpack.sources.ConcatSource} asset */
function getSourceContent(asset) {
  /** @type {string | Buffer} */
  const content = asset.source();
  // Convert to string if buffer...
  if (content instanceof Buffer) {
    return content.toString('utf8');
  }
  // TODO: Check other (?) types?
  return String(content);
}

/** @param {webpack.sources.Source | webpack.sources.ConcatSource} asset */
function getAssetContent(asset) {
  /** @type {string} */
  let content = '';
  // Extract content from a list of children or a single item...
  const concatSourceAsset = /** @type {webpack.sources.ConcatSource} */ (asset);
  if (typeof concatSourceAsset.getChildren === 'function') {
    const sources = concatSourceAsset.getChildren();
    content = sources.map(getSourceContent).join('');
  } else {
    content = getSourceContent(asset);
  }
  return content;
}

/**
 * @param {webpack.Compilation} compilation
 * @param {object} [opts]
 * @param {boolean} [opts.isDev]
 * @param {boolean} [opts.isDebug]
 * @param {boolean} [opts.useLocallyServedDevAssets]
 */
function getCompilationScriptsContent(compilation, opts = {}) {
  const { isDebug, isDev, useLocallyServedDevAssets } = opts;
  /* console.log('[webpack.helpers:getCompilationScriptsContent]', {
   *   isDebug,
   *   isDev,
   *   useLocallyServedDevAssets,
   *   useInlineProdAssets,
   * });
   */
  if (isDev && useLocallyServedDevAssets) {
    return [
      '<!-- Locally linked scripts & styles -->',
      customResources.trim(),
      `<link rel="stylesheet" type="text/css" href="${localServerPrefix}${stylesAssetFile}?${projectHash}" />`,
      `<script type="text/javascript" src="${localServerPrefix}${scriptsAssetFile}?${projectHash}"></script>`,
    ].join('\n');
  }
  // TODO: (Temporarily unused) Generate inline assets from the compilation...
  const { assets } = compilation;
  // Get scripts chunk...
  /** @type {webpack.sources.Source} */
  const scriptsAsset = assets[scriptsAssetFile];
  if (!scriptsAsset) {
    throw new Error('Script asset "' + scriptsAssetFile + '" not found!');
  }
  const scriptsContent = getAssetContent(scriptsAsset);
  // Get styles chunk...
  /** @type {webpack.sources.Source} */
  const stylesAsset = assets[stylesAssetFile];
  if (!stylesAsset) {
    throw new Error('Style asset "' + stylesAssetFile + '" not found!');
  }
  const stylesContent = getAssetContent(stylesAsset);
  if (isDebug || useInlineProdAssets) {
    // Create inlined (base64-encoded) assets
    return [
      `<!-- Injected scripts begin (${scriptsAssetFile}) -->`,
      `<script type="text/javascript" src="data:text/javascript;base64,${btoa(scriptsContent)}"></script>`,
      `<!-- Injected scripts end (${scriptsAssetFile}) -->`,
      '',
      `<!-- Injected styles begin (${stylesAssetFile}) -->`,
      `<link rel="stylesheet" type="text/css" href="data:text/css;base64,${btoa(stylesContent)}" />`,
      `<!-- Injected styles end (${stylesAssetFile}) -->`,
    ].join('\n');
  }
  // Create embedded assets
  return [
    `<!-- Inline scripts begin (${scriptsAssetFile}) -->`,
    '<script type="text/javascript">',
    scriptsContent,
    '</script>',
    `<!-- Inline scripts end (${scriptsAssetFile}) -->`,
    '',
    `<!-- Inline styles begin (${stylesAssetFile}) -->`,
    '<style type="text/css">',
    stylesContent,
    '</style>',
    `<!-- Inline styles end (${stylesAssetFile}) -->`,
  ].join('\n');
}

function getIncludeTemplate() {
  const content = fs
    .readFileSync(path.resolve(__dirname, includeTemplateFile), {
      encoding: 'utf8',
    })
    .replace(/{#[\s\S]+?#}/gm, '')
    .replace(/\{\{appId\}\}/g, appId)
    .replace(/\{\{appFolder\}\}/g, appFolder)
    .replace(/\{\{uploadsFolder\}\}/g, uploadsFolder)
    .replace(/\{\{projectHash\}\}/g, projectHash)
    .replace(/[ \t]+\n/gm, '\n')
    .replace(/\n{3,}/gm, '\n\n')
    .trim();
  return content;
}

/**
 * @param {webpack.Compilation} compilation
 * @param {object} [opts]
 * @param {boolean} [opts.isDev]
 * @param {boolean} [opts.isDebug]
 * @param {boolean} [opts.useLocallyServedDevAssets]
 */
function getIncludeFragment(compilation, opts) {
  // Get scripts chunk content...
  const includeContent = getCompilationScriptsContent(compilation, opts);
  const includeFragment = getIncludeTemplate()
    // prettier-ignore
    .replace(/\{\{CONTENT\}\}/g, includeContent);
  return includeFragment;
}

module.exports = {
  // getCompilationScriptsContent,
  getIncludeFragment,
};
