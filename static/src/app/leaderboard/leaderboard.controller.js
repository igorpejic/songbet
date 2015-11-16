(function() {
    'use strict';
    angular
        .module('app.leaderboard')
        .controller('leaderboardController', leaderboardController);
    
    leaderboardController.$inject = ['leaderboardService'];

    function leaderboardController(leaderboardService) {
        var vm = this;
        vm.users = leaderboardService;
    }
}());
