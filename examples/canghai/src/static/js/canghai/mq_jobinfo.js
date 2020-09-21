'use strict';

var app = angular.module('app');
app.controller('CanghaiMQJobInfoCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer',
function($scope, Request, $stateParams, $httpParamSerializer){
    $scope.update_data=function (){
        var params={};
        params['job_id'] = $stateParams.job_id;
        Request.get('/canghai/job_info?' + $httpParamSerializer(params),function(res){
            $scope.job = res.data;
        }, false, true);
    }
    $scope.update_data()

}]);
