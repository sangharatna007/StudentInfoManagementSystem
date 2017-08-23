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

#需要用户输入功能代码
while True:
    try:
        user_input = int(input('请输入您选择的操作代码：').strip())
    except ValueError:
        print('您输入的不是1-6之间的数字，请重新输入')
    if user_input == 1:
        pass