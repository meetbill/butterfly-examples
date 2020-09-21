'use strict';

var app = angular.module('app');
app.controller('CanghaiMQJobsCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer', '$state', '$location', '$window',
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
        Request.get('/canghai/list_jobs?' + $httpParamSerializer(params),function(res){
            $scope.jobs = res.data.jobs;
            $scope.queueName = res.data.name;
            $scope.registryName = res.data.registry_name;
            $scope.totalItems = res.data.total_items;
        }, false, true);
    }

    $scope.updateData(params)

    $scope.pageChanged = function() {
        params['page_index'] = String($scope.currentPage);
        $state.go('app.canghai.mq_jobs', params,  {notify: false});
        $scope.updateData(params)
    };

}]);
