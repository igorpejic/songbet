angular.module('app.auth')
.controller('SignupCtrl', function($scope, $rootScope, $alert, $auth, $state, $resource) {
    var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
    $scope.signup = function() {
        $auth.signup({
            username: $scope.displayName,
        email: $scope.email,
        password: $scope.password
        }).catch(function(response) {
            if (typeof response.data.message === 'object') {
                angular.forEach(response.data.message, function(message) {
                    $alert({
                        content: message[0],
                    animation: 'fadeZoomFadeDown',
                    type: 'material',
                    duration: 3
                    });
                });
                socialUser.query().$promise.then(
                    function success(data){
                        $rootScope.name = data.name;
                        $rootScope.bettingFunds = data.betting_funds;
                    }
                );
            } else {
                $alert({
                    content: response.data.message,
                    animation: 'fadeZoomFadeDown',
                    type: 'material',
                    duration: 3
                });
            }
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
