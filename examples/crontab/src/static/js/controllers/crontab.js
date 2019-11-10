'use strict';

/* Controllers */

//app.
//    controller('CrontabCtrl', ['$scope', '$filter', '$http', function($scope, $filter, $http){
app.controller('CrontabCtrl', ['$scope', '$filter', '$http', 'editableOptions', 'editableThemes',
  function($scope, $filter, $http, editableOptions, editableThemes){
    editableThemes.bs3.inputClass = 'input-sm';
    editableThemes.bs3.buttonsClass = 'btn-sm';
    editableOptions.theme = 'bs3';
    // editable table
    //$scope.jobs = [
    //  {name: 'exe_cmd', status: 2, cmd: "ls", rule: '* * * * * ',nexttime :"20190808 20:24"},
    //];
    $http.get("/x/get_jobs").success(function (response) {$scope.jobs = response.data;})

    // remove job
    $scope.removeJob = function(name) {
        var remove_job = $http.post("/x/remove_job",{
                "name":name}
                )
        remove_job.success(function (response) {
            for (let i = $scope.jobs.length - 1; i >= 0 ; i--) {
                if($scope.jobs[i].name === name) {
                    console.log(i)
                    $scope.jobs.splice(i, 1);
                }
            };
        })
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
      //$scope.user not updated yet
      return $http.post('x/add_job', data);
    };
  }]);
