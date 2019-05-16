'use strict';

app.config(function($routeProvider) {
    $routeProvider
        .when("/assets", {
            templateUrl : "views/components/assets.html"
        });
});


app.controller('BusyIndicatorCtrl', ['$scope','$interval', function($scope, $interval) {
    var self = this;
}]);


app.controller('AssetListCtrl', ['$scope', '$http', function ($scope, $http) {
    var self = this;
    self.assets = [];
    
    self.fetchDataFromAssetManagement = function(filterParams) {    
        var assetsUrl = '/api/assetmanagement/v3/assets'
        assetsUrl = assetsUrl + '?size=100';
        if(filterParams) {
            assetsUrl = assetsUrl + '&filter=' + encodeURIComponent(filterParams);
        }
        
        var assetsReq = {
            method: 'GET',
            url: assetsUrl
        }
        $http(assetsReq)
        .then(function(response) {
            console.log("response: " + response);
            if (response.data.hasOwnProperty('_embedded')) {
                self.assets = response.data['_embedded'].assets;
            }
            self.assets.forEach(function(asset) {

              var aspectsReq = {
                    method: 'GET',
                    url: '/api/assetmanagement/v3/assets/'+asset.assetId+'/aspects'
                }

                $http(aspectsReq)
                .then(function(response) {
                    console.log('aspects retrieved from API for asset ' + asset.assetId + ': ' + response);
                    if(response.data.hasOwnProperty('_embedded')) {
                        asset.aspects = response.data['_embedded']['aspects'];
                    } 
                }).catch(function(err) {
                    console.log('Augh, there was an error!', err.status, err.data);
                });
            });
        })
        .catch(function(err) {
            console.log('Augh, there was an error!', err.status, err.data);
        });
    }

    // Filter asset list by user
    $scope.filterAssetList = function() {
        if($scope.searchBoxText){
            // Get asset with specific name
            var filterAssetName =  '{"name": {"contains": "' + $scope.searchBoxText + '"}}';
            self.fetchDataFromAssetManagement(filterAssetName);
        }
        else {
            self.fetchDataFromAssetManagement();
        }
    }
    
    self.fetchDataFromAssetManagement();
}]);