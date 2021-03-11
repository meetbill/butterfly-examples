'use strict';

var app = angular.module('app');
app.controller('CanghaiMQSubMsgInfoCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer',
function($scope, Request, $stateParams, $httpParamSerializer){
    $scope.update_data=function (){
        var params={};
        params['msg_id'] = $stateParams.msg_id;
        Request.get('/canghai/submsg_info?' + $httpParamSerializer(params),function(res){
            $scope.submsgs = res.data.list;
        }, false, true);
    }
    $scope.update_data()

}]);
