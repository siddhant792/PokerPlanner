'use strict';
(function () {
    /**
     * Checks if password matches confirm password
     */
    angular.module('pokerPlanner').directive('checkConfirmPass', () => {
        return {
            require: 'ngModel',
            scope: {
                confirmPassword: '=checkConfirmPass'
            },
            link: (scope, element, attributes, paramval) => {
                paramval.$validators.checkConfirmPass = val => {
                    return val == scope.confirmPassword;
                };
                scope.$watch("confirmPassword", () => {
                    paramval.$validate();
                });
            }
        };
    });
})();
