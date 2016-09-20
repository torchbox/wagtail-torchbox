var gulp     = require('gulp');
var config   = require('../config');

gulp.task('watch', function () {
    gulp.watch(config.sass.src, (function () {
        var arr = ['sass'];

        if (config.sass.liveLinting) {
            arr.push('sass-lint');
        }

        return arr;
    }()));

    gulp.watch(config.images.src, ['images']);

    gulp.watch(config.svg.src, ['svg-sprite']);

    gulp.watch(config.scripts.src, (function () {
        var arr = ['scripts'];

        if (config.scripts.liveLinting) {
            arr.push('jshint', 'jscs');
        }

        return arr;
    }()));

    gulp.watch(config.fonts.src, ['fonts']);
});
