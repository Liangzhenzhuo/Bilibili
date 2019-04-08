# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 4:17
# @Author  : Nismison
# @FileName: database.py
# @Description: 数据库函数
# @Blog    ：https://blog.tryfang.cn

from pymysql import connect


class Database(object):
    def __init__(self, host, username, password, db_name):
        self.__connection = connect(host, username, password, db_name)
        self.__cursor = self.__connection.cursor()

    def execute_sql(self, table_name, mode="search", select="*", **kwargs):
        """
        :param table_name: 需要执行操作的表名（str）
        :param mode: 需要执行的操作（search: 查询，insert: 插入）
            search - key: 需要查询的字段（str/list）
            search -> value: 需要匹配的值（str）
            insert - keys: 需要插入的字段名（list）
            inset - values: 需要插入的数据（list）
        :return: 查询到的数据 or True/False
        """

        if mode == "search":
            if isinstance(kwargs['key'], list) and kwargs['value'] == 'all':
                key = ''
                for i in range(len(kwargs['key'])):
                    if i == len(kwargs['key']) - 1:
                        key += "{}".format(kwargs['key'][i])
                    else:
                        key += "{}".format(kwargs['key'][i]) + ", "
                sql = "select {} from {}".format(key, table_name)
                self.__cursor.execute(sql)
                return list(self.__cursor.fetchall())
            elif isinstance(kwargs['key'], str) and (isinstance(kwargs['value'], str) or isinstance(kwargs['value'], int) or isinstance(kwargs['value'], float)):
                sql = "select {} from {} where {}='{}'".format(select, table_name, kwargs['key'], kwargs['value'])
                return self.__cursor.execute(sql)
            else:
                raise TypeError("The 'key' must be a list or str type and the 'value' must be a string type.")

        elif mode == "insert":
            key = ''
            value = ''
            keys = kwargs['keys']
            values = kwargs['values']
            # 如果keys和values类型不是list，抛出异常
            if not isinstance(keys, list) or not isinstance(values, list):
                raise TypeError("The 'keys' and 'value' must be list or number type.")
            try:
                for i in range(len(keys)):
                    if i == len(keys) - 1:
                        key += "{}".format(keys[i])
                    else:
                        key += "{}".format(keys[i]) + ", "
                for i in range(len(values)):
                    if i == len(values) - 1:
                        value += "'{}'".format(values[i])
                    else:
                        value += "'{}'".format(values[i]) + ", "
                sql = "insert into {} ({}) values ({})".format(table_name, key, value)
                # 游标对象执行操作
                self.__cursor.execute(sql)
                # connection对象提交操作
                self.__connection.commit()
                return True
            except Exception as e:
                print("Exception:", e)
                return False

    def get_cursor(self):
        """
        :return: Cursor Object
        """
        return self.__cursor

    def get_connection(self):
        """
        :return: Connection Object
        """
        return self.__connection

    def close(self):
        """
        close connection and cursor
        """
        self.__cursor.close()
        self.__connection.close()
