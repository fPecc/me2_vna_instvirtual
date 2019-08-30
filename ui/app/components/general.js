'use strict';

app.controller('GeneralCtrl', ['$scope','$interval','$http', function($scope, $interval, $http) {
    var self = this;
    var getBatteryPromise;
    var getMutexPromise;

    init();
    
    $scope.$on('$destroy', function() {
        // Poner aca todos los timers que se quieren detener
        $interval.cancel(getBatteryPromise);
        $interval.cancel(getMutexPromise);

        // Destruir sesion
        var req = {
            method: 'POST',
            url: 'http://127.0.0.1:5000/api/destroySession'
        }
        $http(req)
                .then(function(response) {
                })
                .catch(function(err) {
                    console.log('Augh, there was an error!', err.status, err.data);
                });
      });

    function init(){
        /*
        * Como obtener la bateria del equipo
        */
        self.batteryCharge = 0;

        function getBatteryCharge(){
            var req = {
                method: 'GET',
                url: 'http://127.0.0.1:5000/api/getBatteryCharge'
            }

            $http(req)
                .then(function(response) {
                    //console.log('Battery charge: ' + response.data.battery);
                    //console.log(response);
                    self.batteryCharge = response.data.battery;
                })
                .catch(function(err) {
                    console.log('Augh, there was an error!', err.status, err.data);
                });
            }
        getBatteryCharge();
        getBatteryPromise = $interval(getBatteryCharge,60000);

        /*
        * Como obtener el mutex para acceder al equipo
        */
        function getMutex(){
            var req = {
                method: 'GET',
                url: 'http://127.0.0.1:5000/api/getMutex'
            }
            $http(req)
                .then(function(response) {
                })
                .catch(function(err) {
                    console.log('Augh, there was an error!', err.status, err.data);
                });
        }
        getMutex();
        getMutexPromise = $interval(getMutex,5000);
    }

}]);