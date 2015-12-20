(function() {
    'use strict';

    angular
        .module('app.weeks')
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
                state: 'weeks',
                config: {
                    url: '/weeks',
                    templateUrl: '/static/src/app/weeks/weeks.html',
                    controller: 'weeksController',
                    resolve: {
                        weeksService: weeksService,
                        weekTopService: weekTopService
                    },
                    controllerAs: 'vm'
                }
            },
            {
                state: 'weeksDetail',
                config: {
                    url: '/weeks/:id',
                    templateUrl: '/static/src/app/weeks/weeksDetail.html',
                    controller: 'weeksDetailController',
                    resolve: {
                        weeksDetailService: weeksDetailService,
                        commentsResource: commentsResource
                    },
                    controllerAs: 'vm'
                }
            },
        ];
    }
    /* @ngInject */
    function weeksService(dataservice) {
        return dataservice.weeksService().query().$promise;
    }
    /* @ngInject */
    function weeksDetailService(dataservice, $stateParams) {
        return dataservice.weeksService().get({id: $stateParams.id}).$promise;
    }
    /* @ngInject */
    function commentsResource(dataservice) {
        return dataservice.commentsService();
    }
    /* @ngInject */
    function weekTopService(dataservice) {
          return dataservice.weekTopService().query().$promise;
    }
})();
