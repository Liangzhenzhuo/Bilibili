# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 15:17
# @Author  : Nismison
# @FileName: banned.py
# @Description: Bilibili小黑屋数据爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.deal_json import dict_get
from functions.database import Database
from time import strftime, localtime


def banned_crawler():
    database = Database("localhost", "root", "", "bilibili")
    pn = 1
    while True:
        data = {}
        banned_url = "https://api.bilibili.com/x/credit/blocked/list?pn={}".format(pn)
        banned_data = url_get(banned_url, mode="json")
        if banned_data['code'] != 0:
            print("爬取完毕")
            print("-" * 60)
            return
        for item in dict_get(banned_data, "data"):
            data["banned_uname"] = dict_get(item, "uname")
            data['banned_uid'] = dict_get(item, "uid")
            data['banned_reason'] = dict_get(item, "reasonTypeName")
            data['banned_days'] = dict_get(item, "blockedDays")
            banned_time = dict_get(item, "punishTime")
            data['banned_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime(banned_time))
            if database.execute_sql(table_name="banned", mode="insert", keys=list(data.keys()), values=list(data.values())):
                print("用户名： {}".format(data["banned_uname"]))
                print("用户id： {}".format(data['banned_uid']))
                print("封禁类型： {}".format(data['banned_reason']))
                print("封禁时长： {}".format(data['banned_days']))
                print("封禁时间： {}".format(data['banned_time']))
                print("-" * 60)
        pn += 1


if __name__ == '__main__':
    banned_crawler()
