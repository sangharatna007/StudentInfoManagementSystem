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
    # while True:
    #     try:
    #         whether_continue_input = input('是否继续输入学生信息[y:是/n:否]：')
    #         if whether_continue_input not in ['y', 'Y', 'N', 'n']:
    #             print("输入的操作代码有误，请检查[y:是/n:否]。")
    #         else:
    #             if whether_continue_input in ['y', 'Y']:
    #                 get_stud_info()
    #             else:
    #                 print('输入学生信息完毕。')
    #                 break
    #     except:
    #         print('输入的代码有误，请重新输入。')

    return stud_info


# 增加学生信息
def add_new_student_info(stud_info, mysql_connection):
    # 身份证号码是唯一的，可以用身份证号码作为主键
    # 需要判定正在添加的学生信息是否已经存在于数据库中
    if query_student_info(2, stud_info['stud_id_card_num'], mysql_connection):
        print('该学生信息已经存在于系统中，请重新核对并输入。')
        get_stud_info()
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
def del_student_info(stud_id,mysql_connection):
    # 首先需要查询要删除的信息是否存在于数据库中。
    query_cmd = 'SELECT * FROM tbl_student_info WHERE stud_id = {};'.format(repr(stud_id))
    try:
        with mysql_connection.cursor() as cursor:
            query_result = cursor.execute(query_cmd)
    except:
        print('查询学生信息失败，请重新操作。')
        del_student_info(stud_id,mysql_connection)
    if query_result:
        print('已经查询到该生信息。')

    del_cmd = 'DELETE FROM tbl_student_info where stud_id = {};'.format(repr(stud_id))
    while True:
        weather_to_del = input('确定要删除学生信息吗？[y:确定删除/n:不要删除]：')
        if weather_to_del.strip() in ['y', 'Y']:
            try:
                with mysql_connection.cursor() as cursor:
                    cursor.execute(del_cmd)
            except:
                print('删除学生信息失败，请重新操作。')
                del_student_info(stud_id,mysql_connection)
            print('删除学生信息成功。')
            return 1
        elif weather_to_del.strip() in ['n', 'N']:
            print('删除操作已经取消。')
            return 0
        else:
            print('输入错误，请重新输入。')



# 修改学生信息
def mod_student_info(stud_id, mysql_connection):
    # 首先查询输入的信息是否存在
    query_result = query_student_info(1, mysql_connection)
    if query_result:
        print('信息查询成功。')
    else:
        print('要修改的信息不存在，请重新确认。')


# 查询学生信息
# 输入参数：
# para_flag:标志第二个参数的含义，如果为1：则代表是按照学号进行查询，如果是2，则按照身份证号码查询。
# parameter:学号或者身份证号
# mysql_connection:数据库连接
# 返回结果为1，表明已经存在，返回结果为0，表明不存在，返回值为2，表明出错。
def query_student_info(para_flag, parameter, mysql_connection):
    if para_flag == 1:
        query_cmd = 'SELECT * FROM tbl_student_info where student_id = {}'.format(repr(parameter))
    elif para_flag == 2:
        query_cmd = 'SELECT * FROM tbl_student_info where stud_id_card_num = {}'.format(repr(parameter))
    else:
        print("查询参数错误，请检查。")
        return 2
    with mysql_connection.cursor() as cursor:
        query_result = cursor.execute(query_cmd)
    if query_result == 1:
        return 1
    else:
        return 0




# 退出系统
def logout_student_manage_system(mysql_connection):

    if mysql_connection._closed == False:
        mysql_connection.close()
        print('退出系统成功。')
        return 1


# 打印帮助
def print_help_info():
    print(' \n' * 2)
    print('#'*10 + ' 学生成绩管理系统V1.0 ' + '#'*10)
    print(' ' * 5 + '1：添加学生信息')
    print(' ' * 5 + '2：删除学生信息' + ' ' * 10)
    print(' ' * 5 + '3：修改学生信息' + ' ' * 10)
    print(' ' * 5 + '4：查询学生信息' + ' ' * 10)
    print(' ' * 5 + '5：退出管理系统' + ' ' * 10)
    print('#' * 10 + ' 学生成绩管理系统V1.0 ' + '#' * 10)
    print(' \n' * 2)