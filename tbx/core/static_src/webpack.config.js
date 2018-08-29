const path = require('path');
const webpack = require('webpack');

const options = {
  entry: {
    main: './javascript/main.js' // multiple entries can be added here
  },
  output: {
    path: path.resolve('../static_compiled/js/'),
    filename: '[name].js' // based on entry name, e.g. main.js
  },
  module: {
    rules: [
      {
        // tells webpack how to handle js files
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  },
  // externals are loaded via base.html and not included in the webpack bundle.
  // jQuery is loaded this way to make the bundle size smaller.
  externals: {
    jquery: 'jQuery',
    //gettext: 'gettext',
  },
}

/*
  If a project requires internationalisation, then include `gettext` in base.html
    via the Django JSi18n helper, and uncomment it from the 'externals' object above.
*/


if (process.env.NODE_ENV === 'development') {
  // Create JS source maps in the dev mode
  // See https://webpack.js.org/configuration/devtool/ for more options
  options['devtool'] = 'inline-source-map';
}

module.exports = options;
