(function() {
    'use strict';
    angular
        .module('app.mybets')
        .controller('mybetsDetailController', mybetsDetailController);
    
    mybetsDetailController.$inject = ['mybetsDetailService', '$filter'];
    function mybetsDetailController(mybetsDetailService, $filter) {
        var vm = this;
        vm.mybet = mybetsDetailService;
        vm.totalOdds = totalOdds();

        function totalOdds() {
            var total = 0;
            angular.forEach(vm.mybet.betitem_set, function(value, key) {
                console.log('aaa');
                total += value.odd;
            });
            return $filter('number')(total, 2);
        }
    }

}());
