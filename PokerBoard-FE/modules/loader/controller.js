'use strict';
(function () {
    angular.module('pokerPlanner').controller('loaderCtrl', [
        '$rootScope',
        function ($rootScope) {
            $rootScope.$on('LOAD', () => { $scope.loading = true });
            $rootScope.$on('UNLOAD', () => { $scope.loading = false });
        }
    ]);
})();
