'use strict';
(function () {
    /**
     * Creates game with user specified data
     */
    angular.module("pokerPlanner").service('createGameService', [
        'Restangular', 'APP_CONSTANTS',
        
        function(
            Restangular, APP_CONSTANTS
        ) {
            /* Get projects and sprints from JIRA */
            this.getSuggestions = function(){
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.SUGGESTIONS).get();
            };

            /* Get the list of tickets from JQL query */
            this.getTickets = function(query){
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.JQL + query).get();
            };

            /* Creating the pokerboard game */
            this.createGame = function(data){
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.POKERBOARD).post(data);
            };
    }]); 
})();
