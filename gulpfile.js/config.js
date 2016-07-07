var src = 'tbx/core/static/torchbox/';
var dest = 'tbx/core/static';

module.exports = {
    dest: dest,
    images: {
        src: src + '/img/**',
        dest: dest + '/img',
    },
    svg: {
        src: src + '/img/sprite_src/**',
        dest: dest + '/img',
        precision: 2,
        spriteFilename: 'sprite.svg',
    },
    fonts: {
        src: src + '/fonts/**',
        dest: dest + '/fonts',
    },
    sass: {
        src: src + '/css/**/*.{sass,scss}',
        dest: dest + '/css',
        autoprefixer: {
            browsers: ['last 2 versions', 'ie 9-11'],
            cascade: false,
        },
        settings: {
            outputStyle: 'compressed',
        },
        // liveLinting: true,
    },
    scripts: {
        src: src + '/js/**',
        dest: dest + '/js',
        // liveLinting: true,
    },
    browserify: {
        // A separate bundle will be generated for each
        // object in the array below
        bundleConfigs: [

            // Uncomment me to add a file for Babel/Browserify to transpile.
            // {
            //     entries: src + '/js/main.js',
            //     transform: [
            //         ['babelify', { presets: ['es2015'] }],
            //     ],
            //     dest: dest + '/js/',
            //     outputName: 'main.bundled.js',
            //     cache: {},
            //     packageCache: {},
            //     fullPaths: false,
            // },
        ],
    },
};
