'use strict';

/* Controllers */
// signin controller
app.controller('SigninFormController', ['$scope', '$http', '$state','$localStorage', function ($scope, $http, $state,$localStorage) {
    $scope.user = {};
    $scope.authError = null;
    $scope.login = function () {
        $scope.authError = null;
        // Try to login
        $http.post('auth/login', {username: $scope.user.email, password: $scope.user.password})
        .then(function(response) {
          if ( !response.data.success ) {
            $scope.authError = '邮箱或密码错误，请重试' + response.data.message;
          }else{
            $localStorage.jwt = response.data.data.token
            $state.go('app.dashboard-v1');
          }
        }, function(x) {
          $scope.authError = '服务器错误';
        });

        //$state.go('app.dashboard-v1');
    };
}])
;
