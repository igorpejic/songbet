(function() {
    'use strict';

    angular
        .module('app.bet')
        .run(appRun);

    //appRun.$inject = ['routehelper'];

    /* @ngInject */
    function appRun(routerHelper, $rootScope, $state) {
        routerHelper.configureStates(getStates());
        $rootScope.$on("$stateChangeError", function(event){
           event.preventDefault();
           $state.go('signup');
        });
    }

    function getStates() {
        return [
            {
                state: 'singleBet',
                config: {
                    url: '/bet',
                    templateUrl: '/static/src/app/bet/singleBet.html',
                    controller: 'singleBetController',
                    resolve: {
                        lastWeekPrepService: lastWeekPrepService,
                        addBetService: addBetService
                    },
                    controllerAs: 'vm',
                }
            },
        ];
    }

    function lastWeekPrepService(dataservice) {
        return dataservice.lastWeekService().query().$promise;
    }
    function addBetService(dataservice) {
        return dataservice.addBetService();
    }
})();
