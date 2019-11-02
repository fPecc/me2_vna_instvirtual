'use strict';

var app = angular.module("myApp", ["ngRoute", "chart.js", "g1b.datetime-range","ngTable","ngCookies"]);

app.config(['$httpProvider', function($httpProvider) { 
    $httpProvider.defaults.withCredentials = true; 
}]); 

app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "views/main.html"
    });
});