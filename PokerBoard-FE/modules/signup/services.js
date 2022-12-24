'use strict';
(function () {
    /**
     * Creates user and returns details of user(first_name, last_name, email) 
     * and token
     */
    angular.module("pokerPlanner").service ('signupService', [
        'Restangular', 'APP_CONSTANTS',
        function (Restangular, APP_CONSTANTS) {
            this.createUser = user => {
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.SIGNUP).post(user);
            };
    }]); 
})();
