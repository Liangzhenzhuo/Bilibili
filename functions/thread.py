# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 0:32
# @Author  : Nismison
# @FileName: thread.py
# @Description: 
# @Blog    ：https://blog.tryfang.cn

from threading import Thread


def thread_create(thread_num, method):
    """
    批量启动线程
    :param thread_num: 线程数
    :param method: 线程调用方法
    """
    # 线程池
    thread_pool = []
    # 批量创建线程放到线程池中
    for i in range(thread_num):
        th = Thread(target=method, args=(4415 + i * 2000, ))
        thread_pool.append(th)
    # 从线程池中批量启动线程
    for i in range(len(thread_pool)):
        thread_pool[i].start()
        print("线程 {} 已启动".format(i + 1))
    # 等待子线程执行结束
    for th in thread_pool:
        Thread.join(th)
