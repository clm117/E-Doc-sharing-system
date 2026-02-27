#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行创建alipay_wap_pay_records表的SQL脚本
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
    print("开始执行创建alipay_wap_pay_records表的SQL脚本...")
    
    try:
        # 连接Oracle数据库
        print("正在连接Oracle数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 读取SQL脚本文件
        with open('create_alipay_wap_pay_table.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 执行SQL脚本
        print("正在执行SQL脚本...")
        
        # 分割SQL脚本为多个语句
        sql_statements = sql_script.split(';')
        
        for sql in sql_statements:
            # 跳过空语句和注释
            sql = sql.strip()
            if not sql or sql.startswith('--'):
                continue
            
            # 执行SQL语句
            cursor.execute(sql)
        
        # 提交事务
        connection.commit()
        print("✓ 表创建成功")
        
        # 查询表结构
        print("\n表结构信息:")
        print("-" * 60)
        print("{:<20} {:<15} {:<10} {:<10}".format("列名", "数据类型", "长度", "是否允许空"))
        print("-" * 60)
        
        cursor.execute("""
        SELECT column_name, data_type, data_length, nullable
        FROM user_tab_columns
        WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
        ORDER BY column_id
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
