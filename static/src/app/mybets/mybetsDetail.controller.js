(function() {
    'use strict';
    angular
        .module('app.mybets')
        .controller('mybetsDetailController', mybetsDetailController);
    
    mybetsDetailController.$inject = ['mybetsDetailService'];
    function mybetsDetailController(mybetsDetailService) {
        var vm = this;
        vm.mybet = mybetsDetailService;
    }

}());
