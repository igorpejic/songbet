(function() {
    'use strict';

    angular
        .module('app.mybets')
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
                state: 'mybets',
                config: {
                    url: '/mybets',
                    templateUrl: '/static/src/app/mybets/mybets.html',
                    controller: 'mybetsController',
                    resolve: {
                        mybetsService: mybetsService
                    },
                    controllerAs: 'vm'
                }
            },
            {
                state: 'mybetsDetail',
                config: {
                    url: '/mybets/:id',
                    templateUrl: '/static/src/app/mybets/mybetsDetail.html',
                    controller: 'mybetsDetailController',
                    resolve: {
                        mybetsDetailService: mybetsDetailService
                    },
                    controllerAs: 'vm'
                }
            },
        ];
    }
    function mybetsService(dataservice) {
        return dataservice.mybetsService().query().$promise;
    }
    function mybetsDetailService(dataservice, $stateParams) {
        return dataservice.mybetsService().get({id: $stateParams.id}).$promise;
    }
})();
