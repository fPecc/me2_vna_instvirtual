'use strict';

app.controller("TracesCtrl", ['$scope','$http', function($scope, $http) {
    var self = this;
    var baseUrl = 'http://127.0.0.1:5000/';

    iziToast.settings({
        timeout: 5000,
        resetOnHover: false,
        pauseOnHover: false,
        position: 'topRight',
        icon: 'material-icons',
        transitionIn: 'flipInX',
        transitionOut: 'flipOutX',
        onOpening: function(){
            console.log('callback abriu!');
        },
        onClosing: function(){
            console.log("callback fechou!");
        }
    });

    /*
    * Obtengo los datos básicos de como esta configurado el VNA en este momento
    */
    self.options = [{},{},{},{}];
    self.data = [{},{},{},{}];

    /*
    * Modal trace variables
    */
    self.selectedTrace = 1;
    self.minFreq = 0;
    self.maxFreq = 0;
    self.medFreq = 0;
    self.bw = 0;

    self.getActualConfig = function()
    {
        var req = {
            method: 'GET',
            url: baseUrl + 'api/getActualConfig'
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
                    iziToast.error({
                        title: 'Error',
                        message: 'Probablemente el VNA se encuentra desconectado!'
                    });
                    console.log('Augh, there was an error!', err.status, err.data);
                });
    }
    
    self.getActualConfig();

    $scope.onClick = function (points, evt) {
      console.log(points, evt);
    };
    $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }];
    
    self.Trace = function(){
        console.log("Trace");
    };

    /*
    * Modal trace and modal bw functions
    */
    self.selectedTraceClicked = function(i)
    {
        self.selectedTrace = i;
        self.minFreq = self.options[i-1].scales.xAxes[0].ticks.min;
        self.maxFreq = self.options[i-1].scales.xAxes[0].ticks.max;
        self.medFreq = (self.minFreq+self.maxFreq)/2;
        self.bw = self.maxFreq-self.minFreq;
    }

    self.minMaxChanged = function()
    {
        self.medFreq = (self.minFreq+self.maxFreq)/2;
        self.bw = self.maxFreq-self.minFreq;
    }

    self.medBWChanged = function()
    {
        self.minFreq = self.medFreq-self.bw/2;
        self.maxFreq = self.medFreq+self.bw/2;
    }

    self.setTraceNewFreq = function()
    {
        var req = {
            method: 'POST',
            url: baseUrl + 'api/setTraceNewFreq',
            data: {
                selectedTrace: self.selectedTrace,
                minFreq: self.minFreq,
                maxFreq: self.maxFreq
            },
            headers: {
                "Content-Type": "application/json"
            }
        };
        $http(req)
                .then(function(response) {
                    console.log('Trace set');
                    iziToast.success({
                        title: 'OK',
                        message: 'Se modificaron correctamente los datos'
                    });
                    self.getActualConfig();
                })
                .catch(function(err) {
                    iziToast.error({
                        title: 'Error',
                        message: 'No se pudo completar la acción!'
                    });
                    console.log('Augh, there was an error!', err.status, err.data);
                });
    }

    self.setSweep = function()
    {
        // TODO: completar
        var req = {
            method: 'POST',
            url: baseUrl + 'api/setSweep',
            data: {
                sweepTime: 10
            },
            headers: {
                "Content-Type": "application/json"
            }
        };
        $http(req)
                .then(function(response) {
                    console.log('Sweep set');
                    iziToast.success({
                        title: 'OK',
                        message: 'Se modificaron correctamente los datos'
                    });
                    self.getActualConfig();
                })
                .catch(function(err) {
                    iziToast.error({
                        title: 'Error',
                        message: 'No se pudo completar la acción!'
                    });
                    console.log('Augh, there was an error!', err.status, err.data);
                });
    }

    self.setScale = function()
    {
        // TODO: completar
        var req = {
            method: 'POST',
            url: baseUrl + 'api/setScale',
            data: {
                selectedTrace: self.selectedTrace,
                minScale: 0,
                maxScale: 10
            },
            headers: {
                "Content-Type": "application/json"
            }
        };
        $http(req)
                .then(function(response) {
                    console.log('Scale set');
                    iziToast.success({
                        title: 'OK',
                        message: 'Se modificaron correctamente los datos'
                    });
                    self.getActualConfig();
                })
                .catch(function(err) {
                    iziToast.error({
                        title: 'Error',
                        message: 'No se pudo completar la acción!'
                    });
                    console.log('Augh, there was an error!', err.status, err.data);
                });
    }

  }]);