# -*- coding: utf-8 -*-
"""

@ function: |OperateMysql: mysql数据库基本操作类
            |connect_db:   connect函数用于 connect数据库
            |select_db:    select函数用于 select
            |operate_db：   operate函数用于 update、insert、create、delete
            |close_db：     close函数用于关闭数据库连接
            --------------------------------------------------------------------
@ author:   sun-shu-bei
@ date:     2020-07-22
@ vision：  1.5.0
@ modify：
            1. 中文乱码问题修改 sun-shu-bei 2017-11-28
            2. 连接数据库时utf8编码设置 sun-shu-bei 2017-12-07
            3. 修改程序退出机制 sun-shu-bei 2018-01-04
            4. 修改程序return机制 sun-shu-bei 2018-01-23
            5. 增加Python3版本支持 sun-shu-bei 2020-07-22

"""
import pymysql
import time
import re
import sys


class OperateMysql:

    # Python class to manipulate Mysql.
    # timeout_deadline: Quit if timeout_total over timeout_deadline.
    # timeout_total : Total time the connects have cost.
    # timeout_thread: Timeout of one connect.

    def __init__(self, config):

        self._config = config
        self._cursor = None
        self._connect = None

    def connect_db(self, timeout_deadline=5, timeout_total=0, timeout_thread=1):

        try:
            is_none = OperateMysql.__config_check(self._config)

            if is_none == "false":
                return None
            else:
                pass

            self._connect = pymysql.connect(
                host=self._config['host'],
                port=int(self._config['port']),
                user=self._config['user'],
                passwd=self._config['passwd'],
                db=self._config['db'],
                charset=self._config['charset'])
        except pymysql.Error as e:
            print ("数据库连接错误：%s") % str(e)
            # reconnect if not reach timeout_deadline.
            if timeout_total < timeout_deadline:
                interval = 0.5
                timeout_total += (interval + timeout_thread)
                time.sleep(interval)
                OperateMysql.connect_db(self, timeout_total=timeout_total)
            sys.exit(1) # 只在未连接时
        else:
            self._cursor = self._connect.cursor()

    # select
    def select_db(self, sql):
        try:
            o_type = OperateMysql.__type_operate(sql)

            if o_type == "false":
                print ("sql语句 %s 语法错误") % sql
                return None
            elif o_type != 'select':
                print ("错误：请使用 operate 函数！")
                return None
            else:
                self._cursor.execute(sql)
                dict_data = self._cursor.fetchall()
                return dict_data
        except pymysql.Error as e:
            print ("数据库查询错误：%s") % str(e)
            self._connect.rollback()
            return None

    # update or delete or insert or create
    def operate_db(self, sql):
        try:
            o_type = OperateMysql.__type_operate(sql)

            if o_type == "false":
                print ("sql语句 %s 语法错误") % sql
                return None
            elif o_type == 'select':
                print ("错误：请使用 select 函数！")
                return None
            else:
                self._cursor.execute(sql)
                self._connect.commit()
        except pymysql.Error as e:
            print ("数据库更新错误：%s") % str(e)
            self._connect.rollback()
            return None

    # 执行类型检查
    @staticmethod
    def __type_operate(sql):
        re_operate = re.compile('^(?P<operate>\w+)\s+', re.I)
        match_operate = re_operate.match(sql)
        if match_operate:
            if match_operate.group("operate").lower() == 'delete':
                return 'delete'
            elif match_operate.group("operate").lower() == 'update':
                return 'update'
            elif match_operate.group("operate").lower() == 'insert':
                return 'insert'
            elif match_operate.group("operate").lower() == 'select':
                return 'select'
            elif match_operate.group("operate").lower() == 'create':
                return 'create'
            else:
                return "false"

    #  关闭 cursor 和 connect
    def close_db(self):
        self._cursor.close()
        self._connect.close()

    # config 内容检查
    @staticmethod
    def __config_check(config):
        if type(config) is not dict:
            print ("config is not dict")
            return "false"
        else:
            for key in ['host', 'port', 'user', 'passwd', 'db', 'charset']:
                if key not in config:
                    print ('config 缺失 %s') % key
                    return "false"
