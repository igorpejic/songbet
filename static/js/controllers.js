'use strict';

var betControllers = angular.module('betControllers', ['ngCookies']);

betControllers.controller('lastWeekController', ['$scope', '$cookies', '$cookieStore', '$location', 'Song', 'CreateBet', 'AddBet', 'History',
    function($scope, $cookies, $cookieStore, $location, Song, CreateBet, AddBet, History) {
        $scope.possible_bets = [];
        $scope.data = Song.query();
        $scope.hidden = [];
        $scope.data.$promise.then(function (result) { 
          $scope.data = result;
        });
        $scope.addBet = function(new_song, choice){
            if ($scope.possible_bets.length > 9)
                return;

            for(var i=0;i<$scope.possible_bets.length;i++){
                var temp = $scope.possible_bets[i];
                if(angular.equals(temp.song, new_song)){
                  return;
                }
            }
            var possible_bet = {};
            possible_bet.song = new_song;
            possible_bet.choice = choice;
            $scope.possible_bets.push(possible_bet);
            $scope.hidden[new_song.position] = 1;
            console.log($scope.hidden);
        };

        $scope.removeBet = function(bet, index) {
            $scope.hidden[bet.song.position] = 0;
            $scope.possible_bets.splice(index, 1);
        };

        $scope.choose = function(row, choice) {
            var index = row.rowIndex;
            $scope.possible_bets[index].choice = choice;
        };

        $scope.submit_bet = function() {
            var csrf_token = $cookies.get('csrftoken');
            var new_bet = {bet_type: 3};  
            CreateBet.save(new_bet).$promise.then(
                function(success_data){
                  toastr.success('New bet created.');
                  angular.forEach($scope.possible_bets, function(value, key) {
                    var new_bet = {};
                    new_bet['bet_id'] = success_data.bet_id;
                    new_bet['song'] = value.song.song.name;
                    new_bet['choice'] = value.choice;
                    AddBet.save(new_bet);
                  });
                $location.path("/10bets");
                }
            )
        };

        $scope.go_song_view = function(path) {
            $location.path("/songs");
        };
    }]);



betControllers.controller('songsController', ['$scope', '$location', 'Songs',
    function($scope, $location, Songs) {
        $scope.songs = Songs.query();
        $scope.go_positions_view = function(song_id) {
            $location.path("/positions/" + song_id);
        };
}]);

betControllers.controller('songPositionsController', ['$scope', '$routeParams', '$location', 'SongPositions',
    function($scope, $routeParams, $location, SongPositions) {
        $scope.positions = SongPositions.query({song_pk: $routeParams.song_pk});

        $scope.song_name = $routeParams.song_name;

        $scope.go_song_view = function(path) {
            $location.path("/songs");
        };

        $scope.go_week_view = function(week_pk) {
            $location.path("/week/" + week_pk);
        };
}]);

betControllers.controller('weekController', ['$scope', '$routeParams', '$location', 'Week',
    function($scope, $routeParams, $location, Week) {
        $scope.week  = Week.query({week_pk: $routeParams.week_pk});

        $scope.go_positions_view = function(song_id) {
            $location.path("/positions/" + song_id);
        };
}]);

betControllers.controller('weeksController', ['$scope', '$routeParams', '$location', 'Week',
    function($scope, $routeParams, $location, Week) {
        $scope.weeks  = Week.list();
        $scope.go_week_view = function(week_pk) {
            $location.path("/week/" + week_pk);
        };

}]);
betControllers.controller('loginCtrl', ['$scope', '$auth', function($scope, $auth) {
    $scope.authenticate = function(provider) {
      $auth.authenticate(provider);
    };

  }]);
