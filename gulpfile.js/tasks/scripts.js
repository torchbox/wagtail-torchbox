var gulp         = require('gulp');
var gulpif       = require('gulp-if');
var jscs         = require('gulp-jscs');
var jshint       = require('gulp-jshint');
var argv         = require('yargs').argv;
var config       = require('../config').scripts;

gulp.task('jshint', function () {
    return gulp.src(config.src)
        .pipe(jshint())
        .pipe(jshint.reporter())
        .pipe(gulpif(argv.fail, jshint.reporter('fail')));
});

gulp.task('jscs', function () {
    return gulp.src(config.src)
        .pipe(jscs())
        .pipe(jscs.reporter())
        .pipe(gulpif(argv.fail, jscs.reporter('fail')));
});

gulp.task('scripts', function () {
    return gulp.src(config.src)
        .pipe(gulp.dest(config.dest));
});
