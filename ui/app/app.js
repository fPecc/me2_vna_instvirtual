'use strict';

var app = angular.module("myApp", ["ngRoute", "chart.js", "g1b.datetime-range","ngTable"]);
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "views/main.html"
    });
});

app.controller("LineCtrl", function ($scope) {

    $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
    $scope.series = ['Series A', 'Series B'];
    $scope.data = [
      [65, 59, 80, 81, 56, 55, 40],
      [28, 48, 40, 19, 86, 27, 90]
    ];
    $scope.onClick = function (points, evt) {
      console.log(points, evt);
    };
    $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
    $scope.options = {
      scales: {
        yAxes: [
          {
            id: 'y-axis-1',
            type: 'linear',
            display: true,
            position: 'left'
          },
          {
            id: 'y-axis-2',
            type: 'linear',
            display: true,
            position: 'right'
          }
        ]
      }
    };
  });
                

app.constant('config', {  
    //backendUrl: 'https://dsbackend-mindsold.apps.eu1.mindsphere.io',
    backendUrl: 'http://localhost:6003',
    baseUrl: '/'
  });

app.filter('fromNow', function () {
    return function (date) {
        return moment(date).fromNow();
    }
});



app.service('db', function($http,config){
    this.readAll = function(table){
        var req = {
            method: 'GET',
            url: config.backendUrl + '/api/db?table=' + table
        }

        $http(req).then(function(response){
            return response;
        }).catch(function(err) {
            console.log('Augh, there was an error!', err.status, err.data);
            return err.status;
        });
    }

    this.insertConfig = function(table,data){
        var req = {
            method: 'put',
            url: config.backendUrl + '/api/db?table=' + table,
            data: data,
            headers: {'Content-Type':'application/json'}
        }
        //console.log("insertConfig: "+JSON.stringify(data));
        $http(req).then(function(response){
            return response;
        }).catch(function(err) {
            console.log('Augh, there was an error!', err.status, err.data);
            return err.status;
        });
    }
});