'use strict';
(function () {
    angular.module("pokerPlanner").service('groupService', [
        'Restangular', 'APP_CONSTANTS',
        function(Restangular, APP_CONSTANTS) {

            /**
             * @description get group details service
             * @param {integer} groupId 
             * @returns group details object
             */
            this.getGroupDetails = (groupId) => {
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.GROUPS, groupId).get();
            };

            /**
             * @description create members in group service
             * @param {string} email 
             * @param {integer} group 
             * @returns an object with groupId and user details
             */
            this.createMember = (email, group) => {
                const user = { email, group };
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.CREATE_MEMBERS).post(user);
            }

            this.removeMember = (id, data) => {
                // Remove Member from the group
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.DELETE_MEMBERS, id).remove(data);
            }

            /**
             * @description create group service
             * @param {object} group 
             * @returns group object
             */
            this.createGroup = (group) => {
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.GROUPS).post(group);
            };

            /**
             * Deletes group
             * @param {object} group 
             */
            this.deleteGroup = (group) => {
                // delete group service
                return Restangular.one(APP_CONSTANTS.API_ENDPOINT.GROUPS, group).remove();
            };

            /**
             * @description get group list service
             * @returns list of group
             */
            this.getGroups = () => {
                return Restangular.all(APP_CONSTANTS.API_ENDPOINT.GROUPS).getList();
            };
    }]); 
})();
