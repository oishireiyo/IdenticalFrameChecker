const HtmlWebpackPlugin = require('html-webpack-plugin')
const TailwindCSS = require('tailwindcss')
const path = require('path')

module.exports = {
  mode: 'development',
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'main.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
          },
        ],
      },
      {
        test: /\.(ts|tsx)$/,
        use: [
          {
            loader: 'babel-loader',
          },
          {
            loader: 'ts-loader',
            options: {
              configFile: path.resolve(__dirname, 'tsconfig.json'),
            },
          },
        ],
      },
      {
        test: /\.(css)$/,
        use: [
          // JSで読み込んだCSSを、HTMLに読み込ませるためのnpmパッケージ。
          // HTMLのstyleタグとして書き出される。
          {
            loader: 'style-loader',
          },
          // エントリーポイントのJavaScriptに、CSSを読み込ませるためのパッケージ。
          // 作成したCSSを、JSモジュールとして読み込ませる。
          {
            loader: 'css-loader',
          },
          // Tailwind css使用する場合は以下の設定が必要。
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  TailwindCSS,
                ],
              },
            },
          },
        ],
      },
    ],
  },
  devServer: {
    port: 3000,
    host: '127.0.0.1',
    static: {
      directory: path.join(__dirname, 'dist'),
    },
    open: true,
    hot: true,
    liveReload: true,
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
  },
  target: 'web',
  plugins: [
    // ベースとなるHTMLも一緒にバンドルするため。
    new HtmlWebpackPlugin({
      inject: 'body',
      filename: 'index.html',
      template: path.join(__dirname, 'src', 'index.html'),
      favicon: path.join(__dirname, 'assets', 'favicon.ico'),
    }),
  ],
}