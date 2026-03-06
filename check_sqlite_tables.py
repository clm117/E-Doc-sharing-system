#!/usr/bin/env python3
# 检查SQLite数据库表结构

import sqlite3

# SQLite数据库路径
DB_PATH = 'docshare.db'

# 检查SQLite数据库表
def check_sqlite_tables():
    print("检查SQLite数据库表...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查file_info表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_info';")
        file_info_exists = cursor.fetchone() is not None
        print(f"file_info表存在: {file_info_exists}")
        
        # 检查alipay_wap_pay_records表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alipay_wap_pay_records';")
        alipay_exists = cursor.fetchone() is not None
        print(f"alipay_wap_pay_records表存在: {alipay_exists}")
        
        # 检查payment_config表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment_config';")
        payment_config_exists = cursor.fetchone() is not None
        print(f"payment_config表存在: {payment_config_exists}")
        
        # 检查表结构
        if file_info_exists:
            print("\nfile_info表结构:")
            cursor.execute("PRAGMA table_info(file_info);")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  {column[1]} ({column[2]})")
        
        if alipay_exists:
            print("\nalipay_wap_pay_records表结构:")
            cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  {column[1]} ({column[2]})")
        
        if payment_config_exists:
            print("\npayment_config表结构:")
            cursor.execute("PRAGMA table_info(payment_config);")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  {column[1]} ({column[2]})")
        
        # 检查记录数
        print("\n记录数:")
        if file_info_exists:
            cursor.execute("SELECT COUNT(*) FROM file_info;")
            count = cursor.fetchone()[0]
            print(f"file_info表记录数: {count}")
        
        if alipay_exists:
            cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records;")
            count = cursor.fetchone()[0]
            print(f"alipay_wap_pay_records表记录数: {count}")
        
        if payment_config_exists:
            cursor.execute("SELECT COUNT(*) FROM payment_config;")
            count = cursor.fetchone()[0]
            print(f"payment_config表记录数: {count}")
        
    except Exception as e:
        print(f"检查SQLite表时出错: {str(e)}")
    finally:
        conn.close()

# 主函数
def main():
    print("开始检查SQLite数据库表...")
    check_sqlite_tables()
    print("\n检查完成！")

if __name__ == '__main__':
    main()
