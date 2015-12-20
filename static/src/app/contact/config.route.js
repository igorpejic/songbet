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
                state: 'contact',
                config: {
                    url: '/contact',
                    templateUrl: '/static/src/app/contact/contact.html',
                    controller: 'contactController',
                    resolve: {
                        contactService: contactService
                    },
                    controllerAs: 'vm',
                }
            },
        ];
    }

    /* @ngInject */
    function contactService(dataservice) {
        return dataservice.contactService();
    }

})();
