var gulp = require('gulp'),
    gp_concat = require('gulp-concat'),
    gp_rename = require('gulp-rename'),
    gp_uglify = require('gulp-uglify');
    gp_sourcemaps = require('gulp-sourcemaps');
    gp_expect = require('gulp-expect-file');
    ngAnnotate = require('gulp-ng-annotate');


    /*
    'src/app/weeks/weeks.router.js',
    'src/app/weeks/weeks.module.js',
    'src/app/weeks/weeks.controller.js',
    'src/app/weeks/config.route.js',
    'src/app/weeks/weeksDetail.controller.js',
    */
var source = [
    'bower_components/jquery/dist/jquery.js',
    'bower_components/angular/angular.js',
    'bower_components/bootstrap/dist/js/bootstrap.js',
    'bower_components/angular-resource/angular-resource.js',
    'bower_components/angular-cookies/angular-cookies.js',
    'bower_components/angular-sanitize/angular-sanitize.js',
    'bower_components/angular-route/angular-route.js',
    'bower_components/angular-strap/dist/angular-strap.js',
    'bower_components/angular-strap/dist/angular-strap.tpl.js',
    'bower_components/satellizer/satellizer.min.js',
    'bower_components/angular-messages/angular-messages.min.js',
    'bower_components/angular-ui-router/release/angular-ui-router.min.js',
    'bower_components/angular-animate/angular-animate.min.js',
    'bower_components/angular-ui-notification/dist/angular-ui-notification.min.js',

    'src/app/app.module.js',
    'src/app/blocks/router/router.module.js',
    'src/app/blocks/router/routerHelperProvider.js',

    'src/app/core/core.module.js',
    'src/app/core/dataservice.js',
    'src/app/core/config.js',

    'src/app/bet/bet.router.js',
    'src/app/bet/bet.module.js',
    'src/app/bet/singleBet.controller.js',
    'src/app/bet/config.route.js',
    'src/app/bet/betChoice.filter.js',
    'src/app/bet/youtubeLink.filter.js',

    'src/app/leaderboard/leaderboard.router.js',
    'src/app/leaderboard/leaderboard.module.js',
    'src/app/leaderboard/leaderboard.controller.js',
    'src/app/leaderboard/config.route.js',

    'src/app/mybets/mybets.router.js',
    'src/app/mybets/mybets.module.js',
    'src/app/mybets/mybets.controller.js',
    'src/app/mybets/config.route.js',
    'src/app/mybets/mybetsDetail.controller.js',
    'src/app/mybets/betStatus.filter.js',


    'src/app/auth/auth.router.js',
    'src/app/auth/auth.module.js',
    'src/app/auth/directives/passwordStrength.js',
    'src/app/auth/controllers/navbar.js',
    'src/app/auth/controllers/login.js',
    'src/app/auth/controllers/signup.js',
    'src/app/auth/controllers/logout.js',
    'src/app/auth/controllers/profile.js',
    'src/app/auth/services/account.js',
    'src/app/auth/config.route.js',
    'src/app/about/about.module.js',
    'src/app/about/about.router.js',
    'src/app/about/config.route.js',
    'src/app/contact/contact.module.js',
    'src/app/contact/contact.router.js',
    'src/app/contact/config.route.js',
    'src/app/contact/contact.controller.js',
];


gulp.task('js-fef', function(){
    return gulp.src(source)
        .pipe(gp_expect(source))
        .pipe(ngAnnotate())
        .pipe(gp_sourcemaps.init())
        .pipe(gp_concat('concat.js'))
        .pipe(gulp.dest('dist'))
        .pipe(gp_rename('uglify.js'))
        .pipe(gp_uglify())
        .pipe(gp_sourcemaps.write('./'))
        .pipe(gulp.dest('dist'));
});

gulp.task('default', ['js-fef'], function(){});
