# -*- coding: utf-8 -*-
# @Time    : 2019/4/6 19:42
# @Author  : Nismison
# @FileName: pictures.py
# @Description: Bilibili相簿爬取
# @Blog    ：https://blog.tryfang.cn

from os.path import dirname, exists
from os import mkdir
from functions.requests_func import url_get


def dict_get(dict_, objkey):
    """
    从嵌套的字典中拿到需要的值
    :param dict_: 要遍历的字典
    :param objkey: 目标key
    :return: 目标key对应的value
    """
    for key, value in dict_.items():
        if key == objkey:
            return value
        else:
            # 如果value是dict类型，则迭代
            if isinstance(value, dict):
                ret = dict_get(value, objkey)
                if ret is not None:
                    return ret
            # 如果value是list类型，则取第0个进行迭代
            elif isinstance(value, list):
                ret = dict_get(value[0], objkey)
                if ret is not None:
                    return ret
    # 如果找不到指定的key，返回None
    return None


def crawler(type_, sort, path='save_picture', page_num=0):
    """
    :param type_: 分类 --> cos or sifu
    :param sort: 排序 --> hot or new
    :param path: 路径（当前目录下）
    :param page_num: 开始页，默认0页开始
    """
    if path != '' and not exists(path):
        mkdir(path)
    base_dir = dirname(__file__) + "/" + path + "/"
    url = "https://api.vc.bilibili.com/link_draw/v2/Photo/list?category={}&type={}&page_num={}&page_size=20".format(
        type_, sort, page_num)
    res = url_get(url=url, mode="json")
    items = dict_get(res, "items")
    if len(items) == 0:
        print("Current page have no any picture, Exit mission!")
        return
    for i in items:
        title = dict_get(i, "title")  # 相簿标题
        up = dict_get(i, "name")  # up主
        directory_name = title.replace("/", '').replace("<", '').replace(">", '').replace(
            "|", '').replace(":", '').replace("*", '').replace("?", '').replace("\\", '') + "-" + up
        if not exists(path + "/" + directory_name):
            mkdir(path + "/" + directory_name)
        picture_list = []  # 存放图片地址
        for picture in dict_get(i, "pictures"):
            picture_list.append(picture['img_src'])
        print("Downloading Pictures")
        for pic in picture_list:
            pic_name = pic.split("/")[-1]
            full_pic_path = base_dir + directory_name + "/" + pic_name
            if not exists(full_pic_path):
                pic_get = url_get(url=pic, mode="content")
                with open(full_pic_path, "wb") as pic_file:
                    pic_file.write(pic_get)
            else:
                continue
        print("current page: {}".format(page_num + 1))
        print("title: {}".format(title))
        print("up: {}".format(up))
        print("picture: {}".format(len(picture_list)))
        print("-" * 60)
    crawler(type_=type_, sort=sort, path=path, page_num=page_num + 1)


if __name__ == '__main__':
    crawler(type_="sifu", sort="hot")
