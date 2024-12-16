const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  mode: "development",
  entry: "./src/app/index.tsx",
  devtool: "source-map",
  devServer: {
    static: {
      directory: path.join(__dirname, "src", "assets"),
      publicPath: "/assets",
    },
    historyApiFallback: true,
    proxy: [
      {
        context: ["/api"],
        target: "http://localhost:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/api": "",
        },
        logLevel: "debug",
      },
    ],
  },
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist"),
    publicPath: "/",
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js", ".css"],
  },
  module: {
    rules: [
      // load and compile ts and tsx files
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      // load and compile css files
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
      },
      // load and compile asset files which is optional since assets folder is the static folder
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        use: ["file-loader?name=[name].[ext]"],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./src/app/index.html",
    }),
    new webpack.DefinePlugin({
      "process.env.PUBLIC_URL": JSON.stringify("/"),
    }),
    new MiniCssExtractPlugin({
      filename: "[name].css",
      chunkFilename: "[id].css",
    }),
  ],
};
