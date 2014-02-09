through = require "through2"
gutil = require "gulp-util"
browserify = require "browserify"
shim = require "browserify-shim"
File = gutil.File
path = require "path"

pkg = require "./../package.json"

module.exports = ->
  bundle = shim browserify(), pkg.shims

  bundle.require "./config.json", expose: "config"

  search = (file, encoding, callback) ->
    filePath = file.relative.split("/")
    filename = filePath[filePath.length - 1]
    bundle.require require.resolve(file.path), expose: filename.split(".")[0]
    callback()

  transform = ->
    bundle.transform "coffeeify"
    bundle.transform "reactify"

    bundle.bundle (err, data) =>
      console.log err if err

      result = new File
        base: __dirname
        cwd: __dirname
        path: "#{__dirname}/index.js"
        contents: new Buffer data

      @push result
      @emit "end"

  through.obj search, transform
