(function() {
angular
    .module('app.auth')
    .controller('NavbarCtrl', NavbarCtrl);

NavbarCtrl.$inject = ['$scope', '$rootScope', '$auth', '$resource'];

function NavbarCtrl($scope, $rootScope, $auth, $resource) {
    $rootScope.name = '';
    $rootScope.bettingFunds = '';

    $scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
    if ($scope.isAuthenticated) {
        var socialUser = $resource('/api/socialuser/', null, {'query': {method: 'GET', isArray:false}});
        socialUser.query().$promise.then(
            function success(data){
                $rootScope.name = data.name;
                $rootScope.bettingFunds = data.betting_funds;
            }
        );
    }
}
})();
