/**
 * @file task list
 */

var app = angular.module('app');
app.controller('SchedulerHistoryListCtrl', ['$scope', '$modal', 'i18nService', 'Request', '$httpParamSerializer', '$stateParams',
function ($scope, $modal, i18nService, Request, $httpParamSerializer, $stateParams) {

    i18nService.setCurrentLang('zh-cn');

    $scope.searchValue = '';
    $scope.searchNames = ['job_id', 'job_name'];
    $scope.selectedName = 'job_id';

    if ($stateParams.job_id) {
        $scope.selectedName = 'job_id';
        $scope.searchValue = $stateParams.job_id
    }

    if ($stateParams.job_name) {
        $scope.selectedName = 'job_name';
        $scope.searchValue = $stateParams.job_name
    }

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

            Request.get('/ruqi/get_history?' + $httpParamSerializer(params),
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
            field: 'id',
            displayName: 'id',
        },
        {
            field: 'job_id',
            displayName: 'job_id',
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
            field: 'cmd_is_success',
            displayName: '是否执行成功',
            cellTemplate: ''
            + '<div class="ui-grid-cell-contents">'
            + '<label class="label label-danger" ng-if="!row.entity.cmd_is_success">失败</label>'
            + '<label class="label label-success" ng-if="row.entity.cmd_is_success">成功</label>'
            + '</div>',
        },
        {
            field: 'cmd_output',
            displayName: '程序输出'
        },
        {
            field: 'cmd_cost',
            displayName: '执行耗时'
        },
        {
            field: 'scheduler_name',
            displayName: 'scheduler'
        },
        {
            field: 'c_time',
            displayName: '执行时间'
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
}]);
