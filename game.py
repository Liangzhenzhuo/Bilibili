# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 20:19
# @Author  : Nismison
# @FileName: game.py
# @Description: Bilibili游戏列表爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.database import Database
from functions.deal_json import dict_get


def game_crawler():
    database = Database("localhost", "root", "", "bilibili")
    table_name = "game_list"
    game_list_url = "https://game.bilibili.com/gamelist.json"
    game_list_json = url_get(game_list_url, "json")
    for game in game_list_json:
        game_info = {}
        game_info['name'] = dict_get(game, "title")
        game_info['summary'] = dict_get(game, "summary")
        game_info['website'] = dict_get(game, "website")

        if database.execute_sql(table_name=table_name, key="name", value=game_info['name']) != 0:
            print("{} 重复，跳过".format(game_info['name']))
            print("-" * 60)

        if database.execute_sql(table_name=table_name, mode="insert", keys=list(game_info.keys()), values=list(game_info.values())):
            print("游戏名: {}".format(game_info['name']))
            print("游戏介绍: {}".format(game_info['summary']))
            print("游戏官网: {}".format(game_info['website']))
            print("-" * 60)


if __name__ == '__main__':
    game_crawler()
