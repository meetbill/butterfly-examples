# 度小蝶
<!-- vim-markdown-toc GFM -->

* [1 前言](#1-前言)
    * [1.1 live2d 技术简介](#11-live2d-技术简介)
    * [1.2 看板娘可以实现哪些功能？](#12-看板娘可以实现哪些功能)
        * [1.2.1 检测事件并弹出特定消息](#121-检测事件并弹出特定消息)
        * [1.2.2 看板娘的按钮](#122-看板娘的按钮)
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
    * [4.3 loadlive2d 及切换看板娘模型](#43-loadlive2d-及切换看板娘模型)
        * [4.3.1 如何切换看板娘模型](#431-如何切换看板娘模型)
        * [4.3.2 加载 model.json 方式，以 nepnep 为例](#432-加载-modeljson-方式以-nepnep-为例)
            * [方式 1 之 cdn （推荐）](#方式-1-之-cdn-推荐)
            * [方式 2 服务端接口获取 model.json](#方式-2-服务端接口获取-modeljson)
            * [方式 3 服务端静态文件 （推荐）](#方式-3-服务端静态文件-推荐)
        * [4.3.3 浅谈 model.json](#433-浅谈-modeljson)
    * [4.4 如何丰富看板娘的 mousemove/click 监听事件](#44-如何丰富看板娘的-mousemoveclick-监听事件)
        * [4.4.1 浅谈 event](#441-浅谈-event)
        * [4.4.2 例子之鼠标移动到帮助文档 menu 时，弹出消息](#442-例子之鼠标移动到帮助文档-menu-时弹出消息)
* [5 todo](#5-todo)
* [6 传送门](#6-传送门)

<!-- vim-markdown-toc -->
# 1 前言

通过此例子可以学习下使用 js 动态创建样式
## 1.1 live2d 技术简介

Live2D 是一种应用于电子游戏的绘图渲染技术，由日本 Cybernoids 公司开发，通过一系列的连续图像和人物建模来生成一种类似二维图像的三维模型，
换句话说就是 2D 的素材实现一定程度的 3D 效果，但只能是一定程度 3D，因为 Live 2D 人物无法大幅度转身。

## 1.2 看板娘可以实现哪些功能？

看板娘的界面本身都是静态文件，看板娘的有趣的灵魂时如何实现的？

### 1.2.1 检测事件并弹出特定消息

> 页面初始化加载弹出特定消息
```
页面初始化加载时，根据当前时间弹出不同的消息
```
> 检测 visibilitychange 事件
```
检测到 visibilitychange 事件，表示刚从其他页面切换到此画面，会弹窗想念了之类的话
```
> 检测 copy 事件
```
检测到复制事件时，进行弹出特定消息
```
> 检测鼠标 mousemove 事件
```
根据 waifu-tips.json 弹出消息
```
> 检测鼠标 click 事件
```
根据 waifu-tips.json 弹出消息
```
### 1.2.2 看板娘的按钮

在看板娘的旁边可以看到有许多按钮，可以通过丰富这些按钮功能来丰富看板娘的功能

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
## 4.3 loadlive2d 及切换看板娘模型

```
loadlive2d('live2d', 'model.json');
```
### 4.3.1 如何切换看板娘模型

切换看板娘模型即修改 model.json
### 4.3.2 加载 model.json 方式，以 nepnep 为例
#### 方式 1 之 cdn （推荐）
```
loadlive2d("live2d", `${cdnPath}model/${target}/index.json`);
如：
loadlive2d('live2d', 'https://cdn.jsdelivr.net/gh/fghrsh/live2d_api/model/HyperdimensionNeptunia/nepnep/index.json');
```
#### 方式 2 服务端接口获取 model.json
```
loadlive2d("live2d", `${apiPath}get/?id=${modelId}-${modelTexturesId}`);

如：
loadlive2d("live2d", `/duxiaodie/get/?id=${modelId}-${modelTexturesId}`);
```
butterfly 后端 handler
```
# coding=utf8
"""
# Description:
请求 模型_id- 皮肤_id 返回 model.json
"""
import os
import json
import glob

from xlib import retstat
from xlib.middleware import funcattr

__info = "api_demo"
__version = "1.0.1"


class modelList(object):
    #获取模型列表
    def get_list(self):
        # 读取数据
        with open('./data/model_list.json', 'r') as f:
            data = json.load(f)
        return data

    #获取模组名称
    def id_to_name(self, id):
        list = self.get_list()
        return list['models'][id-1]

    #转换模型名称
    def name_to_id(self, name):
        list = self.get_list()
        #$id = array_search($name, $list['models']);
        #return is_numeric($id) ? $id + 1 : false


class modelTextures(object):

    #获取材质列表
    def get_textures(self, modelName):
        #读取材质组合规则
        order_json_file = 'model/' + modelName + '/textures_order.json'
        textures = list()
        if  os.path.exists(order_json_file):
            pass
            """with open(order_json_file, "r") as f:
                order_json = json.load(f)

            tmp = list()
            for key, value in order_json.item():
                tmp2 = list()
                foreach ($v as $textures_dir) {
                    $tmp3 = array();
                    foreach (glob('../model/'.$modelName.'/'.$textures_dir.'/*') as $n => $m) $tmp3['merge'.$n] = str_replace('../model/'.$modelName.'/', '', $m);
                        $tmp2 = array_merge_recursive($tmp2, $tmp3);
                }
                foreach ($tmp2 as $v4) $tmp4[$k][] = str_replace('\/', '/', json_encode($v4));
                $tmp = self::array_exhaustive($tmp, $tmp4[$k]);                                                                    }
            foreach ($tmp as $v) $textures[] = json_decode('['.$v.']', 1);
            return $textures;"""
        else:
            textures_path_pattern = 'model/' + modelName + '/textures/*'
            textures_paths = glob.glob(textures_path_pattern)
            for path in textures_paths:
                textures.append(  path.replace('model/' + modelName + '/', '') )
        return textures

    #获取列表缓存
    def get_list(self, modelName):
        cache_file_path = 'model/' + modelName + '/textures.cache'
        ret = {}
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as f:
                textures = json.load(f)
        else:
            textures = self.get_textures(modelName)
            if textures is not None:
                textures = textures.replace("\/", "/")
                json.dump(textures, cache_file_path)
        ret["textures"] = textures
        return ret

    #获取材质名称
    def get_name(self, modelName, id):
        cache_list = self.get_list(modelName)
        return cache_list['textures'][id-1]

    #数组穷举合并
    #def array_exhaustive(self, arr1, arr2):
        #foreach ($arr2 as $k => $v) {
            #if (empty($arr1)) $out[] = $v;
            #else foreach ($arr1 as $k2 => $v2) $out[] = str_replace('"["', '","', str_replace('"]"', '","', $v2.$v));
        #} return $out;
@funcattr.api
def get(req, id):
    pass
    try:
        #获取参数 id 的值
        arg_id = id
        model_info = arg_id.split("-")
        if len(model_info) != 2:
            raise Exception("The Format of id is XX-XX ")

        modelId = (int)(model_info[0])
        modelTexturesId = (int)(model_info[1])

        model_lst = modelList()
        model_textures = modelTextures()
        #获取模型对应的名称
        modelName = model_lst.id_to_name(modelId)
        index_json = {}
        if type(modelName) == list:
            """类似于这种  ["ShizukuTalk/shizuku-48",  "ShizukuTalk/shizuku-pajama"]"""
            if modelTexturesId > 0:
                modelName = modelName[modelTexturesId -1]
            else:
                modelName = modelName[0]
            index_json_file = 'static/DuXiaoDie/model/' + modelName + '/index.json'
            with open(index_json_file, "r") as f:
                index_json = json.load(f)
        else:
            """类似于这种  "bilibili-live/22"   """
            index_json_file = 'static/DuXiaoDie/model/' + modelName + '/index.json'
            with open(index_json_file, "r") as f:
                index_json = json.load(f)
            if modelTexturesId > 0:
                modelTexturesName = model_textures .get_name(modelName, modelTexturesId)
                index_json['textures'] = modelTexturesName
        if "model" in index_json:
            index_json['model'] = 'static/DuXiaoDie/model/' + modelName  + '/' + index_json['model']
        if "pose" in index_json:
            index_json['pose'] = 'static/DuXiaoDie/model/' + modelName + '/' + index_json['pose']
        if "physics" in index_json:
            index_json['physics'] = 'static/DuXiaoDie/model/' + modelName + '/' + index_json['physics']

        textures = json.dumps(index_json['textures'])
        textures = textures.replace('texture', 'static/DuXiaoDie/model/' + modelName + '/texture')
        textures = json.loads(textures)
        index_json['textures'] = textures

        if "motions" in index_json:
            motions = json.dumps(index_json['motions'])
            motions = motions.replace('sounds', 'static/DuXiaoDie/model/'+ modelName + '/sounds')
            motions = motions.replace('motions', 'static/DuXiaoDie/model/' + modelName + '/motions')
            motions = json.loads(motions,)
            index_json['motions'] = motions

        if "expressions" in index_json:
            expressions = json.dumps( index_json['expressions'])
            expressions = expressions.replace('expressions', 'static/DuXiaoDie/model/' + modelName + '/expressions')
            expressions = json.loads(expressions)
            index_json['expressions'] = expressions

        index_json['code']  = 0
        index_json['info']  = "success"

    except Exception as e:
        index_json['code']  = -1
        index_json['info']  = "error : {}".format(e)
    return retstat.OK, index_json, [(__info, __version)]
```
使用此方式有个问题

浏览器在获取到 model.json 后，要对 model.json 中的静态文件路径进行下载，下载的时候是以 /duxiaodie/get/ 并加上 model.json 中的路径进行获取的
```
2020-07-04 17:35:57	27568	httpgateway.py:242	127.0.0.1	7AE1996CCC878C97	GET	/duxiaodie/get/static/DuXiaoDie/model/ShizukuTalk/shizuku-48/model.moc	0.000066	400	-	stat:	params:	error_msg:API Not Found	res:
```
显然是不符合预期的

#### 方式 3 服务端静态文件 （推荐）
```
loadlive2d('live2d', 'static/DuXiaoDie/model/nepnep/index.json');
```
> 如何进行切换模型
```
可以使用接口获取特定的 model 目录
然后在这里替换 model 目录，类似 cdn 方式
```
### 4.3.3 浅谈 model.json
JS 只是个驱动器，其实 Live2D 效果的实现最大的工作量是在素材资源的制作上

例如，我们看一下下面这个官方提供的案例中的 model.json 文件：
```

{
    "type":"Live2D Model Setting",
    "name":"shizuku",
    "model":"shizuku.moc",
    "textures": [
        "shizuku.1024/texture_00.png",
        "shizuku.1024/texture_01.png",
        "shizuku.1024/texture_02.png",
        "shizuku.1024/texture_03.png",
        "shizuku.1024/texture_04.png",
        "shizuku.1024/texture_05.png"
    ],
    "physics":"shizuku.physics.json",
    "pose":"shizuku.pose.json",
    "expressions": [
     {"name":"f01","file":"expressions/f01.exp.json"},
     {"name":"f02","file":"expressions/f02.exp.json"},
     {"name":"f03","file":"expressions/f03.exp.json"},
     {"name":"f04","file":"expressions/f04.exp.json"}
    ],
    "layout": {
        "center_x":0,
        "y":1.2,
        "width":2.4
    },
    "hit_areas": [
        {"name":"head", "id":"D_REF.HEAD"},
        {"name":"body", "id":"D_REF.BODY"}
    ],
    "motions": {
        "idle": [
            {"file":"motions/idle_00.mtn" ,"fade_in":2000, "fade_out":2000},
            {"file":"motions/idle_01.mtn" ,"fade_in":2000, "fade_out":2000},
            {"file":"motions/idle_02.mtn" ,"fade_in":2000, "fade_out":2000}
        ],
        "tap_body": [
            { "file":"motions/tapBody_00.mtn", "sound":"sounds/tapBody_00.mp3" },
            { "file":"motions/tapBody_01.mtn", "sound":"sounds/tapBody_01.mp3" },
            { "file":"motions/tapBody_02.mtn", "sound":"sounds/tapBody_02.mp3" }
        ],
        "pinch_in": [
            { "file":"motions/pinchIn_00.mtn", "sound":"sounds/pinchIn_00.mp3" },
            { "file":"motions/pinchIn_01.mtn", "sound":"sounds/pinchIn_01.mp3" },
            { "file":"motions/pinchIn_02.mtn", "sound":"sounds/pinchIn_02.mp3" }
        ],
        "pinch_out": [
            { "file":"motions/pinchOut_00.mtn", "sound":"sounds/pinchOut_00.mp3" },
            { "file":"motions/pinchOut_01.mtn", "sound":"sounds/pinchOut_01.mp3" },
            { "file":"motions/pinchOut_02.mtn", "sound":"sounds/pinchOut_02.mp3" }
        ],
        "shake": [
            { "file":"motions/shake_00.mtn", "sound":"sounds/shake_00.mp3","fade_in":500 },
            { "file":"motions/shake_01.mtn", "sound":"sounds/shake_01.mp3","fade_in":500 },
            { "file":"motions/shake_02.mtn", "sound":"sounds/shake_02.mp3","fade_in":500 }
        ],
        "flick_head": [
            { "file":"motions/flickHead_00.mtn", "sound":"sounds/flickHead_00.mp3" },
            { "file":"motions/flickHead_01.mtn", "sound":"sounds/flickHead_01.mp3" },
            { "file":"motions/flickHead_02.mtn", "sound":"sounds/flickHead_02.mp3" }
        ]
    }
}
```
定义了非常多的信息，例如使用的素材纹理 textures，点击区域 hit_areas，运动参数 motions 等。

其中 motions 中的 idle 表示空闲时候运动行为，.mtn 文件是 motions 单词的缩写，是 Live2D 中专有文件格式。tap_body, pinch_in 等都表示相关动作行为，在 Live2D 领域，这些关键字几乎都是约定俗成的一致，因为可以和看板娘发生交互动作的行为也就这些。

具体到每一个动作，会包含一系列的行为，例如：

```
"idle": [
    {"file":"motions/idle_00.mtn" ,"fade_in":2000, "fade_out":2000},
    {"file":"motions/idle_01.mtn" ,"fade_in":2000, "fade_out":2000},
    {"file":"motions/idle_02.mtn" ,"fade_in":2000, "fade_out":2000}
]
```
这里数组有 3 项，每一项是一个纯对象，表示一套动作或一个行为，行为的描述在.mtn 文件中，然后还有一些附加的效果，例如"fade_in"指定淡入的时间，"fade_out"指定淡出的时间。因为某些动作在切换的时候太大，太明显，无法形成连贯的行为，于是前后动作会采用淡入淡出的方式进行过渡。

"sound"属性表示相关行为所伴随的音效资源地址。

## 4.4 如何丰富看板娘的 mousemove/click 监听事件

看板娘的 mousemove/click 事件通过匹配 event.target 来弹出特定的信息

咱们看下 event 都有哪些内容

### 4.4.1 浅谈 event

> 一个 mousemove event
```
{
    altKey: false, // (只读) 当鼠标事件触发的时，如果 alt 键被按下，返回 true
    bubbles: true,
    button: 0,     // (只读) 当鼠标事件触发的时，如果鼠标按钮被按下（如果有的话），将会返回一个数值。
    buttons: 0,
    cancelBubble: false, // (只读)当鼠标事件触发的时，如果多个鼠标按钮被按下（如果有的话），将会返回一个或者多个代表鼠标按钮的数字。
    cancelable: true,
    clientX: 88,   // (只读) 鼠标指针在点击元素（DOM）中的 X 坐标
    clientY: 681,  // (只读) 鼠标指针在点击元素（DOM）中的 Y 坐标
    composed: true,
    ctrlKey: false, // (只读) 当鼠标事件触发时，如果 control 键被按下，则返回 true；
    currentTarget: null,
    defaultPrevented: false,
    detail: 0,
    eventPhase: 0,
    fromElement: span.ng-scope, // ====> object
    isTrusted: true,
    layerX: 88,
    layerY: 9,
    metaKey: false,
    movementX: 0,
    movementY: 0,
    offsetX: 89,
    offsetY: 10,
    pageX: 88,
    pageY: 681,
    path: [a, li, ul.nav.ng-scope, nav.navi.clearfix.ng-scope, div.navi-wrap, div.aside-wrap.ng-scope, div.app-aside.hidden-xs.bg-black, div#app.app.ng-scope.app-header-fixed.app-aside-fixed, body.ng-scope, html.ng-scope, document, Window],
    relatedTarget: span.ng-scope, // ====> object
    returnValue: true,
    screenX: 79,   // (只读) 鼠标指针相对于全局（屏幕）的 X 坐标
    screenY: 724,  // (只读) 鼠标指针相对于全局（屏幕）的Y坐标
    shiftKey: false,
    sourceCapabilities: {firesTouchEvents: false},
    srcElement: a, // ====> object
    target: {// ====> object a, 看板娘主要根据这个 target 进行触发对应操作
        accessKey: "",
        ariaAtomic: null,
        ariaAutoComplete: null,
        ariaBusy: null,
        ariaChecked: null,
        ariaColCount: null,
        ariaColIndex: null,
        ariaColSpan: null,
        ariaCurrent: null,
        ariaDescription: null,
        ariaDisabled: null,
        ariaExpanded: null,
        ariaHasPopup: null,
        ariaHidden: null,
        ariaKeyShortcuts: null,
        ariaLabel: null,
        ariaLevel: null,
        ariaLive: null,
        ariaModal: null,
        ariaMultiLine: null,
        ariaMultiSelectable: null,
        ariaOrientation: null,
        ariaPlaceholder: null,
        ariaPosInSet: null,
        ariaPressed: null,
        ariaReadOnly: null,
        ariaRelevant: null,
        ariaRequired: null,
        ariaRoleDescription: null,
        ariaRowCount: null,
        ariaRowIndex: null,
        ariaRowSpan: null,
        ariaSelected: null,
        ariaSort: null,
        ariaValueMax: null,
        ariaValueMin: null,
        ariaValueNow: null,
        ariaValueText: null,
        assignedSlot: null,
        attributeStyleMap: {size: 0},
        attributes: {0: ui-sref, 1: href, ui-sref: ui-sref, href: href, length: 2},
        autocapitalize: "",
        autofocus: false,
        baseURI: "http://127.0.0.1:8585/main#/app/docs",
        charset: "",
        childElementCount: 2,
        childNodes: [text, i.icon-question.icon, text, span.ng-scope],
        children: [i.icon-question.icon, span.ng-scope],
        classList: [value: ""],
        className: "",
        clientHeight: 39,
        clientLeft: 0,
        clientTop: 0,
        clientWidth: 200,
        contentEditable: "inherit",
        coords: "",
        dataset: {},
        dir: "",
        download: "",
        draggable: true,
        elementTiming: "",
        enterKeyHint: "",
        firstChild: text,
        firstElementChild: i.icon-question.icon,
        hash: "#/app/docs",
        hidden: false,
        host: "127.0.0.1:8585",
        hostname: "127.0.0.1",
        href: "http://127.0.0.1:8585/main#/app/docs",
        hrefTranslate: "",
        hreflang: "",
        id: "",
        innerHTML: "↵            <i class="icon-question icon"></i>↵            <span translate="aside.nav.your_stuff.DOCUMENTS" class="ng-scope">帮助文档</span>",
        innerText: "帮助文档",   // ===========> 对应文字
        inputMode: "",
        isConnected: true,
        isContentEditable: false,
        jQuery224058537375354409191: {events: {…}, handle: ƒ},
        lang: "",
        lastChild: span.ng-scope,
        lastElementChild: span.ng-scope,
        localName: "a",
        name: "",
        namespaceURI: "http://www.w3.org/1999/xhtml",
        nextElementSibling: null,
        nextSibling: text,
        nodeName: "A",
        nodeType: 1,
        nodeValue: null,
        nonce: "",
        offsetHeight: 39,
        offsetLeft: 0,
        offsetParent: li,
        offsetTop: 0,
        offsetWidth: 200,
        onabort: null,
        onanimationend: null,
        onanimationiteration: null,
        onanimationstart: null,
        onauxclick: null,
        onbeforecopy: null,
        onbeforecut: null,
        onbeforepaste: null,
        onbeforexrselect: null,
        onblur: null,
        oncancel: null,
        oncanplay: null,
        oncanplaythrough: null,
        onchange: null,
        onclick: null,
        onclose: null,
        oncontextmenu: null,
        oncopy: null,
        oncuechange: null,
        oncut: null,
        ondblclick: null,
        ondrag: null,
        ondragend: null,
        ondragenter: null,
        ondragleave: null,
        ondragover: null,
        ondragstart: null,
        ondrop: null,
        ondurationchange: null,
        onemptied: null,
        onended: null,
        onerror: null,
        onfocus: null,
        onformdata: null,
        onfullscreenchange: null,
        onfullscreenerror: null,
        ongotpointercapture: null,
        oninput: null,
        oninvalid: null,
        onkeydown: null,
        onkeypress: null,
        onkeyup: null,
        onload: null,
        onloadeddata: null,
        onloadedmetadata: null,
        onloadstart: null,
        onlostpointercapture: null,
        onmousedown: null,
        onmouseenter: null,
        onmouseleave: null,
        onmousemove: null,
        onmouseout: null,
        onmouseover: null,
        onmouseup: null,
        onmousewheel: null,
        onpaste: null,
        onpause: null,
        onplay: null,
        onplaying: null,
        onpointercancel: null,
        onpointerdown: null,
        onpointerenter: null,
        onpointerleave: null,
        onpointermove: null,
        onpointerout: null,
        onpointerover: null,
        onpointerrawupdate: null,
        onpointerup: null,
        onprogress: null,
        onratechange: null,
        onreset: null,
        onresize: null,
        onscroll: null,
        onsearch: null,
        onseeked: null,
        onseeking: null,
        onselect: null,
        onselectionchange: null,
        onselectstart: null,
        onstalled: null,
        onsubmit: null,
        onsuspend: null,
        ontimeupdate: null,
        ontoggle: null,
        ontransitionend: null,
        onvolumechange: null,
        onwaiting: null,
        onwebkitanimationend: null,
        onwebkitanimationiteration: null,
        onwebkitanimationstart: null,
        onwebkitfullscreenchange: null,
        onwebkitfullscreenerror: null,
        onwebkittransitionend: null,
        onwheel: null,
        origin: "http://127.0.0.1:8585",
        outerHTML: "<a ui-sref="app.docs" href="#/app/docs">↵            <i class="icon-question icon"></i>↵            <span translate="aside.nav.your_stuff.DOCUMENTS" class="ng-scope">帮助文档</span></a>",
        outerText: "帮助文档",
        ownerDocument: document,
        parentElement: li,
        parentNode: li,
        part: [value: ""],
        password: "",
        pathname: "/main",
        ping: "",
        port: "8585",
        prefix: null,
        previousElementSibling: null,
        previousSibling: text,
        protocol: "http:",
        referrerPolicy: "",
        rel: "",
        relList: [value: ""],
        rev: "",
        scrollHeight: 40,
        scrollLeft: 0,
        scrollTop: 0,
        scrollWidth: 200,
        search: "",
        shadowRoot: null,
        shape: "",
        slot: "",
        spellcheck: true,
        style: {alignContent: "", alignItems: "", alignSelf: "", alignmentBaseline: "", all: "", …},
        tabIndex: 0,
        tagName: "A",
        target: "",
        text: "↵            ↵            帮助文档"textContent: "↵            ↵            帮助文档",
        title: "",
        translate: true,
        type: "",
        username: ""
    },
    timeStamp: 72896.56000002287,
    toElement: a,
    type: "mouseover",
    view: {parent: Window, opener: null, top: Window, length: 0, frames: Window, …},
    which: 0,
    x: 88,
    y: 681
}
```

### 4.4.2 例子之鼠标移动到帮助文档 menu 时，弹出消息

> waifu-tips.json
```
{
    "mousemove": [
        {
            "selector": "a[href$='/docs']",
            "text": ["要去看看 <span>{text}</span> 么？"]
	    }
    ]
}
```
> 通过 event.target.innerText 替换文字
```
let text = randomSelection(tips.text);
text = text.replace("{text}", event.target.innerText);
```

这样，当鼠标移动到帮助文档 menu 时，就会弹出 "要去看看 帮助文档 么"

# 5 todo

```
目前仓库不包含任何模型文件，需要向特定服务器拉取，可以访问传送门了解更多
```

# 6 传送门

> * 前端之 [live2d-widget](https://github.com/stevenjoezhang/live2d-widget)
> * 后端之 [live2d_api](https://github.com/fghrsh/live2d_api) 模型可以在这里找到哈
> * 模型 [imuncle/live2d](https://github.com/imuncle/live2d)
