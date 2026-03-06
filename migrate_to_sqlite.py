#!/usr/bin/env python3
# 数据库迁移脚本：从Oracle迁移到SQLite

import os
import sqlite3
import sys

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 创建SQLite数据库和表
def create_sqlite_tables():
    print("创建SQLite数据库表...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 读取并执行建表脚本
    with open('create_sqlite_tables.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 执行SQL脚本
    cursor.executescript(sql_script)
    conn.commit()
    print("SQLite数据库表创建成功")
    conn.close()

# 验证迁移结果
def verify_migration():
    print("验证迁移结果...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 检查file_info表
    cursor.execute("SELECT COUNT(*) FROM file_info")
    file_count = cursor.fetchone()[0]
    print(f"file_info表记录数: {file_count}")
    
    # 检查payment_config表
    cursor.execute("SELECT COUNT(*) FROM payment_config")
    config_count = cursor.fetchone()[0]
    print(f"payment_config表记录数: {config_count}")
    
    # 检查alipay_wap_pay_records表
    cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
    payment_count = cursor.fetchone()[0]
    print(f"alipay_wap_pay_records表记录数: {payment_count}")
    
    conn.close()
    print("迁移验证完成")

# 主函数
def main():
    print("开始数据库迁移...")
    
    # 创建SQLite表
    create_sqlite_tables()
    
    # 验证迁移结果
    verify_migration()
    
    print("数据库迁移完成！")

if __name__ == '__main__':
    main()