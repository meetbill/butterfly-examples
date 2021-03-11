'use strict';

var app = angular.module('app');
app.controller('CanghaiMQMsgsCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer', '$state', '$location', '$window',
function($scope, Request, $stateParams, $httpParamSerializer, $state, $location, $window){
    $scope.maxSize = 5;
    $scope.itemsPerPage = 15;
    $scope.totalItems = 1000;

    var params = {};
    if ($stateParams.page_index) {
        params['page_index'] = $stateParams.page_index;
        $scope.currentPage =  Number($stateParams.page_index);
    }
    else
    {
        params['page_index'] = 1;
        $scope.currentPage =  1;
    }

    if ($stateParams.page_size) {
        params['page_size'] = $stateParams.page_size;
    }
    else
    {
        params['page_size'] = 15;
    }

    if ($stateParams.queue_name) {
        params['queue_name'] = $stateParams.queue_name;
    }
    else
    {
        params['queue_name'] = 'default';
    }

    if ($stateParams.registry_name) {
        params['registry_name'] = $stateParams.registry_name;
    }
    else
    {
        params['registry_name'] = 'queued';
    }


    $scope.updateData=function (params){
        Request.get('/canghai/list_msgs?' + $httpParamSerializer(params),function(res){
            $scope.msgs = res.data.msgs;
            $scope.queueName = res.data.name;
            $scope.registryName = res.data.registry_name;
            $scope.totalItems = res.data.total_items;
        }, false, true);
    }

    $scope.updateData(params)

    $scope.emptyQueue = function() {
        var update_params = {};
        update_params["queue_name"] = $stateParams.queue_name;
        update_params["registry_name"] = $stateParams.registry_name;
        Request.post("/canghai/empty_queue", update_params, function(res){
            $scope.updateData(params);
        })
    };
    $scope.deleteMsg = function(msg_id) {
        var update_params = {};
        update_params["msg_id"] = msg_id
        Request.post("/canghai/delete_msg", update_params, function(res){
            $scope.updateData(params);
        })
    };
    $scope.pageChanged = function() {
        params['page_index'] = String($scope.currentPage);
        $state.go('app.canghai.mq_msgs', params,  {notify: false});
        $scope.updateData(params)
    };

}]);
