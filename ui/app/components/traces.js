'use strict';

app.controller("TracesCtrl", function ($scope) {
    var self = this;

    /*
    * Obtengo los datos básicos de como esta configurado el VNA en este momento
    */
    var req = {
        method: 'GET',
        url: 'http://127.0.0.1:5000/api/getActualConfig'
    }

    self.options = 
    $http(req)
            .then(function(response) {
                console.log(response);

            })
            .catch(function(err) {
                console.log('Augh, there was an error!', err.status, err.data);
            });

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