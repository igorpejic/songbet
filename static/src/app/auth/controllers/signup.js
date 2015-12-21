angular.module('app.auth')
.controller('SignupCtrl',
        ['$scope', '$rootScope', '$auth', '$state', '$resource', 'Notification', function($scope, $rootScope, $auth, $state, $resource, Notification) {
    var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
    $scope.signup = function() {
        $auth.signup({
            username: $scope.displayName,
            email: $scope.email,
            password: $scope.password
        }).then(function(response) {
            $auth.setToken(response);
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
                }
            );
            Notification('Sign up successful. Welcome to songbet!');
            $state.go('singleBet');
        })
        .catch(function(response) {
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
        }});
    };
    $scope.authenticate = function(provider) {
        $auth.authenticate(provider)
            .then(function() {
            socialUser.query().$promise.then(
                function success(data){
                    $rootScope.name = data.name;
                    $rootScope.bettingFunds = data.betting_funds;
                    Notification('Sign up successful. Welcome to songbet!');
                    $state.go('singleBet');
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
