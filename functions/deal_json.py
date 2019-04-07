# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 3:15
# @Author  : Nismison
# @FileName: deal_json.py
# @Description: json数据处理函数
# @Blog    ：https://blog.tryfang.cn

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
