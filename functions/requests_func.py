# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 3:17
# @Author  : Nismison
# @FileName: requests_func.py
# @Description: requests函数
# @Blog    ：https://blog.tryfang.cn

from requests import get
from fake_useragent import UserAgent


def url_get(url, mode=None, timeout=20):
    # 重试次数
    retry_count = 0
    try:
        if mode is None:
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout)
        elif mode == "json":
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).json()
        elif mode == "content":
                return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).content
        elif mode == "text":
                return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).text
        elif mode == "code":
                    return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).status_code
        else:
            raise ValueError("Mode error, mode must be one of None/json/content/text/code")
    except Exception:
        if retry_count > 3:
            raise Exception("Maximum retries")
        else:
            url_get(url=url, mode=mode)
            retry_count += 1
