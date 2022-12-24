'use strict';
(function () {
    angular.module('pokerPlanner').controller('groupListCtrl', [
        '$scope', '$rootScope', 'groupService',
        function ($scope, $rootScope, groupService) {
            /*
            Pattern of data that is to be stored in $scope.groups ->
            [
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
            ]
            */
            $scope.groups = [];
            $scope.groupName = "";

            /**
             * @description create a group
             */
            $scope.createGroup = () => {
                groupService.createGroup({name: $scope.groupName}).then(response => {
                    $scope.groups = [...$scope.groups, {
                        id: response.id,
                        name: response.name,
                        created_at: new Date(response.created_at).toLocaleDateString(),
                        members: response.members.length
                    }];
                }, err => {})
            }

            /**
             * Deletes group
             * @param {integer} groupId 
             */
            $scope.deleteGroup = groupId => {
                groupService.deleteGroup(groupId).then(response => {
                    $scope.groups = $scope.groups.filter(group => group.id != groupId)
                }, err => { });
            }

            /**
             * @description get group list
             */
            $scope.getGroups = () => {
                groupService.getGroups().then(response => {
                    $scope.groups = response.map(obj => {
                        return {
                            id: obj.id,
                            name: obj.name,
                            created_at: new Date(obj.created_at).toLocaleDateString(),
                            members: obj.members.length,
                            created_by: obj.created_by
                        }
                    });;
                }, err => { })
            }
            $scope.getGroups();
        }]);

})();
