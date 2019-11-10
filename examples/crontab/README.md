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
## 使用
```
git clone https://github.com/meetbill/butterfly.git
git clone https://github.com/meetbill/pine-Angulr.git

export butterfly_dir=$(PWD)/crontab
mkdir -p ${butterfly_dir}

cp -rf butterfly/butterfly/*  ${butterfly_dir}
cp -rf pine-Angulr/src/static ${butterfly_dir}
cp -rf pine-Angulr/src/templates ${butterfly_dir}

# install crontab
cd butterfly_examples/examples/crontab
bash install
```

> 访问
```
http://127.0.0.1:8585/main
```
![crontab](https://github.com/meetbill/butterfly_examples/blob/master/images/crontab.png)

## Wiki

[wiki](https://github.com/meetbill/butterfly_examples/wiki/apscheduler)
