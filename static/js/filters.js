angular.module('betFilters', []).filter('checkmark', function() {
    return function(input){
        return input ? '\u2713' : '\u2718';
    };
});

angular.module('betFilters', []).filter('bet_type', function() {
    return function(input){
        if (input == 1) return 'Top10';
        if (input == 2) return 'Top20';
        if (input == 3) return '1x2';
    };
});
