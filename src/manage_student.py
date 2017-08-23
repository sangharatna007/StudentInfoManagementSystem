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
from pymysql import connect, cursors


# 登录系统
mysql_connection = connect(
    host = '192.168.0.104',
    user = 'sa',
    password = '123456',
    db = 'stud_info',
    charset = 'utf8mb4',
    cursorclass = cursors.DictCursor

)
# 打印使用帮助，提醒用户操作选项
info_mgt.print_help_info(mysql_connection)

