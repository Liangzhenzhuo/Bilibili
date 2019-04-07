# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 3:12
# @Author  : Nismison
# @FileName: video.py
# @Description: Bilibili视频信息爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.deal_json import dict_get
from functions.database import Database
from time import strftime, gmtime


def crawler(av):
    database = Database(host="localhost", username="root", password="", db_name="bilibili")
    for av_num in range(av, 48544470):
        url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(av_num)
        get_json = url_get(url=url, mode="json")
        if dict_get(get_json, "code") != 0:
            print('错误！没有此视频！av:{}'.format(av_num))
            print('-' * 60)
            continue
        data = {}
        data['video_av'] = str(av_num)
        data['video_up'] = dict_get(get_json, "name")
        data['video_title'] = dict_get(get_json, "title")
        data['video_classification'] = dict_get(get_json, "tname")
        data['video_view'] = dict_get(get_json, "view")
        data['video_share'] = dict_get(get_json, "share")
        data['video_like'] = dict_get(get_json, "like")
        data['video_favorite'] = dict_get(get_json, "favorite")
        data['video_coin'] = dict_get(get_json, "coin")
        data['video_update'] = strftime("%Y-%m-%d %H:%M:%S", gmtime(dict_get(get_json, "ctime")))
        data['video_reply'] = dict_get(get_json, "reply")
        data['video_danmaku'] = dict_get(get_json, "danmaku")
        video_reprint = dict_get(get_json, "no_reprint")
        if video_reprint == 0:
            data['video_reprint'] = "转载" 
        else:
            data['video_reprint'] = "原创"

        db_select = database.execute_sql(table_name="video", mode="search", key="video_av", value=data['video_av'])
        if db_select != 0:
            print('错误！此视频已存在！av:{}'.format(av_num))
            print('-' * 60)
        else:
            if database.execute_sql(table_name="video", mode="insert", keys=list(data.keys()),
                                    values=list(data.values())):
                print("视频av号: {}".format(data['video_av']))
                print("作者: {}".format(data['video_up']))
                print("标题: {}".format(data['video_title']))
                print("视频分类: {}".format(data['video_classification']))
                print("观看数: {}".format(data['video_view']))
                print("分享数: {}".format(data['video_share']))
                print("点赞数: {}".format(data['video_like']))
                print("收藏数: {}".format(data['video_favorite']))
                print("投币数: {}".format(data['video_coin']))
                print("上传时间: {}".format(data['video_update']))
                print("评论数: {}".format(data['video_reply']))
                print("弹幕数: {}".format(data['video_danmaku']))
                print("性质: {}".format(data['video_reprint']))
                print("-" * 60)


if __name__ == '__main__':
    crawler(av=6000)
