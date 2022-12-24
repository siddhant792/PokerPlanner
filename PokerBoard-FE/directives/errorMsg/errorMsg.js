'use strict';
(function () {
    /**
     * Checks if the input field is empty 
     */
    angular.module('pokerPlanner').directive('errorMsg', () => {
        var linker = (scope, el, attrs) => {
            var ele = document.querySelector('[ng-model=' + attrs.field + ']');
            scope.value = " ";
            ele.onfocus = () => {
                scope.$watch("field", () => {
                    scope.attribute = attrs.field.toLowerCase();
                    scope.value = scope.field;
                });
            };
        };
        return {
            scope: {
                field: '=field',
            },
            templateUrl: 'directives/errorMsg/errorMsg.html',
            link: linker
        };
    });
})();
