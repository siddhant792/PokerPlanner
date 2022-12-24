'use strict';
(function () {
    /**
     * Returns list of pokerboards
     */
    angular.module("pokerPlanner").service('memberService', [
        'Restangular', 'APP_CONSTANTS',
        function(
            Restangular, APP_CONSTANTS
        ) {
            /**
             * Fetches members through pokerboard id
             * @param {integer} pokerboardId 
             * @returns member details
             */
            this.getMembers = pokerboardId => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.MEMBERS, pokerboardId).get();
            }

            /**
             * Removes a member of the pokerboard
             * @param {integer} inviteId 
             */
            this.removeMember = inviteId => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.MEMBERS, inviteId).remove();
            }
    }]); 
})();
