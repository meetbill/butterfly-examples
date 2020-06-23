'use strict';

/* Controllers */

app.controller('CrontabCtrl', ['$scope', '$filter', '$http', 'editableOptions', 'editableThemes', 'Request',
function($scope, $filter, $http, editableOptions, editableThemes, Request) {
    editableThemes.bs3.inputClass = 'input-sm';
    editableThemes.bs3.buttonsClass = 'btn-sm';
    editableOptions.theme = 'bs3';
    //$scope.jobs = [
    //  {name: 'exe_cmd', status: 2, cmd: "ls", rule: '* * * * * ',nexttime :"20190808 20:24"},
    //];
    $scope.update_jobs = function() {
        Request.get('ruqi/get_jobs',
        function(res) {
            $scope.jobs = res.data;
        },
        false, true);
    };

    // remove job
    $scope.removeJob = function(name) {
        Request.post('ruqi/remove_job', {
            'name': name
        },
        function(res) {
            for (let i = $scope.jobs.length - 1; i >= 0; i--) {
                if ($scope.jobs[i].name === name) {
                    $scope.jobs.splice(i, 1);
                }
            };
        });
    };

    // add job
    $scope.addJob = function() {
        $scope.inserted = {
            name: '',
            status: null,
            cmd: null,
            rule: null,
            nexttime: null,
        };
        $scope.jobs.push($scope.inserted);
    };
    // update job
    $scope.saveJob = function(data) {
        Request.post("ruqi/add_job", data,
        function(res) {
            $scope.update_jobs();
        });
    };

    $scope.update_jobs();
}]);
