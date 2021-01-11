# 如期
---
layout: post
title:
subtitle:
date: 2019-11-10 14:21:31
category:
author: meetbill
tags:
   -
---

```
"如期"而至
```

<!-- vim-markdown-toc GFM -->

* [1 需求及常用方法](#1-需求及常用方法)
    * [1.1 定时触发](#11-定时触发)
    * [1.2 定期轮询](#12-定期轮询)
* [2 使用](#2-使用)
    * [2.1 部署](#21-部署)
        * [2.1.1 部署 butterfly](#211-部署-butterfly)
        * [2.1.2 部署 ruqi3.0 后端服务(使用 MySQL jobstore)](#212-部署-ruqi30-后端服务使用-mysql-jobstore)
        * [2.1.3 部署 ruqi3.0 前端服务](#213-部署-ruqi30-前端服务)
    * [2.2 接口](#22-接口)
        * [2.2.1 查询](#221-查询)
        * [2.2.2 任务操作](#222-任务操作)
            * [添加任务](#添加任务)
            * [删除任务](#删除任务)
* [3 Wiki](#3-wiki)

<!-- vim-markdown-toc -->
# 1 需求及常用方法

## 1.1 定时触发

crontab 设置：系统服务控制，易配置且稳定可靠；分散难维护。

## 1.2 定期轮询

> 轮询固定时间间隔
```
while True:
    do something
    time.sleep(XXX)
```
> `crontab */N`定时轮询

# 2 使用
## 2.1 部署

### 2.1.1 部署 butterfly

[butterfly 环境部署](https://github.com/meetbill/butterfly/wiki/butterfly_deploy)

### 2.1.2 部署 ruqi3.0 后端服务(使用 MySQL jobstore)

handler(默认已添加)

> 配置(conf/config.py)
```
scheduler_name="Scheduler1"  # Scheduler name, Used to perform historical queries
scheduler_store="mysql"      # ("none"/"mysql"/"memory") ; if set none, the schedule is not run
```
### 2.1.3 部署 ruqi3.0 前端服务
> 静态文件
```
cp -rf src/static/js/controllers/ruqi ${butterfly_dir}/static/js/controllers
cp -rf src/static/tpl/ruqi ${butterfly_dir}/static/tpl
```

> 界面左侧栏(${butterfly_dir}/static/js/controllers/blocks/nav.js)
```
{
    "description":"如期--(定时)",
    "sort": 4,
    "glyphicon": "glyphicon-time icon text-info-dker",
    "is_have_second": true,
    "sref":"",
    "children":[
            {
                "sref":"app.ruqi.scheduler",
                "description":"定时任务"
            },
            {
                "sref":"app.ruqi.scheduler_history",
                "description":"任务执行历史"
            }
    ]
},
```
> 前端路由(${butterfly_dir}/static/js/config.router.js)
```
.state('app.ruqi', {
    url: '/ruqi',
    template: '<div ui-view></div>'
}).state('app.ruqi.scheduler', {
    url: '/scheduler_list?job_id&job_name&page_index&page_size',
    templateUrl: 'static/tpl/ruqi/scheduler_list.html',
    resolve: load(['ui.grid', 'ui.grid.resizeColumns','ui.grid.pagination' ,'static/js/controllers/ruqi/scheduler.js'])
}).state('app.ruqi.scheduler_history', {
    url: '/scheduler_history_list?job_id&job_name&page_index&page_size',
    templateUrl: 'static/tpl/ruqi/scheduler_history_list.html',
    resolve: load(['ui.grid', 'ui.grid.resizeColumns','ui.grid.pagination' ,'static/js/controllers/ruqi/scheduler_history.js'])
```

## 2.2 接口

### 2.2.1 查询
> 查询任务
```
curl "http://127.0.0.1:8585/ruqi/get_jobs"

response:
{
   "data" : {
      "total" : 2,
      "list" : [
         {
            "job_id" : "test2",
            "cmd" : "bash scripts/test.sh",
            "next_run_time" : "2021-01-07 10:44:36",
            "job_name" : "rdb",
            "rule" : "3.0s",
            "Job_trigger" : "interval"
         },
         {
            "job_id" : "test1",
            "cmd" : "bash scripts/test.sh",
            "next_run_time" : "2021-01-07 10:44:43",
            "job_name" : "other",
            "rule" : "10.0s",
            "Job_trigger" : "interval"
         }
      ]
   },
   "stat" : "OK"
}
```
> 查询当前服务状态
```
curl "http://127.0.0.1:8585/ruqi/status"

response:
{
   "data" : {
      "check_time" : "2021-01-07 10:39:23",
      "wait_seconds" : 1.941772,
      "next_wakeup_time" : "2021-01-07 10:39:23"
   },
   "stat" : "OK"
}
```
### 2.2.2 任务操作

#### 添加任务
```
$ curl -v -d '{"job_trigger":"interval", "job_id":"test3", "job_name":"platform", "rule":"10s","cmd":"bash scripts/test.sh"}' "http://127.0.0.1:8585/ruqi/add_job"

response:
{
    "stat": "OK"
}
```

> 备注
```
----------------------------------------------------------cmd
【脚本 1】bash scripts/xx/xx.sh
【脚本 2】python scripts/xx/xx.py arg1 arg2
【URL POST 请求 1】http://127.0.0.1:8585/demo_api/hello#{"str_info":"hello"}    # 使用 "#" 分割 URL 和请求体数据
【URL POST 请求 2】http://127.0.0.1:8585/demo_api/ping

----------------------------------------------------------rule
周期规则: Xs/Xm/Xh/Xd, 如: 10s(每 10s 进行一次操作)
单次规则: 2020-12-16 18:03:17/2020-12-16 18:05:17.682862/now
定时规则: *(秒) *(分) *(时) *(日) *(月) *(周)，如：0 20 2 * * *(每天凌晨 2:20 进行操作)
```


#### 删除任务
```

$ curl "http://127.0.0.1:8585/ruqi/remove_job?job_id=test3"

response:
{
    "stat": "OK"
}
```

# 3 Wiki

[wiki](https://github.com/meetbill/butterfly/wiki/butterfly_ruqi3.0)
