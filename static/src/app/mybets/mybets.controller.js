(function() {
    'use strict';
    angular
        .module('app.mybets')
        .controller('mybetsController', mybetsController);
    
    mybetsController.$inject = ['mybetsService'];

    function mybetsController(mybetsService) {
        var vm = this;
        vm.mybets = mybetsService;
    }
}());
