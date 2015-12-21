angular.module('app.auth')
  .controller('LoginCtrl',
          ['$scope', '$rootScope', '$auth', '$state', '$resource', 'Notification', function($scope, $rootScope, $auth, $state, $resource, Notification) {
    var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
    $scope.login = function() {
      $auth.login({ username: $scope.email, password: $scope.password })
        .then(function() {
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
                    $state.go('singleBet');
                    Notification('Welcome back ' + data.name  + '!');
                }
            );
        })
        .catch(function(response) {
            if (response.status === 400) {
                Notification.error("Incorrect password.");
            }}
            );
    };

    $scope.authenticate = function(provider) {
        $auth.authenticate(provider)
            .then(function() {
                socialUser.query().$promise.then(
                    function success(data){
                        $rootScope.name = data.name;
                        $rootScope.bettingFunds = data.betting_funds;
                        $state.go('singleBet');
                        Notification('Welcome back ' + data.name  + '!');
                    }
                    );
            });
        };

    var guestUser = $resource('/api/guest-login/', null, {'query': {method: 'POST', isArray:false}});
    $scope.guestLogin = function() {
        guestUser.save().$promise.then(
            function success(response) {
                console.log(response);
                $auth.setToken(response.token);
                $rootScope.name = response.name;
                $rootScope.bettingFunds = response.betting_funds;
                Notification('Welcome! Explore using your guest account.');
                $state.go('singleBet');
            }
        );
    };
  }]);
