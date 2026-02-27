#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cx_Oracle

# Oracle数据库连接配置
db_config = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def check_file_info_structure():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询file_info表的结构
        cursor.execute("""
            SELECT column_name, data_type, data_length, nullable
            FROM user_tab_columns
            WHERE table_name = 'FILE_INFO'
            ORDER BY column_id
        """)
        
        columns = cursor.fetchall()
        
        print(f"表 'FILE_INFO' 共有 {len(columns)} 个列：\n")
        
        for col in columns:
            column_name, data_type, data_length, nullable = col
            nullable_str = "NULL" if nullable == 'Y' else "NOT NULL"
            print(f"  {column_name:<30} {data_type:<15} 长度:{data_length:<6} {nullable_str}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查询失败：{str(e)}")

if __name__ == '__main__':
    check_file_info_structure()