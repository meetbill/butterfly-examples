---
layout: post
title: 沧海
subtitle:
date: 2020-09-21 15:10:50
category:
author: meetbill
tags:
   -
---

## 前端路由

```
state('app.canghai', {
    url: '/canghai',
    template: '<div ui-view></div>'
}).state('app.canghai.mq', {
    url: '/mq',
    templateUrl: 'static/tpl/canghai/mq.html',
    resolve: load(['static/js/controllers/canghai/mq.js'])
}).state('app.canghai.mq_msgs', {
    url: '/mq_msgs?queue_name&registry_name&page_size&page_index',
    templateUrl: 'static/tpl/canghai/mq_msgs.html',
    resolve: load(['static/js/controllers/canghai/mq_msgs.js'])
}).state('app.canghai.mq_msginfo', {
    url: '/mq_msginfo?msg_id',
    templateUrl: 'static/tpl/canghai/mq_msginfo.html',
    resolve: load(['static/js/controllers/canghai/mq_msginfo.js'])
}).state('app.canghai.mq_workerinfo', {
    url: '/mq_workerinfo?name',
    templateUrl: 'static/tpl/canghai/mq_workerinfo.html',
    resolve: load(['static/js/controllers/canghai/mq_workerinfo.js'])
}).state('app.canghai.mq_submsginfo', {
    url: '/mq_submsginfo?msg_id',
    templateUrl: 'static/tpl/canghai/mq_submsginfo.html',
    resolve: load(['static/js/controllers/canghai/mq_submsginfo.js'])
```
