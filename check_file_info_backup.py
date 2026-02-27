#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查file_info表的备份情况，尝试恢复之前的数据
"""

import cx_Oracle


def check_file_info_backup():
    """
    检查file_info表的备份情况，尝试恢复之前的数据
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
        
        print("=== 检查file_info表结构 ===")
        # 查询file_info表结构
        cursor.execute("""
            SELECT column_name, data_type, data_length, nullable
            FROM user_tab_columns
            WHERE table_name = 'FILE_INFO'
            ORDER BY column_id
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            column_name, data_type, data_length, nullable = col
            nullable_str = "NULL" if nullable == 'Y' else "NOT NULL"
            print(f"  {column_name:<30} {data_type:<15} 长度:{data_length:<6} {nullable_str}")
        
        print("\n=== 检查最近更新的记录样本 ===")
        # 查询最近更新的10条记录，查看更新效果
        cursor.execute("""
            SELECT file_name, file_author, file_isbn
            FROM file_info
            WHERE rownum <= 10
            ORDER BY file_id DESC
        """)
        
        records = cursor.fetchall()
        for record in records:
            file_name, file_author, file_isbn = record
            print(f"  文件名: {file_name}")
            print(f"  作者: {file_author}")
            print(f"  ISBN: {file_isbn}")
            print()
        
        print("\n=== 检查是否有备份表 ===")
        # 检查是否有备份表
        cursor.execute("""
            SELECT table_name
            FROM user_tables
            WHERE table_name LIKE '%FILE_INFO%' AND table_name != 'FILE_INFO'
        """)
        
        backup_tables = cursor.fetchall()
        if backup_tables:
            print("找到备份表:")
            for table in backup_tables:
                print(f"  - {table[0]}")
        else:
            print("没有找到备份表")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")


if __name__ == '__main__':
    check_file_info_backup()