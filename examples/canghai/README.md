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
}).state('app.canghai.mq_jobs', {
    url: '/mq_jobs?queue_name&registry_name&page_size&page_index',
    templateUrl: 'static/tpl/canghai/mq_jobs.html',
    resolve: load(['static/js/controllers/canghai/mq_jobs.js'])
}).state('app.canghai.mq_jobinfo', {
    url: '/mq_jobinfo?job_id',
    templateUrl: 'static/tpl/canghai/mq_jobinfo.html',
    resolve: load(['static/js/controllers/canghai/mq_jobinfo.js'])
})
```
