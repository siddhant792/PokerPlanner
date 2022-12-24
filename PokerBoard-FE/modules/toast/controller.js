'use strict';
(function() {
    angular.module('pokerPlanner').controller('toastCtrl', [
        'toast',
        function (toast) {
            toast.create ({
                timeout: 2 * 1000,
                message: 'Successfully signed up!',
                className: 'alert-success',
                dismissible: true
            });
        }
    ]);
})()
