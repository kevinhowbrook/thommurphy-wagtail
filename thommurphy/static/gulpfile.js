var sassOptions = {
  errLogToConsole: true,
  outputStyle: 'expanded'
};
var concat = require('gulp-concat');
var minify = require('gulp-minify');

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifyCss = require('gulp-minify-css');
var plugins = require('gulp-load-plugins')({
  rename: {
    'gulp-live-server': 'serve'
  }
});

// ... variables
var autoprefixerOptions = {
  browsers: ['last 2 versions', '> 5%', 'Firefox ESR']
};

var allsass = './scss/*.scss';
var output = 'css';

gulp.task('minify-css', function () {
  return gulp.src('./css/*.css')
      .pipe(minifyCss({compatibility: 'ie8'}))
      .pipe(gulp.dest('dist'));
});

gulp.task('sass', function () {
  return gulp
  // Find all `.scss` files from the `stylesheets/` folder
      .src([
        'node_modules/include-media/dist/_include-media.scss',
        'node_modules/owl.carousel/dist/assets/owl.carousel.min.css',
        'node_modules/owl.carousel/dist/assets/owl.theme.default.min.css',
        'node_modules/chota/src/_*.css',
        allsass])
      .pipe(concat('main.css'))
      // Run Sass on those files
      .pipe(sass({outputStyle: 'minifyed'}))
      // Write the resulting CSS in the output folder
      .pipe(sass(sassOptions).on('error', sass.logError))
      .pipe(autoprefixer(autoprefixerOptions))
      .pipe(minifyCss())

      .pipe(gulp.dest(output))
      .pipe(plugins.livereload());

});


gulp.task('watch', function () {

  return gulp
  // Watch the input folder for change,
  // and run `sass` task when something happens
      .watch(allsass, ['sass'])
      // When there is a change,
      // log a message in the console
      .on('change', function (event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
      });
});
gulp.task('default', ['sass'], function () {
  plugins.livereload.listen();
  gulp.watch(['scss/**/*.scss'], ['sass']);
});

//js
gulp.task('js', function () {
  return gulp
      .src([
        'node_modules/imagesloaded/imagesloaded.pkgd.min.js',
        'node_modules/owl.carousel/dist/owl.carousel.min.js',
        'node_modules/masonry-layout/dist/masonry.pkgd.min.js',
        'node_modules/imagesloaded/imagesloaded.pkgd.min.js',
        './js/thommurphy.js'
      ])
      .pipe(concat('all.js'))

      .pipe(minify({
        ext: {
          src: '-debug.js',
          min: '.js'
        },
      }))
      .pipe(gulp.dest('js'));
});
