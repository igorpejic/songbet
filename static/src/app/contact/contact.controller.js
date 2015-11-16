(function() {
    'use strict';
    angular
        .module('app.bet')
        .controller('contactController', contactController);
    
    contactController.$inject = ['contactService', 'Notification'];

    function contactController(contactService, Notification) {
        var vm = this;
        vm.submit = submit;
        vm.rand1 = getRandom();
        vm.rand2 = getRandom();

        function submit() {
            if (!vm.name) {
                Notification.error({message: "Name is required."});
                return;
            } else if (!vm.email) {
                Notification.error({message: "Email address is required."});
                return;
            } else if (!vm.message) {
                Notification.error({message: "Message is required."});
                return;
            // TODO: replace with google recaptcha
            } else if (vm.sum != (vm.rand1 + vm.rand2)) {
                Notification.error({message: "Are you a spam bot? Please sum the numbers correctly."});
                return;
            }

            contactService.save({name: vm.name, email: vm.email, message: vm.message}).$promise.then(
                function success(data) {
                    Notification.success({message: "Message sent! We will get back to you soon."});
                },
                function failure(data) {
                    if (typeof(data.data.email) !== 'undefined'){
                        Notification.error({message: data.data.email[0]});
                    } else {
                        Notification.error({message: 'Something went wrong. Please try again.'});
                    }

                }
            );
        }
        function getRandom() {
            return Math.floor((Math.random()*6)+1);
        }
    }
}());
