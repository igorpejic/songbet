angular.module('app.auth')
.controller('SignupCtrl', function($scope, $rootScope, $alert, $auth, $state, $resource, Notification) {
    var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
    $scope.signup = function() {
        $auth.signup({
            username: $scope.displayName,
        email: $scope.email,
        password: $scope.password
        }).catch(function(response) {
            if (response.status === 400) {
                angular.forEach(response.data, function(value, key) {
                    if (key === "username") {
                        Notification.error("Please choose a different username.");
                    }
                    if (key === "email") {
                        Notification.error("Enter a valid email address.");
                    }
                    if (key === "error") {
                        Notification.error("Please choose a different email address.");
                    }
                });
        }}).then(function() {
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
                }
            );
        });
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
