# 度小蝶
<!-- vim-markdown-toc GFM -->

* [1 前言](#1-前言)
* [2 使用方法](#2-使用方法)
    * [2.1 部署 butterfly + butterfly-fe](#21-部署-butterfly--butterfly-fe)
    * [2.2 部署前端服务](#22-部署前端服务)
    * [2.3 关闭看板娘](#23-关闭看板娘)
* [3 相关修改](#3-相关修改)
* [4 原理](#4-原理)
    * [4.1 启动过程](#41-启动过程)
        * [4.1.1 加载静态文件](#411-加载静态文件)
        * [4.2 初始化 initWidget](#42-初始化-initwidget)
    * [4.2 按钮样式](#42-按钮样式)
* [5 todo](#5-todo)
* [6 传送门](#6-传送门)

<!-- vim-markdown-toc -->
# 1 前言

通过此例子可以学习下使用 js 动态创建样式

# 2 使用方法

## 2.1 部署 butterfly + butterfly-fe

https://github.com/meetbill/butterfly/wiki/butterfly_deploy

## 2.2 部署前端服务

> 拷贝静态文件
```
export butterfly_dir=$(PWD)/butterfly_project
cp -rf ./DuXiaoDie ${butterfly_dir}/static
```
> 修改 index.html, 将这一行代码加入 <head> 或 <body>，即可展现出效果（建议加到 body)
```
<script src="static/DuXiaoDie/autoload.js"></script>
```
## 2.3 关闭看板娘

关闭看板娘后，会在左侧栏生成个小标签

# 3 相关修改

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
略，就是删
```
# 4 原理
## 4.1 启动过程
### 4.1.1 加载静态文件
```
if (screen.width >= 768) {
    // Promise.all(iterable) 方法返回一个 Promise 实例
	Promise.all([
		loadExternalResource(live2d_path + "waifu.css", "css"),
		loadExternalResource(live2d_path + "live2d.min.js", "js"),
		loadExternalResource(live2d_path + "waifu-tips.js", "js")
	]).then(() => {
		initWidget({
			waifuPath: live2d_path + "waifu-tips.json",
			//apiPath: "https://live2d.fghrsh.net/api/",
			cdnPath: "https://cdn.jsdelivr.net/gh/fghrsh/live2d_api/"
		});
	});
}
```
> Promise
```
Promise 是什么
    首先通过字面来看，他是一个承诺，意思就是现在我先答应你，以后一定给你兑现；
对应到代码中就是，这里有一个操作，比较费时间，浏览器接受你的操作请求，然后将他包装成一个承诺给你，这个承诺在之后的某一个时刻会兑现。
在这段时间之间，浏览器可以继续做自己的事情。

  为什么要有这样的操作？
  我们都知道 js 是一个单线程语言，所有的代码只能一行一行的执行，那么如果执行了一个耗时的操作，下面的代码只能等待它执行完成然后再执行。
这怎么行... 所以 js 一定要异步！试想一下当我们读取一个文件的时候，这个时候耗时的操作是系统读取磁盘文件，这个时候浏览器是空闲的，
我们将读取文件的操作交给浏览器，浏览器返回给我们一个承诺，会把文件读取完成然后告诉我们，让我们继续操作，这就是异步，和 java 中的 nio 的 epoll 模型是一样的；

  承诺有的时候是会搞砸的，浏览器答应帮你做这件事，但是这件事情能不能成功，那就不是浏览器能控制的了，也就是说事情会搞砸，就是抛出了异常，
既然搞砸了，那么浏览器也会告诉你，事情没有办好，但是我把错误信息带来了，你看看要怎么办吧。所以这个承诺一定会兑现，但不一定是想要的结果（要有异常处理）;

  Promise.all([new Promise(...), new Promise(...)]) 批量处理 promise 接受一个 Promise 数组作为参数；
  特点：当其中一个失败则全部失败，返回值是第一个失败的 Promise 的值；当全部成功，则执行 .then 种的内容，返回值是全部 Promise 的数组；
```
### 4.2 初始化 initWidget

```
initWidget 第一个参数为 waifu-tips.json 的路径，第二个参数为 API 地址
```

## 4.2 按钮样式

> 按钮默认样式
```
#waifu-toggle {
	background-color: #fa0;
	border-radius: 5px;
	bottom: 66px;
	color: #fff;
	cursor: pointer;
	font-size: 12px;
	left: 0;
	margin-left: -100px;         // 默认左移了 100px
	padding: 5px 2px 5px 5px;
	position: fixed;
	transition: margin-left 1s;
	width: 60px;
	writing-mode: vertical-rl;
}
```
> 当看板娘隐藏时
```
#waifu-toggle.waifu-toggle-active {
	margin-left: -40px;          // 从左移 100px ==> 40px, 这个时候会出现按钮
}
```
> 当鼠标放置按钮上时
```
#waifu-toggle.waifu-toggle-active:hover {
	margin-left: -30px;          // 从左移 40px == 左移 30px, 这个时候按钮会显示更长点
}
```

# 5 todo

```
目前仓库不包含任何模型文件，需要向特定服务器拉取，可以访问传送门了解更多
```

# 6 传送门

[live2d-widget](https://github.com/stevenjoezhang/live2d-widget)
