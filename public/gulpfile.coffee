gulp = require "gulp"
gutil = require "gulp-util"
jade = require "gulp-jade"
stylus = require "gulp-stylus"
imagemin = require "gulp-imagemin"
concat = require "gulp-concat"
scripts = require "./gulp/scripts"

target = gutil.env.target or "./../stormcrew/static"

gulp.task "views", ->
  gulp.src("./src/views/**/*.jade")
    .pipe(jade())
    .pipe(gulp.dest("./../stormcrew/templates/views"))

gulp.task "ui-views", ->
  gulp.src("./src/views/**/*.jade")
    .pipe(jade())
    .pipe(gulp.dest("./../stormcrew/static"))

gulp.task "scripts", ->
  gulp.src("src/scripts/**/*.coffee", read: false )
    .pipe(scripts())
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
