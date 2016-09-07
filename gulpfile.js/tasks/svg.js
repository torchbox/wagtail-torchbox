var gulp        = require('gulp');
var svgSprite   = require('gulp-svg-sprite');
var plumber     = require('gulp-plumber');
var config      = require('../config').svg;

gulp.task('svg-sprite', function () {
    gulp.src('**/*.svg', { cwd: config.src })
    .pipe(plumber())
    .pipe(svgSprite({
        shape: {
            dimension: {         // Set maximum dimensions
                maxWidth: 32,
                maxHeight: 32,
                precision: config.precision || 2,
            },
            transform: [{
                svgo: {
                    plugins: [{
                        cleanupIDs: true,
                        mergePaths: true,
                    }],
                },
            }]
        },
        svg: {                         // General options for created SVG files
            xmlDeclaration: false,                     // Add XML declaration to SVG sprite
            doctypeDeclaration: false,                     // Add DOCTYPE declaration to SVG sprite
            namespaceIDs: false,                     // Add namespace token to all IDs in SVG shapes
            dimensionAttributes: false,                      // Width and height attributes on the sprite
        },
        mode: {
            symbol: {
                render: {
                    scss: false,  // Activate CSS output (with default options)
                },
                sprite: '../' + config.spriteFilename || 'sprite.svg',
            }
        }
    }))
    .on('error', function (error) {
        console.log(error);
    })
    .pipe(gulp.dest('.', { cwd: config.dest }));
});
