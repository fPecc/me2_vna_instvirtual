'use strict';

app.controller('GeneralCtrl', ['$scope','$interval','$http', function($scope, $interval, $http) {
    var self = this;

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
        $interval(getBatteryCharge,60000);
    }

}]);