'use strict';
(function () {
    /**
     * Displays navbar on each page when user is authenticated
     */
    angular.module('pokerPlanner').directive('navBar', () => {
        const nav = $scope => {
            $scope.navLinks = {
                POKERBOARD: {
                    'ui-sref': 'pokerboard',
                    'link': 'Pokerboard'
                },
                GROUPS: {
                    'ui-sref': 'groups',
                    'link': 'Groups'
                },
                PROFILE: {
                    'ui-sref': 'profile',
                    'link': 'Profile'
                }
            }
        }
        
        return {
            link: nav,
            templateUrl: 'directives/navbar/navbar.html'
        };
    });
})();
