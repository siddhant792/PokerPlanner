'use strict';
(function () {
    /*Controller for creating games*/
    angular.module('pokerPlanner').controller('createGameCtrl', [
        '$scope', '$rootScope', '$state', '$cookies', 'createGameService', '$mdToast', 'APP_CONSTANTS', '$window',
        function (
            $scope, $rootScope, $state, $cookies, createGameService, $mdToast, APP_CONSTANTS, $window
        ) {
            const init = () => {
                /* Initializing function */
                $scope.deckType = Object.keys(APP_CONSTANTS.DECK_NAME).map(ele =>{
                    return {
                        val:ele,
                        name: APP_CONSTANTS.DECK_NAME[ele],
                    }
                });
                
                createGameService.getSuggestions().then(response => {
                    /* Import porjects and sprints from JIRA */
                    $scope.projectList = [];
                    $scope.sprintList = [];
                    const parseProjects = ele => {
                        $scope.projectList.push({
                            label: ele.displayName,
                            id: ele.value,
                        });
                    }
                    const parseSprints = ele => {
                        $scope.sprintList.push({
                            label: ele.name,
                            id: ele.id,
                        });
                    }
                    response.projects.forEach(parseProjects);
                    response.sprints.forEach(parseSprints);
                });
            }

            /* Setting default deck type */
            $scope.selectedType = APP_CONSTANTS.DEFAULT_DECK_OPTION.SERIAL;

            init();

            const showTickets = query => {
                /* Show the list of JIRA tickets from selected projects/sprint/JQL */
                createGameService.getTickets('?jql=' + query).then(response => {
                    $scope.ticketList = [];
                    const parseTickets = ele => {
                        $scope.ticketList.push({
                            id: ele.id,
                            key: ele.key,
                            summary: ele.fields.summary,
                        });
                    }
                    response.issues.forEach(parseTickets);
                    $scope.jqlCustomQuery = query;
                }, error => {
                    $scope.ticketList = []
                    $mdToast.show($mdToast.simple().textContent(APP_CONSTANTS.ERROR_MESSAGES.INVALID_JQL));
                });
            };

            $scope.executeCustomQuery = () => {
                /* Get the JQL written in the query box */
                /* Setting both pre-selected projects/sprint to empty if user executes custom JQL query */
                $scope.selectedSprints = [];
                $scope.selectedProjects = [];
                showTickets($scope.jqlCustomQuery)
            };

            $scope.setDeleteNumber = id => {
                $scope.delTicket = id;
            };

            $scope.removeTicket = () => {
                /* Remove the particular ticket from the list */
                $scope.ticketList = $scope.ticketList.filter(ele => ele != $scope.delTicket);
            };

            const arrToString = arr => {
                var proj = "";
                const makeString = (ele, index) => {
                    proj += ele.id;
                    if (index != arr.length - 1) proj += ',';
                };
                if(arr) arr.forEach(makeString);
                return proj;
            };

            $scope.queryConstructor = () => {
                var projectQuery = arrToString($scope.selectedProjects);
                var sprintQuery = arrToString($scope.selectedSprints);
                var query;
                if (projectQuery || sprintQuery) {
                    if (!projectQuery) {
                        query = "sprint IN (" + sprintQuery + ")";
                    } else if (!sprintQuery) {
                        query = "project IN (" + projectQuery + ")";
                    } else {
                        query = "project IN (" + projectQuery + ") AND sprint IN (" + sprintQuery + ")";
                    }
                }
                if (query){
                    showTickets(query);
                }else{
                    $scope.ticketList = [];
                    $scope.jqlCustomQuery = "";
                } 
            };

            $scope.submit = () => {
                /* Creating the game from desired data */
                const finalizedTickets = [];
                const makeFinalTickets = ele => {
                    finalizedTickets.push(ele.key);
                };
                $scope.ticketList.forEach(makeFinalTickets);
                const data = {
                    title: $scope.name,
                    description: $scope.description,
                    estimation_type: $scope.selectedType,
                    duration: $scope.duration,
                    tickets: finalizedTickets
                };
                createGameService.createGame(data).then(response => {
                    $state.go("pokerboard");
                    /*
                    TODO: Goto estimation page
                    */
                }, error => {
                    if ('title' in error.data) {
                        $scope.nameErrorMsg = error.data.title[0];
                        $window.scrollTo(0, 0);
                    }
                });
            };
        }
    ]);
})()
