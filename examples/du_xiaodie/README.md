# 度小蝶
<!-- vim-markdown-toc GFM -->

* [1 使用方法](#1-使用方法)
    * [1.1 部署 butterfly + butterfly-fe](#11-部署-butterfly--butterfly-fe)
    * [1.2 部署前端服务](#12-部署前端服务)
* [2 相关修改](#2-相关修改)
* [3 todo](#3-todo)
* [4 传送门](#4-传送门)

<!-- vim-markdown-toc -->
# 1 使用方法

## 1.1 部署 butterfly + butterfly-fe

https://github.com/meetbill/butterfly/wiki/butterfly_deploy

## 1.2 部署前端服务

> 拷贝静态文件
```
export butterfly_dir=$(PWD)/butterfly_project
cp -rf ./DuXiaoDie ${butterfly_dir}/static
```
> 修改 index.html, 将这一行代码加入 <head> 或 <body>，即可展现出效果(建议加到 body)
```
<script src="static/DuXiaoDie/autoload.js"></script>
```

# 2 相关修改

> 将看板娘放到右侧 (static/DuXiaoDie/waifu.css)
```
#waifu {
	bottom: -1000px;
	right: 0;                   // left: 0; ===> right: 0;
	line-height: 0;
	margin-bottom: -10px;
	position: fixed;
	transform: translateY(3px);
	transition: transform .3s ease-in-out, bottom 3s ease-in-out;
	z-index: 1;
}
```
> 将看板娘按钮放到了看板娘的左侧 (static/DuXiaoDie/waifu.css)
```
#waifu-tool {
	color: #aaa;
	opacity: 0;
	position: absolute;
    left: -10px;                // right: -10px; ===> left: -10px;
	top: 70px;
	transition: opacity 1s;
}
```
> 去掉了飞机大战以及更换看板娘模型及套装按钮
```
略，，就是删
```
# 3 todo

```
目前仓库不包含任何模型文件，需要向特定服务器拉取, 可以访问传送门了解更多
```

# 4 传送门

[live2d-widget](https://github.com/stevenjoezhang/live2d-widget)
