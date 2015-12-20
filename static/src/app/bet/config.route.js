(function() {
    'use strict';

    angular
        .module('app.bet')
        .run(appRun);

    //appRun.$inject = ['routehelper'];

    /* @ngInject */
    function appRun(routerHelper, $rootScope, $state) {
        routerHelper.configureStates(getStates());
        //debugging
        $rootScope.$on("$stateChangeError", console.log.bind(console));
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

    /* @ngInject */
    function lastWeekPrepService(dataservice) {
        return dataservice.lastWeekService().query().$promise;
    }
    /* @ngInject */
    function addBetService(dataservice) {
        return dataservice.addBetService();
    }
})();
