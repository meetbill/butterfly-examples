'use strict';

var app = angular.module('app');
app.controller('CanghaiMQWorkerInfoCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer',
function($scope, Request, $stateParams, $httpParamSerializer){
    $scope.update_data=function (){
        var params={};
        params['name'] = $stateParams.name;
        Request.get('/canghai/worker_info?' + $httpParamSerializer(params),function(res){
            $scope.worker = res.data;
        }, false, true);
    }
    $scope.update_data()

}]);
