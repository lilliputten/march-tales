// @ts-check

/** @module Webpack config
 *  @since 2024.10.07, 00:00
 *  @changed 2024.12.31, 12:59
 */

const path = require('path');

const webpack = require('webpack');

const ImageMinimizerPlugin = require('image-minimizer-webpack-plugin');

const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
// const CopyPlugin = require('copy-webpack-plugin');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const {
  isDev,
  isDebug,
  projectInfo,
  outPath,
  devtool,
  minimizeAssets,
  scriptsAssetFile,
  stylesAssetFile,
} = require('./webpack.params');

const maxAssetSize = 8 * 1024;

module.exports = {
  mode: isDev ? 'development' : 'production',
  // @see https://webpack.js.org/configuration/devtool/#devtool
  devtool,
  entry: [
    // NOTE: See also `files` field in `tsconfig.json`
    './src/assets/index.ts',
    './src/assets/styles.scss',
  ],
  resolve: {
    extensions: ['.scss', '.sass', '.css', '.tsx', '.ts', '.js', '.jpg', '.jpeg', '.png', '.svg'],
  },
  module: {
    rules: [
      {
        test: /\.html$/i,
        loader: 'html-loader',
      },
      {
        test: /\.tsx?$/,
        // @see https://github.com/TypeStrong/ts-loader
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.s[ac]ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              esModule: false,
            },
          },
          // Translates CSS into CommonJS
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              // modules: true,
              modules: {
                // compileType: 'icss',
                // mode: 'local',
                mode: 'icss',
              },
              sourceMap: true,
              // @see https://webpack.js.org/loaders/css-loader/#url
              url: {
                filter:
                  /**
                   * @param {string} url
                   * @param {string} _resourcePath
                   * @return boolean
                   */
                  (url, _resourcePath) => {
                    return !url.startsWith('/static');
                  },
              },
            },
          },
          {
            loader: 'resolve-url-loader',
            options: {
              sourceMap: true,
            },
          },
          // Compiles Sass to CSS
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              /* // NOTE: Inject 'use' for math and color features, import common variables and mixins.
               * additionalData: [
               *   // '@use "sass:math";',
               *   // '@use "sass:color";',
               *   // '@import "src/variables.scss";',
               *   // '@import "src/mixins.scss";',
               * ]
               *   .filter(Boolean)
               *   .join('\n'),
               */
              api: 'modern',
              sassOptions: {
                // @see https://github.com/sass/node-sass#outputstyle
                outputStyle: minimizeAssets ? 'compressed' : 'expanded',
                // @see https://www.npmjs.com/package/node-sass-glob-importer
                // importer: globImporter(), # Got error here as the plugin is obsolete
                quietDeps: true,
                /* @type {Deprecations[]}
                 */
                silenceDeprecations: [
                  // @see node_modules/sass/types/deprecations.d.ts
                  'import',
                  'color-functions',
                  'global-builtin',
                ],
              },
            },
          },
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)$/i,
        // More information here https://webpack.js.org/guides/asset-modules/
        type: 'asset',
        parser: {
          dataUrlCondition: {
            maxSize: maxAssetSize, // 4kb
          },
        },
      },
    ],
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.DEV': isDev,
      'process.env.DEBUG': isDebug,
      'process.env.APP_VERSION': JSON.stringify(projectInfo),
    }),
    new MiniCssExtractPlugin({
      filename: stylesAssetFile,
    }),
  ],
  optimization: {
    minimize: minimizeAssets,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
        // exclude: 'assets',
        terserOptions: {
          compress: {
            drop_debugger: false,
          },
        },
      }),
      new ImageMinimizerPlugin({
        minimizer: {
          implementation: ImageMinimizerPlugin.sharpMinify,
          options: {
            encodeOptions: {
              // Options for `sharp`
              // https://sharp.pixelplumbing.com/api-output
            },
          },
        },
      }),
    ],
  },
  performance: {
    hints: false,
    maxEntrypointSize: maxAssetSize,
  },
  output: {
    filename: scriptsAssetFile,
    // NOTE: See also `outDir` field in `tsconfig.json`
    path: path.resolve(__dirname, outPath),
    // @see https://webpack.js.org/configuration/output/#outputassetmodulefilename
    assetModuleFilename: `extracted/[name]-[hash][ext][query]`,
  },
};
