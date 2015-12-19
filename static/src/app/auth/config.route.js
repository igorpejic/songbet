(function() {
    'use strict';

    angular
        .module('app.auth')
        .run(appRun);

    //appRun.$inject = ['satellizer'];

    /* @ngInject */
    function appRun(routerHelper, $rootScope) {
        routerHelper.configureStates(getStates());
        $rootScope.$on("$stateChangeError", console.log.bind(console));
    }

    function getStates() {
        return [
            {
                state: 'login',
                config: {
                    url: '/login',
                    templateUrl: '/static/src/app/auth/views/login.html',
                    controller: 'LoginCtrl',
                }
            },
            {
                state: 'signup',
                config: {
                    url: '/',
                    templateUrl: '/static/src/app/auth/views/signup.html',
                    controller: 'SignupCtrl',
                }
            },
            {
                state: 'logout',
                config: {
                    url: '/logout',
                    templateUrl: '/static/src/app/auth/views/logout.html',
                    controller: 'LogoutCtrl',
                }
            },
            {
                state: 'profile',
                config: {
                    url: '/profile',
                    templateUrl: '/static/src/app/auth/views/profile.html',
                    controller: 'ProfileCtrl',
                    resolve: {
                        authenticated: function($q, $location, $auth) {
                            var deferred = $q.defer();

                            if (!$auth.isAuthenticated()) {
                                $location.path('/login');
                                  } else {
                                deferred.resolve();
                              }

                          return deferred.promise;
                        }
                    }
                }
            },
        ];
    }
})();
