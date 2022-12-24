'use strict';
(function () {
    angular.module('pokerPlanner').controller('pokerboardDetailsCtrl', [
        '$state', '$scope', '$stateParams', '$mdToast', 'pokerboardService', 'createGameService', 'APP_CONSTANTS',
        function ($state, $scope, $stateParams, $mdToast, pokerboardService, createGameService, APP_CONSTANTS) {
            
            $scope.pokerboard = {};
            const pokerboardId = $stateParams.id;
            $scope.email = "";
            $scope.isEditing = false;
            $scope.prevOrder = [];
            $scope.emailInviteForm = true;
            $scope.showUserError = false;
            $scope.showGroupError = false;
            
            /**
             * Redirects to pokerboard's members page
             */
            $scope.goToMembers = () => {
                $state.go('pokerboard-members', {"pid": pokerboardId});
            }

            /**
             * Shows form to invite through email
             */
            $scope.showEmailForm = () => {
                $scope.emailInviteForm = true;
            }

            /**
             * Shows form to invite through group
             */
            $scope.showGroupForm = () => {
                $scope.emailInviteForm = false;
            }
            
            $scope.moveDown = (idx) => {
                const tickets = [...$scope.pokerboard.tickets];
                if(idx!=tickets.length-1){
                    let temp = tickets[idx];
                    tickets[idx] = tickets[idx+1];
                    tickets[idx+1] = temp;
                    if(!$scope.isEditing){
                        $scope.isEditing = true;
                        $scope.prevOrder = $scope.pokerboard.tickets;
                    }
                    $scope.pokerboard.tickets = tickets;
                }
            }

            $scope.moveUp = (idx) => {
                const tickets = [...$scope.pokerboard.tickets];
                if(idx!=0){
                    let temp = tickets[idx];
                    tickets[idx] = tickets[idx-1];
                    tickets[idx-1] = temp;
                    if(!$scope.isEditing){
                        $scope.isEditing = true;
                    }
                    if(!$scope.isEditing){
                        $scope.isEditing = true;
                        $scope.prevOrder = $scope.pokerboard.tickets;
                    }
                    $scope.pokerboard.tickets = tickets;
                }
            }

            $scope.saveOrdering = () => {
                const tickets = [...$scope.pokerboard.tickets].map((ticket, idx)=>{
                    ticket.rank = idx+1;
                    return ticket;
                })
                pokerboardService.orderTickets(tickets, $scope.pokerboard.id);
                $scope.isEditing = false;
            }

            $scope.cancelOrdering = () => {
                $scope.pokerboard.tickets = $scope.prevOrder;
                $scope.isEditing = false;
            }

            /**
             * Fetch details of the pokerboard
             */
            const init = () => {
                pokerboardService.getPokerboardDetails(pokerboardId).then(response => {
                    $scope.pokerboard = response;
                    $scope.pokerboard.estimated = $scope.pokerboard.tickets.filter(obj=>obj.estimate);
                    $scope.pokerboard.tickets = $scope.pokerboard.tickets.filter(obj=>!obj.estimate);
                    $scope.pokerboard.tickets = $scope.pokerboard.tickets.sort((a,b)=>a.rank-b.rank);
                    const ticketIds = $scope.pokerboard.tickets.reduce((prev, curr, currIdx) => {
                        return prev + curr.ticket_id + (currIdx !== $scope.pokerboard.tickets.length - 1 ? ", " : "");
                    } , "");
                    
                    if(ticketIds == "") return;
                    const query = `issue IN (${ticketIds})`;
                    return createGameService.getTickets('?jql=' + query);
                })
                .then((res)=>{
                    const issues = res?.issues;
                    var issuesMap = issues.reduce(
                        (obj, item) => Object.assign(obj, { [item.key]: item }), {});
                    $scope.pokerboard.tickets = $scope.pokerboard.tickets.map((obj)=>{
                        obj.summary = issuesMap[obj.ticket_id]?.fields?.summary;
                        return obj;
                    });
                })
                .catch(error => {
                    // $state.go('404-page-not-found');
                });

                pokerboardService.getSession(pokerboardId).then(response => {
                    if (response.status == 1) {
                        $state.go('voting-session', {id: pokerboardId});
                    }
                });
            }
            init();

            /**
             * Invokes error when user is already invited
             */
            $scope.isUserError = () => {
                $scope.showUserError = ($scope.existingInvite === $scope.email);
            };

            /**
             * Invokes error when group is already invited
             */
            $scope.isGroupError = () => {
                $scope.showGroupError = ($scope.existingInvite === $scope.group);
            };

            /**
             * Invokes error when group does not exist
             */
            $scope.isError = () => {
                $scope.showError = ($scope.notExistingGroup === $scope.group);
            };

            /**
             * Invites user
             */
            $scope.inviteUser = () => {
                const user = {
                    type: ($scope.emailInviteForm) ? 1 : 2,
                    invitee: ($scope.emailInviteForm) ? $scope.email : null,
                    pokerboard: $stateParams.id,
                    group_name: ($scope.emailInviteForm) ? null : $scope.group,
                    role: $scope.role
                }
                // Creates invites and checks for errors, if encountered
                pokerboardService.inviteUser(user).then(response => {
                        // User invited
                }, error => {
                    if (error.data.non_field_errors[0] === APP_CONSTANTS.ERROR_MESSAGES.USER_ALREADY_INVITED) {
                        $scope.existingInvite = $scope.email;
                        $scope.isUserError();
                    }
                    if (error.data.non_field_errors[0] === APP_CONSTANTS.ERROR_MESSAGES.GROUP_ALREADY_INVITED) {
                        $scope.existingInvite = $scope.group;
                        $scope.isGroupError();
                    }
                    if (error.data.non_field_errors[0] === APP_CONSTANTS.ERROR_MESSAGES.GROUP_DOES_NOT_EXIST) {
                        $scope.notExistingGroup = $scope.group;
                        $scope.isError();
                    }
                });
            }

            $scope.createSession = ticketId => {
                pokerboardService.createSession({"ticket": ticketId}).then(response => {
                    $state.go('voting-session', {id: pokerboardId, defaultResponse: response});
                }, error => {
                    $mdToast.show($mdToast.simple().textContent(error.data.ticket[0]));
                });
            }

        }]);
})();
