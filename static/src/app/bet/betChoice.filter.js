(function() {
    'use strict';
    angular
        .module('app.bet')
        .filter('betChoice', betChoice);
    
    betChoice.$inject = [];

    function betChoice() {
        return function(choice) {
            var return_value = choice;
            if (choice === '1') {
                return_value = '<i class="fa fa-arrow-up arr-up"></i>';
            } else if (choice === 'X') {
                return_value = '<i class="fa fa-circle arr-middle"></i>';
            } else if (choice === '2') {
                return_value = '<i class="fa fa-arrow-down arr-down"></i>';
            } else if (choice === 'N') {
                return_value = '<p class="arr-new">NEW</p>';
            }
            return return_value;
        };
    }
}());
