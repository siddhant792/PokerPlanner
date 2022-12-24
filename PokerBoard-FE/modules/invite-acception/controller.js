'use strict';
(function () {
    angular.module('pokerPlanner').controller('invitationCtrl', [
        '$scope', '$state', 'invitationService', '$stateParams',

        function (
            $scope, $state, invitationService, $stateParams
        ) {
            /**
             * Redirects to login
             */
            $scope.goToLogin = () => {
                $state.go('login');
            };
            
            /**
             * Checks if the user who was invited is the one making the acception request
             */
            const init = () => {
                invitationService.acceptInvite($stateParams.invite_id)
                .then(response => {
                    $scope.statusMsg = 'Invitation accepted';
                }, error => {
                    $scope.statusMsg = 'Invalid request';
                });
            }
            init();
        }
    ]);
})()
