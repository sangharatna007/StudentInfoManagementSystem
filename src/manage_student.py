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


#打印一下使用帮助
info_mgt.print_help_info()

#登录系统模块
print('请先登录系统：')
mysql_connection = info_mgt.login_student_manage_system()
if mysql_connection._closed == False:
    #获取学生信息
    stud_info = info_mgt.get_stud_info(mysql_connection)

    #添加学生信息
    info_mgt.add_new_student_info(stud_info, mysql_connection)


    #删除一条学生信息
    info_mgt.del_student_info('1', mysql_connection)


    #退出系统
    info_mgt.logout_student_manage_system(mysql_connection)
