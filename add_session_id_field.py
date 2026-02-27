#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向alipay_wap_pay_records表添加session_id字段
"""

import os
import sys

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cx_Oracle
    print("已导入cx_Oracle模块")
except ImportError:
    print("错误：未安装cx_Oracle模块")
    print("请使用以下命令安装：pip install cx_Oracle")
    sys.exit(1)

# 数据库连接配置
DB_CONFIG = {
    'user': 'system',               # 数据库用户名
    'password': 'oracle123',        # 数据库密码
    'dsn': 'localhost:1521/ORCLM',   # 数据库连接字符串
    'encoding': 'UTF-8'             # 字符编码
}

def execute_sql_file(file_path):
    """
    执行SQL文件中的SQL语句
    
    Args:
        file_path: SQL文件的路径
    
    Returns:
        bool: 执行成功返回True，否则返回False
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 读取SQL文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句
        sql_statements = []
        current_statement = []
        in_string = False
        string_char = ''
        
        for char in sql_content:
            if char in "'\"" and not in_string:
                in_string = True
                string_char = char
                current_statement.append(char)
            elif char == string_char and in_string:
                in_string = False
                current_statement.append(char)
            elif char == ';' and not in_string:
                current_statement.append(char)
                sql_statements.append(''.join(current_statement))
                current_statement = []
            else:
                current_statement.append(char)
        
        # 执行每个SQL语句
        for sql in sql_statements:
            sql = sql.strip()
            if sql and not sql.startswith('--'):
                print(f"执行SQL: {sql[:50]}...")
                cursor.execute(sql)
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"执行SQL文件时出错: {str(e)}")
        return False

def main():
    """
    主函数
    """
    sql_file_path = 'add_session_id_to_alipay_table.sql'
    
    if not os.path.exists(sql_file_path):
        print(f"错误：SQL文件不存在: {sql_file_path}")
        return
    
    print(f"执行SQL文件: {sql_file_path}")
    if execute_sql_file(sql_file_path):
        print("session_id字段添加成功")
    else:
        print("session_id字段添加失败")

if __name__ == '__main__':
    main()