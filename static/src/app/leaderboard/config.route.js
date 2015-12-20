(function() {
    'use strict';

    angular
        .module('app.leaderboard')
        .run(appRun);

    //appRun.$inject = ['routehelper'];

    /* @ngInject */
    function appRun(routerHelper, $rootScope) {
        routerHelper.configureStates(getStates());
        $rootScope.$on("$stateChangeError", console.log.bind(console));
    }

    function getStates() {
        return [
            {
                state: 'leaderboard',
                config: {
                    url: '/leaderboard',
                    templateUrl: '/static/src/app/leaderboard/leaderboard.html',
                    controller: 'leaderboardController',
                    resolve: {
                        leaderboardService: leaderboardService
                    },
                    controllerAs: 'vm'
                }
            },
        ];
    }

    /* @ngInject */
    function leaderboardService(dataservice) {
        return dataservice.leaderboardService().get().$promise;
    }
})();
