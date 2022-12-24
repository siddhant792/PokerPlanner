'use strict';
(function () {
    angular.module("pokerPlanner").run(($rootScope, $state, $cookies, $transitions, $mdToast, Restangular, APP_CONSTANTS) => {
        const user = JSON.parse($cookies.get('user') || ("{}"));
        $rootScope.user = user;
        const token = user?.token;
        $rootScope.isAuth = token;

        $rootScope.logout = () => {
            $cookies.remove("user");
            $rootScope.user = {};
            $rootScope.isAuth = false;
            $state.go("login");
        }
        /**
         * Executes before every transition
         */
        $transitions.onBefore({ to: "*" }, function (transition) {
            if (!APP_CONSTANTS.ROUTES.PUBLIC_ROUTES.find((route) => route === transition.to().name)) {
                const currentUser = JSON.parse($cookies.get('user') || ("{}"));
                const authToken = currentUser?.token
                if (authToken) {
                    if (APP_CONSTANTS.ROUTES.UNAUTH_ROUTES.find((route) => route === transition.to().name)) {
                        return transition.router.stateService.target('pokerboard');
                    }
                } else {
                    if (!APP_CONSTANTS.ROUTES.UNAUTH_ROUTES.find((route) => route === transition.to().name)) {
                        return transition.router.stateService.target('login');
                    }
                }
            }
        });

        /**
         * Executes at the time of request
         */
        Restangular.setFullRequestInterceptor((element, operation, route, url, headers, params, httpConfig) => {
            $rootScope.loading = true;
            const authToken = JSON.parse($cookies.get('user') || ("{}")).token
            if (authToken) {
                headers.Authorization = `Token ${authToken}`;
                $rootScope.isAuth = authToken;
            } else {
                const currentUrl = $state.current.name;
                $rootScope.isAuth = "";
                if (!(APP_CONSTANTS.ROUTES.UNAUTH_ROUTES.includes(currentUrl))) {
                    $state.go('login');
                }
            }
            return { element, params, headers, httpConfig };
        });

        /**
         * Executes if successful response is received
         */
        Restangular.addResponseInterceptor((data, operation, what, url, response, deferred) => {
            $rootScope.loading = false;           
            return data;
        });

        /**
         * Shows toast for errors
         */
         const handleObjErrors = errors => {
            for(let key in errors){
                if((typeof errors[key]) === "string"){
                    $mdToast.show($mdToast.simple().textContent(errors[key]));
                } else if((typeof errors[key]) === "object") {
                    for(let error of errors[key]){
                        $mdToast.show($mdToast.simple().textContent(error));
                    }
                }
            }
        }

        /**
         * Executes if error is received
         */
        Restangular.setErrorInterceptor(response => {
            $rootScope.loading = false;
            const key = response.status;
            const errors = response.data;
            if((typeof errors) === "string"){
                $mdToast.show($mdToast.simple().textContent(errors));
            } else if((typeof errors) === "object") {
                handleObjErrors(errors);
            }
            if(key in APP_CONSTANTS.ERROR_ROUTES){
                $state.go(APP_CONSTANTS.ERROR_ROUTES[key], null, {
                    location: 'replace'
                });
            }
            // Stop the promise chain.
            return true;
        });
    });
})();
