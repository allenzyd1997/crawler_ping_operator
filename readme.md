# 介绍 Introduction

## Start

为保证您有所需的库，请先使用
```
pip3 install -r requirement.txt
```
进行安装

## 文件介绍

### bs4_utility.txt

实用的bs4 命令。

### crawl.py

负责获得网页链接的爬虫，生成link_list.txt文件，此文件记录了所需要的链接。如果需要改进link的选取机制，可以在里面更改appendLinkDomain函数

### grabData.py

负责根据link_list.txt文件中的链接进行访问，并进行操作。
需要更改preOperation, latOperation两个函数进行所需要的操作，针对不同的数据需要，可写入不同代码。

此文件，也是最主要的执行的文件
