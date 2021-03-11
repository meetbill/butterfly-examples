'use strict';

var app = angular.module('app');
app.controller('CanghaiMQMsgInfoCtrl', ['$scope', 'Request', '$stateParams', '$httpParamSerializer',
function($scope, Request, $stateParams, $httpParamSerializer){
    $scope.update_data=function (){
        var params={};
        params['msg_id'] = $stateParams.msg_id;
        Request.get('/canghai/msg_info?' + $httpParamSerializer(params),function(res){
            $scope.msg = res.data;
        }, false, true);
    }
    $scope.update_data()

}]);
