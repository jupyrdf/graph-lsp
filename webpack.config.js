//@ts-check

const webpack = require('webpack');
const path = require('path');

/** @type {import('webpack').Configuration} */
const config = {
  output: {
    clean: true,
  },
  target: 'web',
  mode: 'development',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        use: ['source-map-loader'],
      },
    ],
  },

  plugins: [],
  ignoreWarnings: [/Failed to parse source map/],
};

module.exports = config;
