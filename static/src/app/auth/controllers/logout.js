angular.module('app.auth')
  .controller('LogoutCtrl', function($auth, $alert, $state) {
    if (!$auth.isAuthenticated()) {
        return;
    }
    $auth.logout()
      .then(function() {
        
      });
  });
