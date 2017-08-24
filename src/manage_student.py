#/usr/bin/env python3.6
# -*- coding: utf-8 -*-


"""
@version: python 3.6.1
@author: zengyongjie
@contact: zengyongjievip@163.com
@software: PyCharm Community Edition
@file: manage_student.py
@time: 2017/8/20 下午9:05
"""


from StudentInfoManage import info_mgt
from pymysql import connect, cursors, err
import sys


# 登录系统
mysql_connection = False
for retry_time in range(1,6):
    try:
        print('正在尝试第' + str(retry_time) + '次连接数据库...')
        mysql_connection = connect(
            host = '192.168.0.104',
            user = 'sa',
            password = '123456',
            db = 'stud_info',
            charset = 'utf8mb4',
            cursorclass = cursors.DictCursor

        )
        print('第' + str(retry_time) + '连接数据库成功。')
        break
    except err.OperationalError:
        print('第' + str(retry_time) + '次连接数据库失败。')
if not mysql_connection:
    print('连接数据库失败，系统退出。')
    sys.exit(1)

# 打印使用帮助，提醒用户操作选项
info_mgt.print_help_info(mysql_connection)

