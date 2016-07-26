var gulp         = require('gulp');
var gulpif       = require('gulp-if');
var sass         = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var notify       = require('gulp-notify');
var scsslint     = require('gulp-scss-lint');
var cache        = require('gulp-cached');
var argv         = require('yargs').argv;
var config       = require('../config').sass;

gulp.task('sass-lint', function () {
    return gulp.src(config.src)
        .pipe(cache('scsslint'))
        .pipe(scsslint({
            maxBuffer: 400 * 1024,
        }))
        .pipe(gulpif(argv.fail, scsslint.failReporter()));
});

gulp.task('sass', function () {
    return gulp.src(config.src)
        .pipe(sass(config.settings)
            .on('error', notify.onError({
                title: 'SASS compilation error',
                message: '<%= error.message %>',
                time: 10000,
            }))
        )
        .pipe(autoprefixer(config.autoprefixer))
        .pipe(gulp.dest(config.dest));
});
