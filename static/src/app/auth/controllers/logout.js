angular.module('app.auth')
  .controller('LogoutCtrl', ['$auth', '$alert', '$state', function($auth, $alert, $state) {
    if (!$auth.isAuthenticated()) {
        return;
    }
    $auth.logout()
      .then(function() {
        
      });
  }]);
