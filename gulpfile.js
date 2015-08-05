var gulp = require('gulp');
var googlecdn = require('gulp-google-cdn');

gulp.task('default', function () {
    return gulp.src('templates/index.html')
        .pipe(googlecdn(require('./bower.json')))
        .pipe(gulp.dest('dist'));
});
