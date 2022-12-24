'use strict';
(function () {
    /**
     * Get already created game sessions
     */
    angular.module("pokerPlanner").service('votingSessionService', [
        'Restangular', 'APP_CONSTANTS', '$websocket',
        function (
            Restangular, APP_CONSTANTS, $websocket
        ) {
            /**
             * Get game session
             * @param {Integer} pokerboardId 
             * @returns session details
             */
            this.getSession = pokerboardId => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.GAME_SESSION, pokerboardId).get();
            };

            /**
             * Fetches pokerboard through pokerboard id
             * @param {Integer} pokerboardId 
             * @returns pokerboard details
             */
            this.getPokerboardDetails = pokerboardId => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.POKERBOARD, pokerboardId).get();
            }

            /**
             * Fetches JIRA issue from ticketID
             * @param {String} query
             * @returns JIRA issue details
             */
            this.getIssue = query => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.JQL + query).get();
            }

            /**
             * Fetches JIRA issue cooments from ticketID
             * @param {*} query
             * @returns JIRA issue details
             */
            this.getComments = ticketId => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.COMMENT + `?issueId=${ticketId}`).get();
            }

            /**
             * Add comment on JIRA issue
             * @param {Object} comment
             * @returns Comment on JIRA
             */
            this.postComment = comment => {
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.COMMENT).post(comment);
            }

            /**
             * Connect to websocket
             * @param {Integer} sessionId
             * @param {String} token
             * @returns Connection with websocket
             */
            this.wsConnect = (sessionId, token) => {
                return $websocket(APP_CONSTANTS.WS_BASE_URL + "session/" + sessionId + "?token=" + token);
            }

        }]);
})();
