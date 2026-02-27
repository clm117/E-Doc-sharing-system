#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行创建支付配置表的SQL脚本
并插入初始化数据
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
    'dsn': 'localhost:1521/ORCLM',   # 数据库连接字符串，使用正确的服务名
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
        print(f"尝试连接Oracle数据库: {DB_CONFIG['dsn']}")
        connection = cx_Oracle.connect(**DB_CONFIG)
        print("数据库连接成功")
        
        # 创建游标
        cursor = connection.cursor()
        
        # 读取SQL文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句（根据分号分割，但要处理字符串中的分号）
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
        print("SQL文件执行成功")
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        print("数据库连接已关闭")
        
        return True
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"数据库错误: {error.code} - {error.message}")
        return False
    except Exception as e:
        print(f"执行SQL文件时出错: {str(e)}")
        return False

def main():
    """
    主函数
    """
    # SQL文件路径
    sql_file_path = 'create_payment_config_table.sql'
    
    # 检查SQL文件是否存在
    if not os.path.exists(sql_file_path):
        print(f"错误：SQL文件不存在: {sql_file_path}")
        return
    
    # 执行SQL文件
    execute_sql_file(sql_file_path)

if __name__ == '__main__':
    main()