'use strict';
(function () {
    angular.module('pokerPlanner').controller('groupDetailsCtrl', [
        '$scope', '$state', '$stateParams', '$rootScope', 'groupService',
        function ($scope, $state, $stateParams, $rootScope, groupService) {
            /*
            Pattern of data that is to be stored in $scope.group ->
             {
                    "id": <int>,
                    "name": "<string>",
                    "members": [
                        {
                            "id": <int>,
                            "user": {
                                "first_name": "<string>",
                                "last_name": "<string>",
                                "email": "<string>",
                            },
                            "group": <int>,
                            "created_at": "<datetime>",
                            "updated_at": "<datetime>"
                        },
                    ],
                    "created_by": <int>,
                    "created_at": "<datetime>",
                    "updated_at": "<datetime>"
                },
             */
            $scope.group = {};
            const groupId = $stateParams.id;
            $scope.email = "";

            /**
             * @description create members in the group
             */
            $scope.createMember = () => {
                groupService.createMember($scope.email, $scope.group.id).then(response => {
                    $scope.group.members = [...$scope.group.members, {user: response.user}]
                }, err => {});
            }

            /**
             * Sets the id of the member to be removed to $scope.delMember
             * @param {integer} id 
             */
            $scope.setDeleteNumber = id => {
                $scope.delMember = id;
            };

            /**
             * Removes member from the group
             */
            $scope.removeMember = () => {
                groupService.removeMember(groupId, {"userId": $scope.delMember}).then(response=>{
                    $scope.group.members = $scope.group.members.filter(member => member.id != $scope.delMember)
                }, err=>{
                    $state.go('500-internal-server-error');
                });
            }

            /**
             * @description Get group details
             */
             $scope.getGroupDetails = () => {
                groupService.getGroupDetails(groupId).then(response => {
                    $scope.group = response;
                }, err => {});
            }
            $scope.getGroupDetails();
        }]);
})();
