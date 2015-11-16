angular
    .module('app.core')
    .factory('authenticate', authenticate);

authenticate.$inject = ['$q', '$state', '$auth'];

// currently not used, but could be useful
function authenticated($q, $state, $auth) {
    var deferred = $q.defer();
    if (!$auth.isAuthenticated()) {
        deferred.reject();
    } else {
        deferred.resolve();
    }
    return deferred.promise;
}
