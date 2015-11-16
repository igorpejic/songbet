(function() {
    'use strict';
    angular
        .module('app.weeks')
        .controller('weeksDetailController', weeksDetailController);
    
    weeksDetailController.$inject = ['weeksDetailService', 
                                     'commentsResource',
                                    ];
    function weeksDetailController(
        weeksDetailService,
        commentsResource) {
        var vm = this;
        vm.week = weeksDetailService;
        vm.hoverIn = hoverIn;
        vm.hoverOut = hoverOut;
        vm.comment = comment;

        function hoverIn (song) {
            song.commentFocus = true;
        }

        function hoverOut (song) {
            song.commentFocus = false;
        }

        function comment(week, song, songComment) { 
            commentsResource.save({weekId: week.id, position: song.position}, {comment: songComment}).$promise.then(
                function success(){
                    console.log('Success.');
                }
            );
        }
    }
}());
