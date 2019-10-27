# butterfly_examples
蝶舞示例
<div align=center><img src="https://github.com/meetbill/butterfly/blob/master/images/butterfly.png" width="350"/></div>

<!-- vim-markdown-toc GFM -->

* [Butterfly 使用手册](#butterfly-使用手册)
* [Butterfly 示例](#butterfly-示例)
* [参加步骤](#参加步骤)

<!-- vim-markdown-toc -->


## Butterfly 使用手册

[使用手册](https://github.com/meetbill/butterfly/wiki)

## Butterfly 示例

> * [Redis 资源计算器](./examples/resource-calculator)

## 参加步骤

* 在 GitHub 上 `fork` 到自己的仓库，然后 `clone` 到本地，并设置用户信息。
```
$ git clone https://github.com/meetbill/butterfly_examples.git
$ cd butterfly_examples
$ git config user.name "yourname"
$ git config user.email "your email"
```
* 修改代码后提交，并推送到自己的仓库。
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* 在 GitHub 网站上提交 pull request。
* 定期使用项目仓库内容更新自己仓库内容。
```
$ git remote add upstream https://github.com/meetbill/butterfly_examples.git
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```

