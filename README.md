# Bilibili网站爬虫
![][8] ![][9] ![][10] ![][11]



-------------
我胖虎今天就是要把b站爬完
--------

 
 
 ---------------------
 - [video.py][3] - Bilibili视频信息爬取
 > 从av100逐一递增遍历视频信息，并录入数据库
 
 
 ---------------------
 - [rank.py][4] - Bilibili排行榜数据爬取
 > 爬取排行榜数据，可自定义爬取分类以及排行榜时间
 
 
 ---------------------
 - [pictures.py][5] - Bilibili相簿图片爬取
 > 爬取相簿图片，并下载至本地
 
 
 ---------------------
 - [member.py][6] - Bilibili会员信息数据爬取
 > 从id0开始逐一递增，爬取所有会员信息，并录入数据库，但是由于会员数量过于庞大，至少有2500w+，我试过同时开20个进程同时爬取，但是由于请求过于频繁，ip被封掉了，但是思路已经摆在这了，有ip代理的话问题不大
 
 
 ---------------------
 - [audio.py][7] - Bilibili音频爬取下载
 > 爬取音频专辑id，从12000逐一递增爬取，并将音乐下载至本地
 


-------------


Bilibili视频地址:[https://space.bilibili.com/25216986][2]
============
个人博客: [https://blog.tryfang.cn][1]，欢迎前来交流
=============


[1]:https://blog.tryfang.cn
[2]:https://space.bilibili.com/25216986
[3]:https://github.com/Liangzhenzhuo/Bilibili/blob/master/video.py
[4]:https://github.com/Liangzhenzhuo/Bilibili/blob/master/rank.py
[5]:https://github.com/Liangzhenzhuo/Bilibili/blob/master/pictures.py
[6]:https://github.com/Liangzhenzhuo/Bilibili/blob/master/member.py
[7]:https://github.com/Liangzhenzhuo/Bilibili/blob/master/audio.py
[8]:https://img.shields.io/badge/Python-v3.7.1-brightgreen.svg
[9]:https://img.shields.io/badge/requests-2.21-green.svg
[10]:https://img.shields.io/badge/pymysql-0.9.3-red.svg
[11]:https://img.shields.io/badge/Bilibili-%E5%B9%B2%E6%9D%AF-ff69b4.svg
