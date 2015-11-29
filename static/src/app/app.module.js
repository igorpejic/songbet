(function () {
    'use strict';

    angular.module('app', [
      'ngResource',
      'ngMessages',
      'satellizer',
      'ngCookies',
      'ngSanitize',
      'ui.router',
      'mgcrea.ngStrap',
      'blocks.router',
      'app.auth',
      'app.core',
      'app.bet',
      'app.leaderboard',
      'app.mybets',
      'ui-notification',
    ]).
        config(['NotificationProvider', function(NotificationProvider) {
            NotificationProvider.setOptions({
                positionY: 'bottom'
            });
        }
    ]).
        config(['$resourceProvider', function($resourceProvider){
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }
    ]).
        config(function($authProvider, $locationProvider) {
            var getCookie = function (name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            };
            $authProvider.loginUrl = '/api-token-auth/';
            $authProvider.signupUrl = '/api/register/';
            $authProvider.loginRedirect = '/bet';
            $authProvider.logoutRedirect = '/';
            $locationProvider.html5Mode(true);
            $locationProvider.hashPrefix('!');
            $authProvider.google({
                clientId:'609163425136-1i7b7jlr4j4hlqtnb1gk3al2kagavcjm.apps.googleusercontent.com',
                url: 'api/login/google-oauth2/',
                optionalUrlParams: ['display', 'state'],
                state: function() {
                    return getCookie('csrftoken');
                }
            });
            $authProvider.facebook({
                clientId: '1629513813961116',
                url: 'api/login/facebook/',
                scope: ['email'],
                state: function() {
                    return getCookie('csrftoken');
                }
            });
    });
})();
