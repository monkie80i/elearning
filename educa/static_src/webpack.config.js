const path = require('path');

module.exports = {
  entry: './node_modules/jquery/dist/jquery.js',
  output: {
    path: path.resolve(__dirname, '../static/js'),
    filename: 'my-first-webpack.bundle.js',
  },
};