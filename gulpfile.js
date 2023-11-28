const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const browserSync = require('browser-sync').create();
const { spawn } = require('child_process');

// Define paths for the assets
const paths = {
    scss: 'src/assets/scss/**/*.scss',
    js: 'src/assets/js/**/*.js',
    fonts: 'src/assets/fonts/**/*',
};

// Reference to the Django server process
let djangoProcess = null;

// Function to start the Django development server
function djangoServer() {
    const pythonExecutable = 'python'; // or 'python3' if that's your environment
    djangoProcess = spawn(pythonExecutable, ['manage.py', 'runserver'], { stdio: 'inherit' });
}

// BrowserSync Task - to reload the browser on file changes
function browserSyncTask() {
    browserSync.init({
        proxy: 'localhost:8000', // Ensure this matches your Django server address
        port: 3000, // BrowserSync port
        open: true, // Set to false if you don't want the browser to open automatically
        notify: false
    });
}

// SCSS Task - Compile SASS files into CSS
function scssTask() {
    return gulp.src(paths.scss)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('static/assets/css'))
        .pipe(browserSync.stream());
}

// Font Task - Copy fonts
function fontTask() {
    return gulp.src(paths.fonts)
        .pipe(gulp.dest('static/assets/fonts'));
}

// JavaScript Task - Copy JS files
function jsTask() {
    return gulp.src(paths.js)
        .pipe(gulp.dest('static/assets/js'))
        .pipe(browserSync.stream());
}

// Watch Task - to watch for file changes
function watchTask() {
    gulp.watch(paths.scss, scssTask);
    gulp.watch(paths.fonts, fontTask);
    gulp.watch(paths.js, jsTask);
    gulp.watch(['**/*.html', '**/*.py']).on('change', browserSync.reload);
}
// Handle Gulp Exit
process.on('exit', () => {
    if (djangoProcess) {
        djangoProcess.kill();
    }
});

// Default Gulp task
exports.default = gulp.parallel(
    scssTask, 
    djangoServer,
    browserSyncTask,
    watchTask
);
exports.scssTask = scssTask;