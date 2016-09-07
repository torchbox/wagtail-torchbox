var gulp           = require('gulp');
var browserifyTask = require('./browserify');

gulp.task('build', function () {
    // Start browserify task with devMode off, to enabled uglifying etc
    return browserifyTask();
});
