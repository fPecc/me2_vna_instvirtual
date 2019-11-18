'use strict';

app.config(function($routeProvider) {
    $routeProvider
        .when("/sa", {
            templateUrl : "views/components/sa.html"
        });
});

app.controller('SaCtrl', ['$scope', '$http', function ($scope, $http) {
    var self = this;
    
    /* COMPLETAR */
    
}]);