(function() {
    'use strict';

    angular
        .module('app.bet')
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
                state: 'about',
                config: {
                    url: '/about',
                    templateUrl: '/static/src/app/about/about.html',
                }
            },
            {
                state: 'faq',
                config: {
                    url: '/faq',
                    templateUrl: '/static/src/app/about/faq.html',
                }
            },
        ];
    }
})();
