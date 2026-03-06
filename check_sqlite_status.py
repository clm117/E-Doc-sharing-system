#!/usr/bin/env python3
# 检查SQLite数据库状态

import sqlite3

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 检查数据库状态
def check_database_status():
    print("检查SQLite数据库状态...")
    
    try:
        # 连接SQLite数据库
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"数据库中的表: {[table[0] for table in tables]}")
        
        # 检查file_info表
        print("\nfile_info表结构:")
        cursor.execute("PRAGMA table_info(file_info);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM file_info")
        count = cursor.fetchone()[0]
        print(f"file_info表记录数: {count}")
        
        # 检查payment_config表
        print("\npayment_config表结构:")
        cursor.execute("PRAGMA table_info(payment_config);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM payment_config")
        count = cursor.fetchone()[0]
        print(f"payment_config表记录数: {count}")
        
        # 检查alipay_wap_pay_records表
        print("\nalipay_wap_pay_records表结构:")
        cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        count = cursor.fetchone()[0]
        print(f"alipay_wap_pay_records表记录数: {count}")
        
        # 检查前几条记录
        print("\nfile_info表前3条记录:")
        cursor.execute("SELECT file_id, file_name, create_time FROM file_info LIMIT 3")
        for row in cursor.fetchall():
            print(f"  {row}")
        
        print("\npayment_config表记录:")
        cursor.execute("SELECT * FROM payment_config")
        for row in cursor.fetchall():
            print(f"  {row}")
        
        # 关闭连接
        conn.close()
        print("\n数据库状态检查完成")
        
    except Exception as e:
        print(f"检查数据库状态失败: {str(e)}")

if __name__ == '__main__':
    check_database_status()
