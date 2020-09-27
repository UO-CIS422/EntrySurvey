// webpack.config.js
// from https://medium.com/the-node-js-collection/modern-javascript-explained-for-dinosaurs-f695e9747b70
module.exports = {
  mode: 'development',
  entry: './index.js',
  output: {
    filename: 'main.js',
    publicPath: 'dist'
  }
};