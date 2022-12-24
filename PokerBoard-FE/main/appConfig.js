'use strict';
(function () {
    angular.module("pokerPlanner").config([
        '$stateProvider', '$urlRouterProvider', '$locationProvider', 'RestangularProvider', 'APP_CONSTANTS',
        function (
            $stateProvider, $urlRouterProvider, $locationProvider, RestangularProvider, APP_CONSTANTS,
        ) {
            $locationProvider.hashPrefix('');

            $stateProvider
                .state('404-page-not-found', {
                    url: '/404-page-not-found',
                    templateUrl: 'modules/error_templates/404-page-not-found.html'
                })

                .state('500-internal-server-error', {
                    url: '/500-internal-server-error',
                    templateUrl: 'modules/error_templates/500-internal-server-error.html'
                })

                .state('signup', {
                    url: '/signup',
                    templateUrl: 'modules/signup/signup.html',
                    controller: 'signupCtrl'
                })

                .state('login', {
                    url: '/login',
                    templateUrl: 'modules/login/login.html',
                    controller: 'loginCtrl'
                })

                .state('profile', {
                    url: '/profile',
                    templateUrl: 'modules/profile/profile.html',
                    controller: 'profileCtrl'
                })

                .state('pokerboard', {
                    url: '/',
                    templateUrl: 'modules/pokerboard/pokerboard.html',
                    controller: 'pokerboardCtrl'
                })

                .state('create-game', {
                    url: '/create-game',
                    templateUrl: 'modules/create-game/create-game.html',
                    controller: 'createGameCtrl'
                })

                .state('pokerboard-details', {
                    url: "/pokerboard/:id",
                    templateUrl: "modules/pokerboard/pokerboardDetails.html",
                    controller: "pokerboardDetailsCtrl",
                })
                
                .state("groups", {
                    url: "/groups",
                    templateUrl: "modules/group/groupList.html",
                    controller: "groupListCtrl",
                })

                .state("group", {
                    url: "/groups/:id",
                    templateUrl: "modules/group/groupDetails.html",
                    controller: "groupDetailsCtrl",
                })              
                
                .state('email-verification', {
                    url: '/activate/:uid/:token',
                    templateUrl: 'modules/emailVerification/email-verification.html',
                    controller: 'emailVerificationCtrl'
                })

                .state('voting-session', {
                    url: "/session/:id",
                    templateUrl: "modules/voting-session/voting-session.html",
                    controller: "votingSessionCtrl",
                    params: {
                        defaultResponse: undefined,
                    }
                })
                
                .state('invite-acception', {
                    url: '/join/:invite_id',
                    templateUrl: 'modules/invite-acception/inviteAcception.html',
                    controller: 'invitationCtrl'
                })

                .state('pokerboard-members', {
                    url: '/pokerboard/:pid/members',
                    templateUrl: 'modules/pokerboard-members/pokerboardMembers.html',
                    controller: 'pokerboardMembersCtrl'
                });
                
            $urlRouterProvider.otherwise("/404-page-not-found");
            
            RestangularProvider.setBaseUrl(APP_CONSTANTS.BASE_URL);
        }   
    ]);
})();
