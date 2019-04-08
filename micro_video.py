# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 20:46
# @Author  : Nismison
# @FileName: micro_video.py
# @Description: Bilibili小视频爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.deal_json import dict_get
from functions.database import Database


def micro_video_crawler(order='', page_num=1):
    """
    :param order: 排序方式，new为按照视频上传时间排序，默认为系统推荐
    """
    database = Database("localhost", "root", "", "bilibili")
    table_name = "micro_video"
    classification = []
    # 获取所有分类
    classification_url = "https://api.vc.bilibili.com/clip/v1/video/zonelist?page=total"
    classification_json = url_get(classification_url, "json")
    classification_data = dict_get(classification_json, "data")
    for i in classification_data:
        if classification_data[i] == '':
            continue
        for j in classification_data[i]['tags']:
            classification.append(j)

    for tag in classification:
        ps = 50  # page_size最大50
        pn = page_num  # 开始页，调用时可自定义
        while True:
            next_offset = (pn - 1) * ps
            micro_video_url = "https://api.vc.bilibili.com/clip/v1/video/search?" \
                              "page_size={}&need_playurl=0&next_offset={}&order={}" \
                              "&tag={}".format(ps, next_offset, order, tag)
            micro_video_json = url_get(micro_video_url, "json")
            items = dict_get(micro_video_json, "items")
            if len(items) == 0:
                break
            for item in items:
                video_info = {"tag": tag}
                video_info['title'] = dict_get(item, "description").replace("\n", "")  # 视频标题
                video_info['video_id'] = dict_get(item, "id")  # 视频id
                video_info['reply'] = dict_get(item, "reply")  # 视频评论数
                video_info['upload_time'] = dict_get(item, "upload_time")  # 视频上传时间
                video_info['video_size'] = round(float(dict_get(item, "video_size")) / 1024**2, 2)  # 视频文件大小，单位mb（float）
                video_info['video_time'] = dict_get(item, "video_time")  # 视频时长，单位s
                video_info['video_playurl'] = dict_get(item, "video_playurl")  # 视频播放地址
                video_info['watched_num'] = dict_get(item, "watched_num")  # 视频播放数
                video_info['name'] = dict_get(item, "name")  # 上传者用户名
                video_info['uid'] = dict_get(item, "uid")  # 上传者uid

                # 如果需要下载视频，请把下面注释去掉
                # video_content = url_get(video_info['video_playurl'], "content")  # 获取视频内容
                # video_file_name = video_info['title'][:30].replace("/", '').replace("<", '').replace(">", '').replace(
                #     "|", '').replace(":", '').replace("*", '').replace("?", '').replace("\\", '') + ".mp4"  # 拼接视频文件名
                # # 保存视频
                # with open(video_file_name, "wb") as video_file:
                #     video_file.write(video_content)
                #     video_file.close()

                # 如果不需要插入数据库，请把下面部分注释掉
                if database.execute_sql(table_name=table_name, key="video_id", value=video_info['video_id']) != 0:
                    print("视频id：{} 重复，跳过".format(video_info['video_id']))
                    print("-" * 60)
                    continue
                if database.execute_sql(table_name=table_name, mode="insert",
                                        keys=list(video_info.keys()), values=list(video_info.values())):
                    print("视频标题: {}".format(video_info['title']))
                    print("视频id: {}".format(video_info['video_id']))
                    print("视频评论数: {}".format(video_info['reply']))
                    print("视频上传时间: {}".format(video_info['upload_time']))
                    print("视频大小（mb）: {}".format(video_info['video_size']))
                    print("视频时长: {}".format(video_info['video_time']))
                    print("视频播放地址: {}".format(video_info['video_playurl']))
                    print("视频观看数: {}".format(video_info['watched_num']))
                    print("上传者用户名: {}".format(video_info['name']))
                    print("上传者id: {}".format(video_info['uid']))
                    print("-" * 60)
            pn += 1


if __name__ == '__main__':
    micro_video_crawler()
