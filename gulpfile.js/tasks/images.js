var changed    = require('gulp-changed');
var gulp       = require('gulp');
var imagemin   = require('gulp-imagemin');
var imageminAdvpng = require('imagemin-advpng');
var imageminPngcrush = require('imagemin-pngcrush');
var config     = require('../config').images;

gulp.task('images', function () {
    return gulp.src(config.src)
        .pipe(changed(config.dest)) // Ignore unchanged files
        .pipe(gulp.dest(config.dest));
});

gulp.task('images:optimise', function () {
    return gulp.src(config.src)
        .pipe(imagemin({
            optimizationLevel: 4,
            progressive: true,
            svgoPlugins: [
                {
                    removeViewBox: false,
                },
            ],
            use: [
                imageminAdvpng({ optimizationLevel: 4 }),
                imageminPngcrush({ reduce: true }),
            ],
        })) // Optimize
        .pipe(gulp.dest(config.dest));
});
