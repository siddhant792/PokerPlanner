'use strict';
(function () {
    /**
     * Controller for signup
     */
    angular.module('pokerPlanner').controller('signupCtrl', [
        '$scope', '$rootScope', '$state', '$cookies', 'signupService', 'APP_CONSTANTS',
        function(
            $scope, $rootScope, $state, $cookies, signupService, APP_CONSTANTS
        ) {
            $scope.showError = false;
            $rootScope.signedUp = false;
            $scope.passNote = APP_CONSTANTS.ERROR_MESSAGES.PASSWORD_VALIDATION;

            /**
             * Checks if email already exists
             */ 
            $scope.isEmailError = () => {
                $scope.showError = ($scope.existingEmail === $scope.email);
            };

            $scope.signup = () => {
                const user = {
                    first_name: $scope.firstName,
                    last_name: $scope.lastName,
                    email: $scope.email,
                    password: CryptoJS.SHA256($scope.password).toString(),
                }

                signupService.createUser(user).then(response => {
                    $rootScope.signedUp = true;
                    $scope.goToLogin();
                }, error => {
                    if(error.status === 404)
                        $state.go('404-page-not-found');
                    else if(error.status === 500)
                        $state.go('500-internal-server-error');
                    else if(error.data.email[0] === APP_CONSTANTS.ERROR_MESSAGES.EMAIL) {
                        $scope.existingEmail = $scope.email;
                        $scope.isEmailError();
                    }
                })
            };
    
            $scope.goToLogin = () => {
                $state.go('login');
            };
    }]);
})();
