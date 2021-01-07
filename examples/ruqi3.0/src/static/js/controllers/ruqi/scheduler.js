/**
 * @file task list
 */

var app = angular.module('app');
app.controller('SchedulerListCtrl', ['$scope', '$modal', 'i18nService', 'Request', '$httpParamSerializer',
function ($scope, $modal, i18nService, Request, $httpParamSerializer) {

    i18nService.setCurrentLang('zh-cn');

    $scope.searchValue = '';
    $scope.searchNames = ['job_id', 'job_name'];
    $scope.selectedName = 'job_id';

    var getPagedDataAsync = function (curPage) {
        setTimeout(function () {
            var data;
            var params = {};

            if (curPage) {
                params['page_index'] = curPage;
            }

            if ($scope.searchValue) {
                params[$scope.selectedName] = $scope.searchValue;
            }

            params['page_size'] = 15;

            Request.get('/ruqi/get_jobs?' + $httpParamSerializer(params),
                function (res) {
                    if (res.data.list)
                    {
                        $scope.myData = res.data.list;
                        $scope.gridOptions.totalItems = res.data.total;
                    }
                    else
                    {
                        $scope.myData = [];
                        $scope.gridOptions.totalItems = 0;
                    }
                }, false, true
            );
        },
        100);
    };

    $scope.myKeyup = function (e) {
        // IE 编码包含在 window.event.keyCode 中，Firefox 或 Safari 包含在 event.which 中
        var keycode = window.event ? e.keyCode : e.which;
        if (keycode === 13) {
            $scope.search();
        }
    };

    // Angular 网格控件主参数
    $scope.gridOptions = {
        data: 'myData',
        rowHeight: 36,
        headerRowHeight: 36,
        enableRowSelection: false,
        // -------- 分页属性 ----------------
        enablePagination: true,
        // 是否分页，默认为 true
        enablePaginationControls: true,
        // 使用默认的底部分页
        paginationPageSizes: [15],
        // 每页显示个数可选
        paginationPageSize: 15,
        paginationCurrentPage: 1,
        // 当前页码
        totalItems: 0,
        // 总数量
        useExternalPagination: true,
        // 是否使用分页按钮
        columnDefs: [{
            field: 'job_id',
            displayName: 'id',
            width: '15%'
        },
        {
            field: 'job_name',
            displayName: '分类',
        },
        {
            name: 'cmd',
            displayName: 'cmd',
        },
        {
            field: 'Job_trigger',
            displayName: '类型',
        },
        {
            field: 'rule',
            displayName: '规则'
        },
        {
            field: 'next_run_time',
            displayName: '下次运行时间'
        },
        {
            name: 'button',
            displayName: '操作',
            cellTemplate: ''
            + '<div>' //+'<div class="ui-grid-cell-contents">'
            + '<button ng-click="grid.appScope.removeJob(row.entity.job_id)" type="button" class="btn-danger btn" >删除</button>'
            + '<button ng-click="grid.appScope.pauseJob(row.entity.job_id)" type="button" class="btn-warning btn" ng-if="row.entity.next_run_time != null">暂停</button>'
            + '<button ng-click="grid.appScope.resumeJob(row.entity.job_id)" type="button" class="btn-info btn" ng-if="row.entity.next_run_time == null">继续</button>'
            + '<button type="button" class="btn-success btn"><a ui-sref="app.ruqi.scheduler_history({job_id: row.entity.job_id})" >执行历史</a></button>'
            + '</div>',
            width: '20%'
        }
        ],
        // ---------------api---------------------
        onRegisterApi: function (gridApi) {
            $scope.gridApi = gridApi;
            // 分页按钮事件
            gridApi.pagination.on.paginationChanged($scope,
            function (newPage, pageSize) {
                if (getPagedDataAsync) {
                    getPagedDataAsync(newPage);
                }
            });
        },
    };

    // 默认获取所有列表
    getPagedDataAsync(1);
    $scope.search = function () {
        $scope.gridOptions.paginationCurrentPage = 1;
        getPagedDataAsync($scope.gridOptions.paginationCurrentPage);
    };

    // -------- 按钮函数 ----------------
    $scope.addJob = function () {
        var modalInstance = $modal.open({
            templateUrl: 'static/tpl/ruqi/scheduler_add_job.html',
            controller: 'AddJobModalCtrl',
            size: 'lg',
            resolve: {}
        });

        modalInstance.result.then(function (params) {
            Request.post('/ruqi/add_job', params, function(res) {
                getPagedDataAsync($scope.gridOptions.paginationCurrentPage);
            });
        },
        function () {
            console.log('模式对话框关闭时间: ' + new Date());
        });
    };
    $scope.removeJob = function (job_id) {
        var params = {};
        params["job_id"] = job_id
        Request.post("/ruqi/remove_job", params, function(res){
            getPagedDataAsync($scope.gridOptions.paginationCurrentPage);

        })
    };
    $scope.pauseJob = function (job_id) {
        var params = {};
        params["job_id"] = job_id
        Request.post("/ruqi/pause_job", params, function(res){
            getPagedDataAsync($scope.gridOptions.paginationCurrentPage);

        })
    };
    $scope.resumeJob = function (job_id) {
        var params = {};
        params["job_id"] = job_id
        Request.post("/ruqi/resume_job", params, function(res){
            getPagedDataAsync($scope.gridOptions.paginationCurrentPage);
        })
    };


}]);

app.controller('AddJobModalCtrl', ['$scope', '$modalInstance', 'Request',
function ($scope, $modalInstance, Request) {
    $scope.params = {};
    $scope.params['job_name'] = 'rdb';
    $scope.params['job_trigger'] = 'interval';

    $scope.ok = function () {
        console.log($scope.params)
        $modalInstance.close($scope.params);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);
