(function() {
    'use strict';
    angular
        .module('app.bet')
        .controller('singleBetController', singleBetController);
    
    singleBetController.$inject = ['$rootScope', 'lastWeekPrepService', 'addBetService', '$filter', '$state', 'Notification', '$timeout'];

    function singleBetController($rootScope, lastWeekPrepService, addBetService, $filter, $state, Notification, $timeout) {
        var vm = this;
        vm.bets = [];
        vm.date = lastWeekPrepService[0].date;
        vm.lastWeekSongs = lastWeekPrepService[0].songs;
        vm.addBet = addBet;
        vm.removeBet = removeBet;
        vm.submitBet = submitBet;
        vm.totalOdds = totalOdds;
        vm.stake = 10;
        vm.calculateWin = calculateWin;
        vm.win = 0;

        function addBet(newSong, choice){

            var bet = {};
            bet.song = newSong;
            bet.choice = choice;
            if (choice == '1') {
                newSong.one = !newSong.one;
                bet.odd = newSong.odd_1;
            } else if(choice == '2') {
                newSong.two = !newSong.two;
                bet.odd = newSong.odd_2;
            } else if (choice == 'X') {
                newSong.x = !newSong.x;
                bet.odd = newSong.odd_x;
            }

            // check if song is already present in bets and if present remove it
            for(var i=0;i<vm.bets.length;i++){
                var temp = vm.bets[i];
                if(angular.equals(temp, bet)){
                    vm.bets.splice(vm.bets.indexOf(temp), 1);
                    return;
                }
            }
            vm.bets.push(bet);
            calculateWin();
        }

        function removeBet(bet, index) {
            if (bet.choice == '1') {
                bet.song.one = !bet.song.one;
            } else if(bet.choice == '2') {
                bet.song.two = !bet.song.two;
            } else if (bet.choice == 'X') {
                bet.song.x = !bet.song.x;
            }
            vm.bets.splice(index, 1);
            calculateWin();
        }

        function submitBet() {
			if (vm.stake === 0) {
                Notification.error({message: "Can't bet without stake. Can you?"});
				return;
			}
            var bets = [];
            angular.forEach(vm.bets, function(value, key) {
                bets.push({song: value.song.song.id, choice: value.choice});
            });
            addBetService.save({date: vm.date, stake: vm.stake, bet_type: 3, bets: bets}).$promise.then(
                function success(data){
                    $rootScope.bettingFunds -= data.stake;
                    Notification.success({message: "Your bet has been saved."});
                    vm.startFade = true;
                    $timeout(resetPendingBet, 2000);
                },
                function failure(data) {
                    Notification.error({message: "Insufficient funds."});
                }
            );
        }
        function totalOdds() {
            var total = 0;
            angular.forEach(vm.bets, function(value, key) {
                total += value.odd;
            });
            return $filter('number')(total, 2);
        }
        function calculateWin() { 
            vm.win = $filter('number')(vm.totalOdds() * vm.stake, 2);
        }

        function resetPendingBet() {
            vm.bets = [];
            vm.totalOdds = null;
            vm.stake = 10;
            vm.win = 0;
            angular.forEach(vm.lastWeekSongs, function(value, key) {
                if (value.hasOwnProperty('one')) {
                    delete value.one;
                } else if (value.hasOwnProperty('two')) {
                    delete value.two;
                    value.removeAttr('two');
                } else if (value.hasOwnProperty('x')) {
                    delete value.x;
                }
            });
        }
    }
}());
