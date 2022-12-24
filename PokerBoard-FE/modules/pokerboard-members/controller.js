'use strict';
(function () {
    angular.module('pokerPlanner').controller('pokerboardMembersCtrl', [
        '$state', '$scope', '$rootScope', '$stateParams', 'memberService', 'pokerboardService', 'APP_CONSTANTS',
        function ($state, $scope, $rootScope, $stateParams, memberService, pokerboardService, APP_CONSTANTS) {
            
            $scope.pokerboard = {};
            const pokerboardId = $stateParams.pid;
            $scope.isManager = false;

            /**
             * Checks if the user is the manager of the pokerboard and fetches details of the pokerboard's members
             */
            const init = () => {
                // Gets pokerboard details and checks if the logged in user is the manager of the pokerboard
                pokerboardService.getPokerboardDetails(pokerboardId).then(response => {
                    $scope.pokerboard = response;
                    $scope.isManager = ($rootScope.user.email == response.manager.email);
                });

                // Fetches details of the pokerboard's members
                memberService.getMembers(pokerboardId).then(response => {
                    $scope.members = [];
                    const parse = member => {
                        $scope.members.push({
                            id: member.id,
                            pokerboard: member.pokerboard,
                            invitee: member.invitee,
                            group: member.group,
                            group_name: member.group_name ? member.group_name : "-",
                            role: APP_CONSTANTS.MEMBER_ROLE[member.role]
                        });
                    }
                    response.forEach(parse);
                }, error => {
                    $state.go('404-page-not-found');
                })
            }
            init();

            $scope.setDeleteNumber = id => {
                $scope.delMember = id;
            };

            /**
             * Removes a member
             */
            $scope.removeMember = () => {
                memberService.removeMember($scope.delMember);
                $scope.members = $scope.members.filter(member => member.id != $scope.delMember);
            }
        }]);
})();
