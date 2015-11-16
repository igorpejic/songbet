'use strict';

var betServices = angular.module('betServices', ['ngResource']);

betServices.factory('Song', ['$resource',
    function($resource) {
        return $resource('/bet/lastweek/', {}, {
            query: {method:'GET', isArray:true}
        });
    }]);

betServices.factory('History', ['$resource',
    function($resource) {
        return $resource('/bet/history/', {}, {
            query: {method:'GET', isArray:true}
        });
    }]);

betServices.factory('CreateBet', ['$resource', '$cookies',
    function($resource, $cookies) {
        var csrf_token = $cookies.get('csrftoken');
        return $resource('/bet/createbet/', {}, {
          save: {method:'POST', isArray:false, headers: {'X-CSRFToken': csrf_token}}
        });
    }]);

betServices.factory('AddBet', ['$resource', '$cookies',
    function($resource, $cookies) {
        var csrf_token = $cookies.get('csrftoken');
        return $resource('/bet/addbet/', {}, {
          save: {method:'POST', isArray:false, headers: {'X-CSRFToken': csrf_token}}
        });
    }]);

betServices.factory('Songs', ['$resource',
    function($resource) {
      return $resource('/bet/song/', {}, {
        query: {method:'GET', isArray:true}
      });
    }]);

betServices.factory('SongPositions', ['$resource',
    function($resource) {
      return $resource('/bet/position/:song_pk/', {}, {
        query: {method:'GET', isArray:true, params: {pk: '@song_pk'}}
      });
    }]);

betServices.factory('Week', ['$resource',
    function($resource) {
      return $resource('/bet/week/:week_pk/', {}, {
        query: {method:'GET', isArray:false, params: {pk: '@week_pk'}},
        list: {method:'GET', isArray:true}
      });
    }]);
