'use strict';
(function () {
    angular.module('pokerPlanner').controller('emailVerificationCtrl', [
        '$scope', '$state', '$cookies', 'emailVerificationService', '$stateParams',

        function (
            $scope, $state, $cookies, emailVerificationService, $stateParams
        ) {
            $scope.goToLogin = () => {
                $state.go('login');
            };
            
            emailVerificationService.activateAccount($stateParams.uid, {'token': $stateParams.token})
                .then(response => {
                    $scope.statusMsg = 'Account activated successfully';
                }, error => {
                    $scope.statusMsg = 'Invalid email activation link';
                });
        }
    ]);
})()
