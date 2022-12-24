'use strict';
(function () {
    angular.module('pokerPlanner').controller('profileCtrl', [
        '$scope', '$rootScope', '$state', '$cookies', '$mdToast', 'profileService', 'APP_CONSTANTS',
        function (
            $scope, $rootScope, $state, $cookies, $mdToast, profileService, APP_CONSTANTS,
        ) {
            $scope.passNote = APP_CONSTANTS.ERROR_MESSAGES.PASSWORD_VALIDATION;
            $scope.votes = [];
            const init = function () {
                profileService.getUser($rootScope.user.id).then(response => {
                    $scope.groupList = [];
                    $scope.pokerboardList = [];
                    $scope.email = response.email;
                    $scope.firstname = response.first_name;
                    $scope.lastname = response.last_name;
                    $scope.votes = response.votes;
                    const parsePokerboard = ele => {
                        $scope.pokerboardList.push({
                            title: ele.title,
                            description: ele.description,
                            status: APP_CONSTANTS.POKERBOARD_STATUS[ele.status],
                        });
                    }
                    const parseGroup = ele => {
                        $scope.groupList.push({
                            name: ele.name,
                            createdAt: new Date(ele.created_at).toLocaleDateString(),
                        });
                    }
                    response.pokerboard.forEach(parsePokerboard);
                    response.group.forEach(parseGroup);
                });
            };

            init();

            $scope.onSubmit = () => {
                /* User is trying to change password or other data */
                const data = !$scope.password ? { first_name: $scope.firstname, last_name: $scope.lastname } : { first_name: $scope.firstname, last_name: $scope.lastname, password: CryptoJS.SHA256($scope.password).toString() };
                profileService.updateUser($rootScope.user.id, data).then(response => {
                    $mdToast.show($mdToast.simple().textContent("Profile Update Successful"));
                }, error => {
                    $scope.errorMsg = error.data.password[0];
                });
            };
        }
    ]);
})()
