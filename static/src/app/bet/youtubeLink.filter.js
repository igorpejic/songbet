(function() {
    'use strict';
    angular
        .module('app.bet')
        .filter('youtubeLink', youtubeLink);
    
    youtubeLink.$inject = [];

    function youtubeLink() {
        return function(videoId, type) {
            var return_value;
            if (type === 'video') {
                return_value = 'https://www.youtube.com/watch?v=' + videoId;
            } else if (type === 'thumbnail') {
                return_value = 'https://img.youtube.com/vi/' + videoId + '/default.jpg';
            }
            return return_value;
        };
    }
}());
