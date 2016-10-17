var browserify   = require('browserify');
var watchify     = require('watchify');
var mergeStream  = require('merge-stream');
var gulp         = require('gulp');
var source       = require('vinyl-source-stream');
var config       = require('../config').browserify;
var _            = require('lodash');
var gutil        = require('gulp-util');
var exorcist     = require('exorcist');

var browserifyTask = function (devMode) {
    var browserifyThis = function (bundleConfig) {
        // 
        // if (devMode) {
        //     // Add debug (sourcemaps) option
        //     _.extend(bundleConfig, { debug: true });
        // }

        var bundler = browserify(bundleConfig);

        var runBundle = function () {

            return bundler.bundle()
                .on('error', function (err) {
                    // Report compile errors
                    gutil.log('Browserify error:', err);
                    this.emit('end');
                })
                .pipe(source(bundleConfig.outputName))
                .pipe(gulp.dest(bundleConfig.dest));
        };

        if (devMode) {
            bundler = watchify(bundler);
            bundler.on('update', runBundle);
        } else {
            bundler.plugin('minifyify', { map: false, uglify: true });
        }

        return runBundle();
    };

    // Start bundling with Browserify for each bundleConfig specified
    return mergeStream.apply(gulp, _.map(config.bundleConfigs, browserifyThis));
};

// Exporting the task so we can call it directly in our watch task, with the 'devMode' option
module.exports = browserifyTask;
