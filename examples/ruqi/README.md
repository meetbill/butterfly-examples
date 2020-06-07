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
        * [2.1.2 部署 ruqi](#212-部署-ruqi)
    * [2.2 接口](#22-接口)
    * [2.3 访问](#23-访问)
* [3 Wiki](#3-wiki)

<!-- vim-markdown-toc -->
## 1 需求及常用方法

### 1.1 定时触发

crontab 设置：系统服务控制，易配置且稳定可靠；分散难维护。

### 1.2 定期轮询

> 轮询固定时间间隔
```
while True:
    do something
    time.sleep(XXX)
```
> `crontab */N`定时轮询

## 2 使用
### 2.1 部署

#### 2.1.1 部署 butterfly

[butterfly 环境部署](https://github.com/meetbill/butterfly/wiki/butterfly_deploy)

#### 2.1.2 部署 ruqi

> third
```
cp -rf src/third/apscheduler ${butterfly_dir}/third/
```

> handler
```
cp -rf src/handlers/ruqi ${butterfly_dir}/handlers/
```
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
            "sref":"app.ruqi.crontab",
            "description":"定时任务"
        }
    ]
},
```
> 前端路由(${butterfly_dir}/static/js/config.router.js)
```
.state('app.ruqi', {
    url: '/ruqi',
    template: '<div ui-view></div>'
}).state('app.ruqi.crontab', {
    url: '/crontab',
    templateUrl: 'static/tpl/ruqi/crontab.html',
    resolve: load(['xeditable', 'static/js/controllers/ruqi/crontab.js'])
})
```

### 2.2 接口
> 查询任务
```
curl "http://127.0.0.1:8585/ruqi/get_jobs"

response:
{
    "stat": "OK",
    "data": [
                {
                    "nexttime": "2019-11-10 17:26:00",
                    "cmd": "ls",
                    "name": "ls_test",
                    "rule": "0 * * * * *"
                }
            ]
}
```
> 添加任务
```
curl -d '{"rule":"* * * * * *","cmd":"date","name":"date_test"}' "http://127.0.0.1:8585/ruqi/add_job"

response:
{
    "stat": "OK"
}
```
> 删除任务
```
curl -d '{"name":"ls_test"}' "http://127.0.0.1:8585/x/remove_job"

response:
{
    "stat": "OK"
}
```
删除任务时会删除同样 name 的所有任务

### 2.3 访问
```
http://127.0.0.1:8585/main
```

## 3 Wiki

[wiki](https://github.com/meetbill/butterfly/wiki/butterfly_ruqi)
