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


<!-- vim-markdown-toc GFM -->

* [1 需求及常用方法](#1-需求及常用方法)
    * [1.1 定时触发](#11-定时触发)
    * [1.2 定期轮询](#12-定期轮询)
* [2 使用](#2-使用)
    * [2.1 部署](#21-部署)
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

在原 crontab 基础上，添加了 auth

> 部署
```
git clone https://github.com/meetbill/butterfly.git
git clone https://github.com/meetbill/pine-Angulr.git

export butterfly_dir=$(PWD)/crontab
mkdir -p ${butterfly_dir}

cp -rf butterfly/butterfly/*  ${butterfly_dir}
cp -rf pine-Angulr/src/static ${butterfly_dir}
cp -rf pine-Angulr/src/templates ${butterfly_dir}

# install crontab
cd butterfly_examples/examples/crontab_auth
bash install
```
> 配置
```
conf/config.py  # 修改 MySQL 的配置
```

### 2.2 接口
> 查询任务
```
curl "http://127.0.0.1:8585/api/get_jobs"

response:
{
    "stat": "OK",
    "data": [
                {
                    "nexttime": "2019-11-10 17:26:00",
                    "cmd": "ls",
                    "name": "ls_test",
                    "rule": "* * * * *"
                }
            ]
}
```
> 添加任务
```
curl -d '{"rule":"* * * * *","cmd":"date","name":"date_test"}' "http://127.0.0.1:8585/api/add_job"

response:
{
    "stat": "OK"
}
```
> 删除任务
```
curl -d '{"name":"ls_test"}' "http://127.0.0.1:8585/api/remove_job"

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
![crontab](https://github.com/meetbill/butterfly_examples/blob/master/images/crontab.png)

## 3 Wiki

[wiki](https://github.com/meetbill/butterfly_examples/wiki/apscheduler)
