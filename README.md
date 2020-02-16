# [一次性爬虫系列-----**宅男福利**]()![Language](https://img.shields.io/badge/language-Python3-orange.svg)

## 项目简介

**首先感谢各位通过传送门来到这里，请star**
![图一][1]

这里有个故事，受朋友的委托去采集一位叫ycc的麻豆的图
看来看去觉得漂亮，就在twitter上搜罗了一番
随后发现此人曾经在秀人网叫gxx
随后笔者觉得整容前其实看着更有味道点
随后去搜gxx，然后就找到这个网站

**没有被墙不容易啊,请珍惜**

不过这个网站有个蛋疼的地方就是
浏览一个图集的时候，需要不断的翻页，用户体验很差
所以笔者当下决定，写个爬虫撸一遍

截止笔者发稿，一共采集到15w张图片的url，正持续下载中
为了影响人家到最小，笔者很轻柔的爬
所以也希望各位请轻柔对待

![示例][3]

## 致"宅福利"网站
   
首先跟"宅福利"这个网站的所有人说一声抱歉把您收集分享的图片给割了一波韭菜

## 前言
一次性系列，爬虫按照怎么快怎么写
所以说格式啊
代码风格啊
功能里的持久化啊
通通都没顾及

**注意:**图片的集合已经采集好了,各位只需要clone 后 直接下载就行

## 环境

    python3
    所需库:
    requests
    lxml
   
   
## 目录:
![目录][2]

    .
    ├── AISSaisi                # 爱丝图集
    ├── luyilu                  # 撸一撸图集
    ├── meiyanshe               # 魅妍社图集
    ├── meiyuanguan             # 美媛馆图集
    ├── tuinvlang               # 推女郎图集
    ├── youguo                  # 尤果图集
    ├── README.md               # readme
    ├── seeds_list.txt          # 所有图片url
    ├── image_list.txt          # 所有图集url
    ├── download_imags.py       # 图片下载
    └── download_seeds.py       # 种子下载 
   
## 启动方式

    下载种子:
    python3 download_seeds.py
    
    自动遍历该网站所有分类，然后遍历各个分类里具体的图集，并保存下url
    

[1]: ./tool/1.png
[2]: ./tool/3.png
[3]: ./tool/2.png


