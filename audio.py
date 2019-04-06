# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 0:49
# @Author  : Nismison
# @FileName: audio.py
# @Description: bilibili 音频爬取
# @Blog    ：https://blog.tryfang.cn

from requests import get
from fake_useragent import UserAgent
from os.path import dirname, exists
from os import mkdir


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


def audio_crawler(path='songs'):
    """
    音频爬取函数
    :param path: 提供自定义下载路径修改
    :return: None
    """
    # 规定基础路径
    base_dir = dirname(__file__) + "/" + path + "/"
    # 如果路径不存在则创建路径
    if not exists(base_dir):
        mkdir(base_dir)
    # 构造请求头
    headers = {
        "User-Agent": UserAgent().random
    }
    # 从12032-20000遍历sid，生成专辑url
    for sid in range(12032, 20000):
        # 拼接专辑url
        url = "https://www.bilibili.com/audio/music-service-c/web/song/of-menu?sid={}&pn=1&ps=100".format(sid)
        res = get(url=url, headers=headers)
        data = dict_get(res.json(), "data")
        # 如果data为空，则跳过
        if data is None:
            continue
        items = dict_get(data, "data")
        # 获取专辑信息请求
        info_url = "https://www.bilibili.com/audio/music-service-c/web/menu/info?sid={}".format(sid)
        info_get = get(url=info_url, headers=headers).json()
        album_title = dict_get(info_get, "title").replace("/", '').replace("<", '').replace(">", '').replace(
            "|", '').replace(":", '').replace("*", '').replace("?", '').replace("\\", '')
        # 如果路径不存在则创建路径
        if not exists(base_dir + album_title):
            mkdir(base_dir + album_title)
        # 遍历专辑下所有音乐
        for item in items:
            author = dict_get(item, "author")  # 歌手
            title = dict_get(item, "title")  # 音乐标题
            sid = dict_get(item, "id")  # 音乐id，用于拼接音乐下载url
            songs_url = "https://www.bilibili.com/audio/music-service-c/web/url?sid={}".format(sid)
            songs_get = get(url=songs_url, headers=headers).json()
            file_size = round(dict_get(songs_get, "size") / 1024 / 1024, 2)  # 音频文件大小
            # 分析json中cdns数据，判断音频文件真实地址
            cdns = dict_get(songs_get, "cdns")
            if cdns[0] > cdns[1]:
                real_url = cdns[0]
            else:
                real_url = cdns[1]
            print("Downloading Audio")
            song_file_name = base_dir + album_title + "/" + title + " - " + author + '.m4a'
            # 如果文件已存在，则跳过
            if exists(song_file_name):
                continue
            # 下载音频文件
            song_file_get = get(real_url, headers=headers).content
            with open(song_file_name, "wb") as song:
                song.write(song_file_get)
                song.close()
            # 显示进程信息
            print("album_title: {}".format(album_title))
            print("author: {}".format(author))
            print("title: {}".format(title))
            print("file_size: {} MB".format(file_size))
            print("-" * 60)


if __name__ == '__main__':
    audio_crawler()
