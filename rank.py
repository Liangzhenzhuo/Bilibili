# -*- coding: utf-8 -*-
# @Time    : 2019-04-07 18:44:09
# @Author  : Nismison
# @FileName: rank.py
# @Description: Bilibili排行榜爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.deal_json import dict_get
from os.path import exists
from os import mkdir


def rank_crawler():
    # 保存目录
    save_path = "rank"
    # 如果目录不存在则创建目录
    if not exists(save_path):
        mkdir(save_path)
    # rid字典
    rid_dict = {
        "全站": 0,
        "动画": 1,
        "国创相关": 168,
        "音乐": 3,
        "舞蹈": 129,
        "游戏": 4,
        "科技": 36,
        "数码": 188,
        "生活": 160,
        "鬼畜": 119,
        "时尚": 155,
        "娱乐": 5,
        "影视": 181,
    }
    # 排行时间字典
    day_dict = {
        "日排行": 1,
        "三日排行": 3,
        "周排行": 7,
        "月排行": 30,
    }
    # 遍历rid字典
    for k, v in rid_dict.items():
        rid = v
        # 遍历排行时间字典
        for k2, v2 in day_dict.items():
            day = v2
            # 拼接url
            url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(rid, day)
            res = url_get(url=url, mode="json")
            rank_list = dict_get(res, "list")
            for i in range(len(rank_list)):
                aid = dict_get(rank_list[i], "aid")  # 视频id
                author = dict_get(rank_list[i], "author")  # up主
                coins = dict_get(rank_list[i], "coins")  # 投币数
                play = dict_get(rank_list[i], "play")  # 播放数
                pts = dict_get(rank_list[i], "pts")  # 综合得分
                title = dict_get(rank_list[i], "title")  # 视频标题
                video_review = dict_get(rank_list[i], "video_review")  # 视频弹幕数（？）
                no_reprint = dict_get(rank_list[i], "no_reprint")
                if no_reprint == 1:  # 判断是否原创
                    reprint = "原创"
                else:
                    reprint = "转载"

                # 将数据保存到txt文件中，也可以导入functions.database包将数据保存到数据库中
                with open("{}/Bilibili-{}-{}.txt".format(save_path, k, k2), "a+", encoding="utf-8") as data_file:
                    data_file.write("排名: {}\n".format(i + 1))
                    data_file.write("视频id: {}\n".format(aid))
                    data_file.write("up主: {}\n".format(author))
                    data_file.write("投币数: {}\n".format(coins))
                    data_file.write("播放数: {}\n".format(play))
                    data_file.write("综合得分: {}\n".format(pts))
                    data_file.write("视频标题: {}\n".format(title))
                    data_file.write("视频弹幕数: {}\n".format(video_review))
                    data_file.write("是否原创: {}\n".format(reprint))
                    data_file.write("-" * 60 + "\n")
                    data_file.close()

                # 打印进程显示
                print("排名: {}".format(i + 1))
                print("视频id: {}".format(aid))
                print("up主: {}".format(author))
                print("投币数: {}".format(coins))
                print("播放数: {}".format(play))
                print("综合得分: {}".format(pts))
                print("视频标题: {}".format(title))
                print("视频弹幕数: {}".format(video_review))
                print("是否原创: {}".format(reprint))
                print("-" * 60)


if __name__ == "__main__":
    rank_crawler()
