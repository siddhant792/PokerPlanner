'use strict';
(function () {
    /*Controller for voting session*/
    angular.module('pokerPlanner').controller('votingSessionCtrl', [
        '$scope', '$rootScope', '$state', 'votingSessionService', '$mdToast', 'APP_CONSTANTS', '$stateParams',
        function ($scope, $rootScope, $state, votingSessionService, $mdToast, APP_CONSTANTS, $stateParams) {
            const pokerboardId = $stateParams.id;

            let issueId;
            $scope.voteList = [];
            const setCards = type => {
                /* Setting card type */
                $scope.cardList = APP_CONSTANTS.DECK_TYPE[type];
            };

            const setIssueDetails = ticketId => {
                /* Fetching JIRA issue to be estimated */
                const query = "?jql=issue IN (" + ticketId + ")";
                issueId = ticketId;
                votingSessionService.getIssue(query).then(response => {
                    $scope.issueTitle = ticketId + ": " + response.issues[0].fields.summary;
                    $scope.issueDescription = response.issues[0].fields.description;
                    $scope.labelList = response.issues[0].fields.labels;
                }, error => {
                    $state.go('404-page-not-found');
                });
            };

            $scope.getComments = () => {
                /* Getting comment on JIRA */
                votingSessionService.getComments(issueId).then(response => {
                    $scope.comments = response.map(obj => {
                        return {
                            author: obj.author.displayName,
                            created: new Date(obj.created).toLocaleString(),
                            body: obj.body
                        }
                    });
                }, error => {
                    $mdToast.show($mdToast.simple().textContent(APP_CONSTANTS.ERROR_MESSAGES.COMMENT_GET_FAILED));
                });
            };

            $scope.postComment = () => {
                /* Posting new comment on JIRA */
                votingSessionService.postComment({ "issue": issueId, "comment": $scope.comment }).then(response => {
                    $mdToast.show($mdToast.simple().textContent(APP_CONSTANTS.SUCCESS_MESSAGES.COMMENT_ADDED));
                }, error => {
                    $mdToast.show($mdToast.simple().textContent(APP_CONSTANTS.ERROR_MESSAGES.COMMENT_POST_FAILED));
                });
            };

            $scope.startCountdown = () => {
                /* Countdown timer broadcast */
                const data = {
                    message: "Start Timer",
                    message_type: APP_CONSTANTS.MESSAGE_TYPE.START_TIMER
                }
                $scope.websocket.send(data);
            };

            $scope.skipGame = () => {
                /* Skipping the current game */
                const data = {
                    message: "Skip game",
                    message_type: APP_CONSTANTS.MESSAGE_TYPE.SKIP
                }
                $scope.websocket.send(data);
            };

            const countdown = () => {
                /* Countdown helper */
                if ($scope.time == 0) {
                    clearInterval($scope.timerId);
                    $scope.estimated = true;
                    $scope.$apply();
                    return;
                } else {
                    $scope.time--;
                }
                $scope.$apply();
            };

            const setCountdown = timer => {
                /* Setting up countdown timer */
                $scope.time = 0;
                if (timer === "null") {
                    return;
                }
                let startTime = new Date(timer);
                let currentTime = new Date();
                $scope.time = Math.round($scope.duration - (currentTime - startTime) / 1000);
                if ($scope.time <= 0) {
                    clearInterval($scope.timerId);
                    $scope.time = 0;
                    $scope.estimated = true;
                    $scope.$apply();
                    return;
                }else {
                    $scope.estimated = false;
                    $scope.$apply();
                }
                $scope.timerId = setInterval(countdown, 1000);
            };

            const initializeGame = data => {
                /* Initializing game after successfull connection with websocket */
                $scope.voteList = [];
                updateParticipants(data.users);
                const parseVotes = ele => {
                    addRealTimeVotedUser(ele);
                }
                data.votes.forEach(parseVotes);
                setCountdown(data.timer);
            };

            const updateParticipants = data => {
                /* Updating Participants in UI */
                $scope.participantList = [];
                const parseUsers = ele => {
                    let name = ele.first_name + " " + ele.last_name;
                    if (!$scope.participantList.includes(name)) {
                        $scope.participantList.push(name);
                    }
                }
                data.forEach(parseUsers);
            };

            const addRealTimeVotedUser = data => {
                /* Adding user who voted to the list for UI */
                // updateVote(data.user.id, data.user.estimate);
                $scope.voteList = $scope.voteList.filter(ele => ele.id != data.user.id);
                let first_name = data.user.first_name;
                let last_name = data.user.last_name;
                if (data.user.id === $rootScope.user.id) {
                    elevateCard($scope.cardList.indexOf(data.estimate));
                }
                $scope.voteList.push(
                    {
                        id: data.user.id,
                        name: first_name + " " + last_name,
                        estimate: data.estimate,
                        short_name: (first_name.charAt(0) + last_name.charAt(0)).toUpperCase()
                    },
                );
            };

            const onGameSkipped = () => {
                /* Navigate to estimation page */
                $state.go('pokerboard-details', { id: pokerboardId });
            };

            const setSocketConnection = sessionId => {
                /* Establishing web socket connection */
                $scope.websocket = votingSessionService.wsConnect(sessionId, $rootScope.user.token);
                $scope.websocket.send({ "message": "Member Joined", "message_type": APP_CONSTANTS.MESSAGE_TYPE.INITIALIZE_GAME });
                $scope.websocket.onMessage(function (message) {
                    const obj = JSON.parse(message.data);
                    console.log(obj);
                    switch (obj.type) {
                        case APP_CONSTANTS.MESSAGE_TYPE.INITIALIZE_GAME: initializeGame(obj);
                            break;
                        case APP_CONSTANTS.MESSAGE_TYPE.SKIP: onGameSkipped();
                            break;
                        case APP_CONSTANTS.MESSAGE_TYPE.VOTE: addRealTimeVotedUser(obj.vote);
                            break;
                        case APP_CONSTANTS.MESSAGE_TYPE.START_TIMER: setCountdown(obj.timer_started_at);
                            break;
                        case APP_CONSTANTS.MESSAGE_TYPE.ESTIMATE: $state.go('pokerboard-details', { id: pokerboardId });
                            break;
                        case APP_CONSTANTS.MESSAGE_TYPE.UPDATE: updateParticipants(obj.users);
                            break;
                    }
                });
            };

            const setUserVote = number => {
                /* Broadcast current user vote */
                const data = {
                    message: {
                        estimate: number
                    },
                    message_type: APP_CONSTANTS.MESSAGE_TYPE.VOTE
                }
                $scope.websocket.send(data);
            };

            const elevateCard = id => {
                /* Highlighting current user's voted card */
                if ($scope.prevCard != undefined) document.getElementById("card" + $scope.prevCard).classList.remove("selected-card");
                document.getElementById("card" + id).classList.add("selected-card");
                $scope.prevCard = id;
            };

            $scope.setEstimate = function (number, id) {
                /* Card click function */
                if ($scope.prevCard === id) {
                    return;
                }
                elevateCard(id);
                setUserVote(number);
            };

            const onSession = response => {
                if (response.status != 1) {
                    $state.go('404-page-not-found');
                }
                setSocketConnection(response.id);
                setIssueDetails(response.ticket.ticket_id);
            };

            const init = () => {
                /* Initializing function */
                if (!$stateParams.defaultResponse) {
                    votingSessionService.getSession(pokerboardId).then(response => {
                        onSession(response);
                    }, error => {
                        $state.go('404-page-not-found');
                    });
                } else {
                    onSession($stateParams.defaultResponse);
                }

                /* Fetching Pokerboard Details */
                votingSessionService.getPokerboardDetails(pokerboardId).then(response => {
                    $scope.isAdmin = response.manager.id === $rootScope.user.id;
                    $scope.duration = response.duration;
                    $scope.title = response.title;
                    $scope.description = response.description;
                    setCards(response.estimation_type);
                }, error => {
                    $state.go('404-page-not-found');
                });
            };

            $scope.setTicketEstimate = () => {
                const data = {
                    message: {
                        estimate: $scope.ticketEstimate
                    },
                    message_type: "estimate"
                }
                $scope.websocket.send(data);
            };

            init();
        }
    ]);
})()
