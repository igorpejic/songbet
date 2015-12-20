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
  }]);
