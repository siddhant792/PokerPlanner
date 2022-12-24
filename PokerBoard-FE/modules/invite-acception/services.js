'use strict';
(function () {
    /**
     * Activate user account if the token is valid
     */
    angular.module("pokerPlanner").service('invitationService', [
        'Restangular', 'APP_CONSTANTS',
        
        function(
            Restangular, APP_CONSTANTS
        ) {
            /**
             * 
             * @param {integer} invite_id 
             * @returns whether invitation accepted or not
             */
            this.acceptInvite = invite_id => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.MEMBERS, invite_id).customPUT();
            };
    }]); 
})();
