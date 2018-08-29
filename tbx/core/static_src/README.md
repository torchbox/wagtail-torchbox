# Front end tooling

This set of tooling should form the basis for any new wagtail projects. It can also be used for custom django builds - simply copy the `static_src` directory from here to your build.

## What's required

When developing, it's faster to run the tooling from your host machine, although it is also possible to run it in the vm.

If you want to run it from your host machine, ensure you have the lastest version of node installed

* [Node.js](http://nodejs.org)


## Setting up a new project from the wagtail-kit tooling

* Note that due to differences in the installation process for the vm and the host machine, it may be necessary to delete the `node_modules` directory if this was previously created by `vagrant provision` before running the next command on your host machine.
* From inside the `static_src` directory, run `npm install`.
* This will create:
    - a set of files inside `node_modules` which should be excluded from the repo
    - a `package-lock.json` file, which will record the exact version of node pacakages used.
* Ensure you commit the package-lock.json file to your repo.
* It may be advisable to upgrade the packages to their latest versions (see Using npm below)

Note that for easier maintenance the package-lock.json file is not committed to the `wagtail-kit` repo, but it *should* be committed in any new project created from `wagtail-kit` to ensure consistency between the packages used when different developers are working on the same project.

## What's included

* [SASS](http://sass-lang.com/) CSS with [auto-prefixing](https://github.com/postcss/autoprefixer).
* [Browsersync](https://www.browsersync.io) for autoreloading.
* [Webpack](https://webpack.js.org/) and [Babel](https://babeljs.io) for ES2015 support with module loading.
* Consideration for images, currently copying the directory only - to avoid slowdowns and non-essential dependancies. We encourage using SVG for UI vectors and pre-optimised UI photograph assets.
* [Build commands](#build-scripts) for generating testable or deployable assets only
* Sass linting with `sass-lint`
* JS linting with `eslint`
* React support


## Developing with it

* To start the development environment, run `npm start` - to stop this process press `ctrl + c`.
* This will start Browsersync and make the project available at `http://localhost:3000/html/`. If another process is using this port, check terminal for an updated URL. You can change this configuation by modifying the `browsersync.config.js` file, documented here https://www.browsersync.io/docs/options.
* Source files for developing your project are in `static_src` and the distribution folder for the compiled assets is `static_compiled`. Don't make direct changes to the `static_compiled` directory as they will be overwritten.

Note that the build, debug and start commands will all rebuild node-sass before running the watch commands. This is because of differences between the way node-sass is installed when running vagrant up and when running `npm install` on the host machine.

### Using npm

* Install all packages from `package.json`: `npm install`
* Add new packages that are only required for development, e.g. tooling: `npm install --save-dev package_name` (this will add it to `package.json` and `package-lock.json` too)
* Add new packages required in production, e.g. react: `npm install --save-prod package_name`
* To upgrade packages run `npm update package_name` or `npm update` to update them all.

## Deploying it

### Build scripts

To only build assets for either development or production you can use

 * `npm run build` To build development assets
 * `npm run build:prod` To build assets with minification and vendor prefixes

### Debug script

To test production, minified and vendor prefixed assets you can use

 * `npm run debug` To develop with a simple http server, no browsersync and production assets


## React support
If your project requires react support:

* `mv react.babelrc .babelrc`
* `mv react.eslintrc .eslintrc`
* `mv react.package.json package.json`
* `mv react.webpack.config.js webpack.config.js`
* `npm install`

You can test that compilation of react is working by uncommenting the relevant lines in `javascript/main.js` and `javascript/components/test-react.js`

Note that react is installed as a dependency and imported via main.js.

## Using and updating the tooling in wagtail-kit

You can remove this section from the readme file for new builds.

To run the tooling inside the `wagtail-kit` build, ensure that you run `npm install` from insdie the built image, i.e. `wagtail-kit/built_image/ck_repo_name/ck_repo_name/static_src`

The easiest way to install new packages is to run `npm install --save-dev package_name` in `wagtail-kit/built_image/ck_repo_name/ck_repo_name/static_src`, but then copy the resultant changes to `package.json` over to `/wagtail-kit/{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}/static_src`.

Changes to the config files can be made directly in `/wagtail-kit/{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}/static_src` If you make updates to either the config files or package.json ensure you update both the default versions and the react verisons.

## Further details of the packages included
- **autoprefixer** - adds vendor prefixes as necessary for the browsers defined in `browserslist` in the npm config https://www.npmjs.com/package/autoprefixer
- **babel-core** - transpiler for es6 / react https://www.npmjs.com/package/babel-core
- **babel-eslint** - add-on for extra linting of experimental features (may not be necessary for all projects) https://www.npmjs.com/package/babel-eslint
- **babel-loader** - use babel with webpack - https://www.npmjs.com/package/babel-loader
- **babel-plugin-external-helpers** - handles helper functions nicely for multiple files (may not be necessary for all projects) https://www.npmjs.com/package/babel-plugin-external-helpers, https://babeljs.io/docs/plugins/external-helpers/
- **babel-preset-env** - babel preset for the latest version of es6, es2015 etc. https://www.npmjs.com/package/babel-preset-env https://babeljs.io/env/ https://babeljs.io/docs/plugins/
- **browser-sync** - for automatic reloading of your browser when changes are made to CSS / JS files https://www.npmjs.com/package/browser-sync
- **eslint** - lint your javascript https://www.npmjs.com/package/eslint
- **node-sass** - compiles Sass to CSS https://www.npmjs.com/package/node-sass
- **npm-run-all** - run more than one npm script concurrently - used by some of our npm scripts https://www.npmjs.com/package/npm-run-all
- **onchange** - watches for changes in a set of files - used by our watch scripts https://www.npmjs.com/package/onchange
- **postcss-cli** - required by `autoprefixer` - https://www.npmjs.com/package/postcss-cli
- **postcss-custom-properties** - polyfill for CSS custom properties - https://www.npmjs.com/package/postcss-custom-properties
- **sass-lint** - Linting for Sass files - https://www.npmjs.com/package/sass-lint
- **webpack** - Bundler for js files (can do much more too) - https://www.npmjs.com/package/webpack https://webpack.js.org/concepts/
- **webpack-cli** - The webpack command calls this behind the scenese (as of webpack v 4) https://www.npmjs.com/package/webpack-cli

## React specific packages
- **babel-polyfill** - IE11 fallbacks for some js functions https://www.npmjs.com/package/babel-polyfill
- **babel-preset-react** - babel preset for react. https://www.npmjs.com/package/babel-preset-react https://babeljs.io/env/ https://babeljs.io/docs/plugins/
- **eslint-plugin-react** - linting for react and jsx https://www.npmjs.com/package/eslint-plugin-react





