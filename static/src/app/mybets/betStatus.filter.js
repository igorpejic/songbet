(function() {
    'use strict';
    angular
        .module('app.bet')
        .filter('betStatus', betStatus);
    
    betStatus.$inject = [];

    function betStatus() {
        return function(choice) {
            var return_value = choice;
            if (choice === 'False') {
                return_value = 'Lost';
            } else if (choice === 'True') {
                return_value = 'Won';
            }
            return return_value;
        };
    }
}());
