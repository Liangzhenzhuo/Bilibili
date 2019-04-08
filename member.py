# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 21:33
# @Author  : Nismison
# @FileName: member.py
# @Description: Bilibili会员信息爬取
# @Blog    ：https://blog.tryfang.cn

from functions.requests_func import url_get
from functions.deal_json import dict_get
from functions.database import Database
from functions.thread import thread_create


def member_crawler(mid):
    database = Database("localhost", "root", "", "bilibili")
    while True:
        follow_url = "https://api.bilibili.com/x/relation/stat?vmid={}".format(mid)
        view_url = "https://api.bilibili.com/x/space/upstat?mid={}".format(mid)
        info_url = "https://api.bilibili.com/x/space/acc/info?mid={}".format(mid)
        tag_url = "https://space.bilibili.com/ajax/member/getTags?mids={}".format(mid)
        charging_url = "https://elec.bilibili.com/api/query.rank.do?mid={}".format(mid)
        upload_data_url = "https://api.bilibili.com/x/space/navnum?mid={}".format(mid)
        try:
            member_info = url_get(info_url, mode='json')
            username = dict_get(member_info, "name")
            if username is None:
                print("该会员不存在, 跳过 {}".format(mid))
                print("-" * 60)
                mid += 1
                continue
            level = dict_get(member_info, "level")
            member_id = dict_get(member_info, "mid")
            sex = dict_get(member_info, "sex")
            coins = dict_get(member_info, "coins")
            official_data = dict_get(member_info, "official")
            follow_data = url_get(follow_url, mode="json")
            following = dict_get(follow_data, 'following')
            follower = dict_get(follow_data, 'follower')
            view = dict_get(url_get(view_url, mode="json"), "view")

            if official_data['role'] == 1:
                official = official_data['title']
            else:
                official = "暂无认证"
            birthday = dict_get(member_info, "birthday")
            sign = dict_get(member_info, "sign")
            vip = dict_get(member_info, "status")
            if vip == 1:
                vip_status = "是"
            else:
                vip_status = "否"
            tag = ''
            for x in dict_get(url_get(tag_url, mode="json"), "tags"):
                tag += x + ' '
            charging = dict_get(url_get(charging_url, mode="json"), "total_count")
            video_upload = dict_get(url_get(upload_data_url, mode="json"), "video")

            if database.execute_sql(table_name="member", mode="search", key="member_id", value=member_id) != 0:
                print("该会员已存在, 跳过 {}".format(member_id))
                print("-" * 60)
                mid += 1
                continue

            insert_data = {
                "member_id": member_id,
                "username": username,
                "sex": sex,
                "birthday": birthday,
                "level": level,
                "coins": coins,
                "sign": sign,
                "charging": charging,
                "video_upload": video_upload,
                "tag": tag,
                "vip_status": vip_status,
                "official": official,
                "following": following,
                "follower": follower,
                "view": view,
            }

            if database.execute_sql(mode="insert", table_name="member", keys=list(
                    insert_data.keys()), values=list(insert_data.values())):
                print("用户id: {}".format(member_id))
                print("用户名: {}".format(username))
                print("性别: {}".format(sex))
                print("生日: {}".format(birthday))
                print("等级: {}".format(level))
                print("B币: {}".format(coins))
                print("个人签名: {}".format(sign))
                print("充电人数: {}".format(charging))
                print("视频数量: {}".format(video_upload))
                print("标签: {}".format(tag))
                print("B站大会员: {}".format(vip_status))
                print("Bilibili认证: {}".format(official))
                print("关注数: {}".format(following))
                print("粉丝数: {}".format(follower))
                print("播放量: {}".format(view))
                print("-" * 60)
            mid += 1
        except Exception as e:
            print("错误, 跳过 mid={}".format(mid))
            print(e)
            print("-" * 60)
            mid += 1
            continue


if __name__ == '__main__':
    member_crawler(mid=0)
