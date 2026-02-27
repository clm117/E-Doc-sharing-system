#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查file_info表的结构
"""

import cx_Oracle


def check_table_structure():
    """
    连接Oracle数据库，检查file_info表的结构
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查看表结构
        cursor.execute("SELECT * FROM file_info WHERE ROWNUM <= 1")
        
        # 获取列名
        columns = [col[0] for col in cursor.description]
        print(f"file_info表的列名: {columns}")
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")


if __name__ == '__main__':
    check_table_structure()
