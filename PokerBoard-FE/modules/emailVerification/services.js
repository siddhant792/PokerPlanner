'use strict';
(function () {
    /**
     * Activate user account if the token is valid
     */
    angular.module("pokerPlanner").service('emailVerificationService', [
        'Restangular', 'APP_CONSTANTS',
        
        function(
            Restangular, APP_CONSTANTS
        ) {
            this.activateAccount = function(uid, data){
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.ACCOUNT_ACTIVATE , uid).customPUT(data);
            };
    }]); 
})();
