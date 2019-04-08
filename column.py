# -*- coding: utf-8 -*-
# @Time    : 2019-04-08 16:37:54
# @Author  : Nismison
# @FileName: column.py
# @Description: Bilibili专栏文章爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.database import Database
from functions.deal_json import dict_get
from time import strftime, localtime



def column_crawler():
    database = Database("localhost", "root", "", "bilibili")
    table_name = "zhuanlan"
    cid_dict = {
        "动画": 2,
        "游戏": 1,
        "影视": 28,
        "生活": 3,
        "兴趣": 29,
        "轻小说": 16,
        "科技": 17,
    }
    for v in cid_dict.values():
        pn = 1
        while True:
            column_url = "https://api.bilibili.com/x/article/recommends?cid={}&pn={}&ps=100&sort=0".format(v, pn)
            column_get = url_get(column_url, mode="json")
            column_data = dict_get(column_get, "data")
            if len(column_data) == 0:
                print(pn)
                break
            for item in column_data:
                data = {}
                author_info = dict_get(item, "author")  # 作者信息
                data['author_mid'] = author_info['mid']  # 作者id
                data['author_name'] = author_info['name']  # 作者用户名
                data['category'] = dict_get(item, "category")['name']  # 所属分类
                data['update_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime(dict_get(item, 'update_time')))  # 上传时间
                data['art_id'] = dict_get(item, "id")  # 文章id，如果需要爬取文章内容可以拼接url: https://www.bilibili.com/read/cv[文章id]
                data['art_title'] = dict_get(item, "title")  # 文章标题
                data['art_words'] = dict_get(item, "words")  # 文章字数
                data['art_like'] = dict_get(item, "like")  # 文章点赞数
                data['art_reply'] = dict_get(item, "reply")  # 文章评论数
                data['art_view'] = dict_get(item, "view")  # 文章浏览数
                data['art_favorite'] = dict_get(item, "favorite")  # 文章收藏数
                data['art_coin'] = dict_get(item, "coin")  # 文章投币数
                data['art_share'] = dict_get(item, "share")  # 文章分享数
                data['art_summary'] = dict_get(item, "summary")  # 文章摘要
                data['crawl_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime())  # 爬取时间

                if database.execute_sql(table_name=table_name, select="id", key="art_id", value=data['art_id']) != 0:
                    print("id:{} 重复，跳过".format(data['art_id']))
                    print("-" * 60)
                    # pn += 1
                    continue
                if database.execute_sql(table_name=table_name, mode="insert", keys=list(
                        data.keys()), values=list(data.values())):
                    print("作者id: {}".format(data['author_mid']))
                    print("作者用户名: {}".format(data['author_name']))
                    print("所属分类: {}".format(data['category']))
                    print("上传时间: {}".format(data['update_time']))
                    print("文章id: {}".format(data['art_id']))
                    print("文章标题: {}".format(data['art_title']))
                    print("文章字数: {}".format(data['art_words']))
                    print("文章点赞数: {}".format(data['art_like']))
                    print("文章评论数: {}".format(data['art_reply']))
                    print("文章浏览数: {}".format(data['art_view']))
                    print("文章收藏数: {}".format(data['art_favorite']))
                    print("文章投币数: {}".format(data['art_coin']))
                    print("文章分享数: {}".format(data['art_share']))
                    print("文章摘要: {}".format(data['art_summary']))
                    print("爬取时间: {}".format(data['crawl_time']))
                    print("-" * 60)
                else:
                    print("id:{} 异常，跳过".format(data['art_id']))
                    print("-" * 60)
                    # pn += 1
                    continue
            pn += 1

if __name__ == "__main__":
    column_crawler()
