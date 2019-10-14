'use strict';

app.controller("TracesCtrl", ['$scope','$http', function($scope, $http) {
    var self = this;

    /*
    * Obtengo los datos básicos de como esta configurado el VNA en este momento
    */
    self.options = [{},{},{},{}];
    self.data = [{},{},{},{}];

    var req = {
        method: 'GET',
        url: 'http://127.0.0.1:5000/api/getActualConfig'
    };
    $http(req)
            .then(function(response) {
                var i = 0;
                response.data.traces.forEach(element => {
                    console.log(element);
                    i = element.number - 1;
                    self.options[i] = {
                        title: {
                            display: true,
                            text: element.title
                        },
                        scales: {
                          yAxes: [
                            {
                                id: 'y-axis-1',
                                type: element.yScale,
                                display: true,
                                position: 'left',
                                ticks: {
                                    max: element.yMax,
                                    min: element.yMin
                                },
                                scaleLabel: {
                                    display: true,
                                    labelString: element.yLabel
                                }
                            }
                          ],
                          xAxes: [
                            {
                                type: element.xScale,
                                display: true,
                                position: 'bottom',
                                ticks: {
                                    max: element.xMax,
                                    min: element.xMin
                                },
                                scaleLabel: {
                                    display: true,
                                    labelString: element.xLabel
                                }
                            }
                          ]
                        },
                        elements: {
                            line: {
                                    fill: false
                            }
                        }
                      };

                    self.data[i] = element.data;
                    console.log(self.data[i]);
                    /*
                    self.data[i] = [
                        {x: 10,y:20},
                        {x: 100,y:100},
                        {x: 500,y:1000},
                        {x: 1000,y:2000},
                        {x: 10000,y:3000}];*/
                });
                
            })
            .catch(function(err) {
                console.log('Augh, there was an error!', err.status, err.data);
            });

    $scope.onClick = function (points, evt) {
      console.log(points, evt);
    };
    $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }];
    
  }]);