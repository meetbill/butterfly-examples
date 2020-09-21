'use strict';

app.controller('CanghaiMQCtrl', ['$scope','Request',function($scope, Request){

    $scope.update_data=function (){
        Request.get("/canghai/list_workers",function(res){
            $scope.workers = res.data.workers;
        }, false, true);
        Request.get("/canghai/list_queues",function(res){
            $scope.queues = res.data.queues;
        }, false, true);
    }
    $scope.update_data()

}]);
