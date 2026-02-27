#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行表结构修改脚本
"""

import cx_Oracle

# 数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def main():
    print("开始执行表结构修改脚本...")
    
    try:
        # 连接Oracle数据库
        print("正在连接Oracle数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 执行表结构修改命令
        print("正在修改表结构...")
        
        # 修改文件大类字段为允许为空
        cursor.execute("ALTER TABLE file_info MODIFY file_major_class VARCHAR2(20) NULL")
        print("✓ 修改file_major_class字段为允许为空")
        
        # 修改文件中类字段为允许为空
        cursor.execute("ALTER TABLE file_info MODIFY file_mid_class VARCHAR2(20) NULL")
        print("✓ 修改file_mid_class字段为允许为空")
        
        # 修改文件小类字段为允许为空
        cursor.execute("ALTER TABLE file_info MODIFY file_minor_class VARCHAR2(20) NULL")
        print("✓ 修改file_minor_class字段为允许为空")
        
        # 修改下载次数字段为允许为空
        cursor.execute("ALTER TABLE file_info MODIFY download_count NUMBER NULL")
        print("✓ 修改download_count字段为允许为空")
        
        # 尝试删除约束
        try:
            cursor.execute("ALTER TABLE file_info DROP CONSTRAINT ck_file_major_class")
            print("✓ 删除ck_file_major_class约束")
        except cx_Oracle.DatabaseError:
            print("✗ ck_file_major_class约束不存在，跳过删除")
        
        try:
            cursor.execute("ALTER TABLE file_info DROP CONSTRAINT ck_file_mid_class")
            print("✓ 删除ck_file_mid_class约束")
        except cx_Oracle.DatabaseError:
            print("✗ ck_file_mid_class约束不存在，跳过删除")
        
        try:
            cursor.execute("ALTER TABLE file_info DROP CONSTRAINT ck_file_minor_class")
            print("✓ 删除ck_file_minor_class约束")
        except cx_Oracle.DatabaseError:
            print("✗ ck_file_minor_class约束不存在，跳过删除")
        
        # 提交事务
        connection.commit()
        print("\n✓ 表结构修改完成，事务已提交")
        
        # 重新检查表结构
        print("\n重新检查表结构:")
        print("-" * 60)
        print("{:<20} {:<15} {:<10} {:<10}".format("列名", "数据类型", "长度", "是否允许空"))
        print("-" * 60)
        
        cursor.execute("""
        SELECT column_name, data_type, data_length, nullable
        FROM user_tab_columns
        WHERE table_name = 'FILE_INFO'
        """)
        
        for row in cursor.fetchall():
            column_name, data_type, data_length, nullable = row
            print("{:<20} {:<15} {:<10} {:<10}".format(
                column_name, data_type, data_length, "YES" if nullable == 'Y' else "NO"
            ))
        
    except Exception as e:
        print(f"执行过程中发生错误: {str(e)}")
        # 回滚事务
        if 'connection' in locals():
            connection.rollback()
            print("✗ 事务已回滚")
    finally:
        # 关闭数据库连接
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
    print("\n执行任务结束")

if __name__ == "__main__":
    main()
