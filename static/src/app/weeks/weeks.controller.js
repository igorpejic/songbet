(function() {
    'use strict';
    angular
        .module('app.weeks')
        .controller('weeksController', weeksController);
    
    weeksController.$inject = ['weeksService', 'weekTopService'];

    function weeksController(weeksService, weekTopService) {
        var vm = this;
        vm.weeks = weeksService;
        vm.weekTop = weekTopService;
        var i = 0;
        angular.forEach(vm.weeks, function(obj) {
            obj["topSong"] = vm.weekTop[i];
            i++;
        });
    }
}());
