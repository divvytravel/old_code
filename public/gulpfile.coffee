args   = require("optimist").argv
gulp = require "gulp"
gutil = require "gulp-util"
gulpif = require "gulp-if"
jade = require "gulp-jade"
stylus = require "gulp-stylus"
imagemin = require "gulp-imagemin"
uglify = require "gulp-uglify"
concat = require "gulp-concat"
scripts = require "./gulp/scripts"

isProduction = args.type is "production"
target = gutil.env.target or "./../divvy/static"

gulp.task "views", ->
  gulp.src("./src/views/**/**/*.jade")
    .pipe(jade())
    .pipe(gulp.dest("./../divvy/templates/views"))

gulp.task "ui-views", ->
  gulp.src("./src/views/**/*.jade")
    .pipe(jade())
    .pipe(gulp.dest("./../divvy/static"))

gulp.task "scripts", ->
  gulp.src("src/scripts/**/**/**/*.coffee", read: false )
    .pipe(scripts())
    .pipe(gulpif(isProduction, uglify outSourceMap: true))
    .pipe(gulp.dest("#{target}/js"))

gulp.task "styles", ->
  gulp.src("./src/styles/**/*.styl")
    .pipe(
      stylus(
        import:[],
        use: ["nib"], 
        paths:[]
      )
    )
    .pipe(concat("index.css"))
    .pipe(gulp.dest("#{target}/styles"))

gulp.task "imgs", ->
  gulp.src(["./src/img/**/**/*.png", "./src/img/**/**/*.jpg"])
        .pipe(imagemin())
        .pipe(gulp.dest("#{target}/img"))

gulp.task "watch", ->
  gulp.run "scripts"
  gulp.run "imgs"
  gulp.run "styles"
  gulp.run "views"
  gulp.run "ui-views"

  gulp.watch "./src/views/**/*.jade", ->
    gulp.run "views"
    gulp.run "ui-views"

  gulp.watch "./src/scripts/**/*.coffee", ->
    gulp.run "scripts"

  gulp.watch "./src/styles/**/*.styl", ->
    gulp.run "styles"

gulp.task "default", ["watch"]
gulp.task "build", ["views", "ui-views", "scripts", "styles", "imgs"]
