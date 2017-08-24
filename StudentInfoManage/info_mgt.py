#/usr/bin/env python3.6
# -*- coding: utf-8 -*-


"""
@version: python 3.6.1
@author: zengyongjie
@contact: zengyongjievip@163.com
@software: PyCharm Community Edition
@file: info_mgt.py
@time: 2017/8/20 下午8:54
"""


from pymysql import connect, cursors
import pandas
import time


# 登录学生管理系统
# 参数：用户名，密码
# 返回值：登录成功的话返回数据库连接，登录失败的话返回0
def login_student_manage_system():

    while True:
        username = input('请输入用户名:')
        password = input('请输入密码：')
        if username.strip() == '' or password.strip() == '':
            print('用户名密码输出错误，请重新输入。')
        else:
            break
    try:
        mysql_connection = connect(
            user = username,
            password = password,
            host = '192.168.0.104',
            charset = 'utf8mb4',
            db = 'stud_info',
            cursorclass = cursors.DictCursor
        )

    except:
        print('连接系统数据库失败，请检查用户名密码是否正确。')
        return 0

    print('用户登录成功。')
    return mysql_connection


# 获取学生信息
def get_stud_info(mysql_connection):
    if mysql_connection._closed == False:
        stud_info = {}



        while True:
            stud_info['stud_name'] = input('请输入学生姓名：')
            if stud_info['stud_name'].strip() == '' or len(stud_info['stud_name'].strip()) == 1:
                print('输入姓名非法，请重新核对输入：')
            else:
                break

        while True:
            try:
                stud_info['stud_sex'] = int(input('请输入学生性别代码[1：男/2：女]：'))
                if stud_info['stud_sex'] not in [1, 2]:
                    print('性别代码输入错误，请重新输入。')
                else:
                    break
            except ValueError as reason:
                print('输入的数据代码有误，请重新输入。')
                continue
    else:
        print('已经与系统断开连接，请重新登录学生管理系统。')
        login_student_manage_system()

    while True:
        try:
            stud_info['stud_age'] = int(input('请输入学生年龄[1-100]：'))
            if stud_info['stud_age'] not in range(1, 101):
                print('年龄输入错误，请重新输入。')
            else:
                break
        except ValueError as reason:
            print('输入的年龄有误，请重新输入。')

    while True:
        stud_info['stud_racial'] = input('请输入学生民族：')
        if stud_info['stud_racial'] == '':
            print('民族输入错误，请重新输入。')
        else:
            break

    while True:
        stud_info['stud_id_card_num'] = input('请输入学生身份证号[长度为18位]：')
        if len(stud_info['stud_id_card_num']) != 18:
            print('学生身份证号码输入错误，请检查并重新输入。')
        else:
            break

    while True:
        stud_info['stud_address'] = str(input('请输入学生地址：'))
        if stud_info['stud_address'] == '':
            print('地址输入错误，请重新输入。')
        else:
            break
    while True:
        stud_info['stud_phone'] = input('请输入学生电话号码[11位数字]：')
        if len(stud_info['stud_phone']) != 11:
            print('学生电话号码输入错误，请重新输入。')
        else:
            break

    return stud_info


# 增加学生信息
def add_new_student_info(mysql_connection):
    # 需要判定正在添加的学生信息是否已经存在于数据库中
    stud_info = get_stud_info(mysql_connection)
    query_cmd = 'SELECT * FROM tbl_student_info where stud_id_card_num = {}'.format(repr(stud_info['stud_id_card_num']))
    with mysql_connection.cursor() as cursor:
        res = cursor.execute(query_cmd)
    if res:
        print('要添加的学生的身份证信息已经在数据库中，请重新核对，查询到的学生信息如下:')
        print(pandas.DataFrame(cursor.fetchall()))
    else:
        insert_cmd = 'INSERT INTO tbl_student_info VALUES(null, {}, {}, {}, {}, \
        {}, {}, {});'.format(
            repr(stud_info['stud_name']),
            repr(stud_info['stud_sex']),
            repr(stud_info['stud_age']),
            repr(stud_info['stud_racial']),
            repr(stud_info['stud_id_card_num']),
            repr(stud_info['stud_address']),
            repr(stud_info['stud_phone'])
        )

        with mysql_connection.cursor() as cursor:
            try:
                cursor.execute(insert_cmd)
            except:
                print('保存学生信息到数据库失败，请检查系统是否正常。')
            print('保存学生信息成功。')

# 删除学生信息
def del_student_info(mysql_connection):

    # 让用户输入学生ID，根据ID删除学生信息。
    while True:
        try:
            stud_id = int(input('请输入需要删除的学生的ID：').strip())
            break
        except ValueError:
            print('输入错误，学生ID为1-8位数之间的整数，请重新输入。')

    # 首先需要查询要删除的信息是否存在于数据库中。
    query_cmd = 'SELECT * FROM tbl_student_info WHERE stud_id = {};'.format(repr(stud_id))

    with mysql_connection.cursor() as cursor:
        query_result = cursor.execute(query_cmd)

    if query_result:
        print('已经查询到该生信息。查询到的结果如下：')
        print(pandas.DataFrame(cursor.fetchall()))

    del_cmd = 'DELETE FROM tbl_student_info where stud_id = {};'.format(repr(stud_id))
    while True:
        weather_to_del = input('确定要删除学生信息吗？[y:确定删除/n:不要删除]：')
        if weather_to_del.strip() in ['y', 'Y']:
            try:
                with mysql_connection.cursor() as cursor:
                    cursor.execute(del_cmd)
            except:
                print('删除学生信息失败，请重新操作。')
                del_student_info(mysql_connection)
            print('删除学生信息成功。')
            return 1
        elif weather_to_del.strip() in ['n', 'N']:
            print('删除操作已经取消。')
            return 0
        else:
            print('输入错误，请重新输入。')



# 修改学生信息
def mod_student_info(mysql_connection):

    # 让用户输入学生ID，根据ID删除学生信息。
    while True:
        try:
            stud_id = int(input('请输入需要修改信息的学生的ID：').strip())
            break
        except ValueError:
            print('输入错误，学生ID为1-8位数之间的整数，请重新输入。')

    # 首先查询输入的信息是否存在
    query_cmd = 'SELECT * FROM tbl_student_info where stud_id = {};'.format(repr(stud_id))
    with mysql_connection.cursor() as cursor:
        query_result = cursor.execute(query_cmd)

    if query_result:
        print('查询学生信息成功，查询到的信息如下：')
        print(pandas.DataFrame(cursor.fetchall()))

    else:
        print('没有查询到该生信息，请重新核对。')
        return 0
    print('请输入修改后的学生信息：')
    new_stud_info = get_stud_info(mysql_connection)
    update_cmd = ("UPDATE tbl_student_info set stud_name = {}, stud_age = {}, stud_sex = {}, stud_racial = {}, " +
                  "stud_address = {}, stud_phone = {}, stud_id_card_num = {} WHERE stud_id = {};").format(
        repr(new_stud_info['stud_name']),
        repr(new_stud_info['stud_age']),
        repr(new_stud_info['stud_sex']),
        repr(new_stud_info['stud_racial']),
        repr(new_stud_info['stud_address']),
        repr(new_stud_info['stud_phone']),
        repr(new_stud_info['stud_id_card_num']),
        repr(stud_id)
        )
    print(update_cmd)
    try:
        with mysql_connection.cursor() as cursor:
            update_result = cursor.execute(update_cmd)
    except:
        print('系统异常，无法修改该生信息。')
    print('修改学生信息成功。修改后的信息如下。')
    with mysql_connection.cursor() as cursor:
        result = cursor.execute(query_cmd)
        if result:
            print(pandas.DataFrame(cursor.fetchall()))
    return 1


# 查询学生信息
# 输入参数：mysql_connection:数据库连接
# 支持按照学号查询或者身份证号码查询
# 返回结果为查询出来学生信息的列表。
def query_student_info(mysql_connection):
    while True:
        try:
            query_info = int(input('请输入要查询学生的学生ID或者身份证号码：'))
            break
        except ValueError:
            print('您输入的信息有误，请重新输入，请按照提示输入要查询学生的学生ID或者身份证号码。')

    query_cmd1 = 'SELECT * FROM tbl_student_info where stud_id = {}'.format(repr(query_info))
    query_cmd2 = 'SELECT * FROM tbl_student_info where stud_id_card_num = {}'.format(repr(query_info))
    with mysql_connection.cursor() as cursor:
        res1 = cursor.execute(query_cmd1)
        if res1:
            query_result = cursor.fetchall()
            return query_result
        else:
            res2 = cursor.execute(query_cmd2)
            if res2:
                query_result = cursor.fetchall()
                print(pandas.DataFrame(query_result))
                return query_result






# 退出系统
def logout_student_manage_system(mysql_connection):

    if mysql_connection._closed == False:
        mysql_connection.close()
        print('退出系统成功。')
        return 1


# 打印帮助
def print_help_info(mysql_connection):
    print(' \n' * 2)
    print('#'*10 + ' 学生成绩管理系统V1.0 ' + '#'*10)
    print(' ' * 5 + '1：登录管理系统' + ' ' * 10)
    print(' ' * 5 + '2：添加学生信息' + ' ' * 10)
    print(' ' * 5 + '3：删除学生信息' + ' ' * 10)
    print(' ' * 5 + '4：修改学生信息' + ' ' * 10)
    print(' ' * 5 + '5：查询学生信息' + ' ' * 10)
    print(' ' * 5 + '6：导出信息报表' + ' ' * 10)
    print(' ' * 5 + '7：退出管理系统' + ' ' * 10)
    print('#' * 10 + ' 学生成绩管理系统V1.0 ' + '#' * 10)
    print(' \n' * 2)
    choose_a_operation(mysql_connection)


# 选择一项功能
def choose_a_operation(mysql_connection):
    if mysql_connection._closed == True:
        print('您尚未登录系统，登录后才能做其他操作。')
        login_student_manage_system()
    else:
        while True:
            try:
                user_input_code = int(input('请输入您的选择：').strip())
            except ValueError:
                print('您输入的不是 1-5之间的数字，请重新输入。')
            if user_input_code == 1:
                if mysql_connection._closed == False:
                    print('已经登录系统。')
                else:
                    mysql_connection = login_student_manage_system()
            elif user_input_code == 2:
                add_new_student_info(mysql_connection)
            elif user_input_code == 3:
                del_student_info(mysql_connection)
            elif user_input_code == 4:
                mod_student_info(mysql_connection)
            elif user_input_code == 5:
                print(query_student_info(mysql_connection))
            elif user_input_code == 6:
                export_info_to_excel(mysql_connection)
            elif user_input_code == 7:
                logout_student_manage_system(mysql_connection)
                return 0
            else:
                print('您输入的不是 1-5之间的数字，请重新输入。')


# 导出学生信息到excel表格中
def export_info_to_excel(mysql_connection):
    # 让用户定义导出的学号的范围
    print('使用帮助：如果您需要输入一段连续的学号范围内的学生信息，请输入1;\
    如果您需要导出学号不连续学生的学生,请输入2。')
    while True:
        try:
            choice = int(input('请输入您的选择：').strip())
        except ValueError:
            print('您的输入不符合系统的要求，')
            print('使用帮助：如果您需要输入一段连续的学号范围内的学生信息，请输入1;\
                如果您需要导出学号不连续学生的学生,请输入2。')
            continue
        if choice in [1, 2]:
            break

    if choice == 1:

        while True:

            while True:
                try:
                    stud_id_start = int(input('请输入需要导出学生信息的起始学号：').strip())
                    break
                except ValueError:
                    print('您输入的学号有误，请输入1-8位数字的学号。')

            while True:
                try:
                    stud_id_end = int(input('请输入需要导出学生信息的终止学号：').strip())
                    break
                except ValueError:
                    print('您输入的学号有误，请输入1-8位数字的学号。')

            if stud_id_start > stud_id_end:
                print('起始学号大于结束学号，无法导出，请重新输入。')
            else:
                stud_id_list = [id for id in range(stud_id_start, stud_id_end + 1)]
                break

        if len(stud_id_list):
            stud_info_to_export = []

            for stud_id in stud_id_list:
                query_cmd = "SELECT * FROM tbl_student_info WHERE stud_id = {};".format(repr(stud_id))
                with mysql_connection.cursor() as cursor:
                    cursor.execute(query_cmd)
                    if len(cursor.fetchall()):
                        stud_info_to_export.extend(cursor.fetchall())

            dt = pandas.DataFrame(stud_info_to_export)
            export_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            dt.to_excel('export_'+ export_time + '.xlsx')
            print('导出学生信息完成。')

    if choice == 2:
        stud_id_list = (input('请依次输入您需要导出信息的学生的学号，学号之间用英文逗号分割：').strip().split(','))
        stud_id_after_filter = []
        for each_id in stud_id_list:
            try:
                stud_id_after_filter.append(int(each_id))
            except:
                print('这个学号' + str(each_id) + '无效。')

        if len(stud_id_after_filter):
            stud_info_to_export = []

            for stud_id in stud_id_after_filter:
                query_cmd = "SELECT * FROM tbl_student_info WHERE stud_id = {};".format(repr(stud_id))
                with mysql_connection.cursor() as cursor:
                    cursor.execute(query_cmd)
                    if len(cursor.fetchall()):
                        stud_info_to_export.extend(cursor.fetchall())
            dt = pandas.DataFrame(stud_info_to_export)
            export_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            dt.to_excel('export_'+ export_time + '.xlsx')
            print('导出学生信息完成。')