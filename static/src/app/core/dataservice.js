angular
    .module('app.core')
    .factory('dataservice', dataservice);

dataservice.$inject = ['$resource', '$http', '$cookies'];

function dataservice($resource, $http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.get('csrftoken');
    return {
        lastWeekService: lastWeekService,
        addBetService: addBetService,
        leaderboardService: leaderboardService,
        mybetsService: mybetsService,
        weeksService: weeksService,
        commentsService: commentsService,
        weekTopService: weekTopService,
        contactService: contactService,
    };

    function lastWeekService() {
        return $resource('/api/lastweek/',
            null, null);
    }
    function addBetService() {
        return $resource('/api/bet/',
            null, null);
    }
    function leaderboardService() {
        return $resource('/api/leaderboard',
            null, null);
    }
    function mybetsService() {
        return $resource('/api/mybets/:id',
            null, null);
    }
    function weeksService() {
        return $resource('/api/weeks/:id',
            null, null);
    }
    function commentsService() {
        return $resource('/api/weeks/:weekId/positions/:position/comments/:id',
            null, null);
    }
    function weekTopService() {
        return $resource('/api/bestoftheweek/',
            null, null);
    }
    function contactService() {
        return $resource('/api/contact/',
            null, null);
    }
}
