angular.module('app.auth')
  .controller('LoginCtrl', function($scope, $rootScope, $alert, $auth, $state, $resource, Notification) {
    var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
    $scope.login = function() {
      $auth.login({ username: $scope.email, password: $scope.password })
        .then(function() {
          $alert({
            content: 'You have successfully logged in',
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 3
          });
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
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
                $alert({
                    content: 'You have successfully logged in',
                    animation: 'fadeZoomFadeDown',
                    type: 'material',
                    duration: 3
                });
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
                }
            );
        });
    };
  });
