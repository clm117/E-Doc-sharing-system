#!/usr/bin/env python3
# 检查SQLite数据库中是否存在alipay_wap_pay_records表

import sqlite3

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 检查表是否存在
def check_table_exists():
    print("检查alipay_wap_pay_records表是否存在...")
    
    try:
        # 连接SQLite数据库
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alipay_wap_pay_records'")
        result = cursor.fetchone()
        
        if result:
            print("✅ alipay_wap_pay_records表存在")
            
            # 检查记录数
            cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
            count = cursor.fetchone()[0]
            print(f"表中记录数: {count}")
            
            # 检查表结构
            print("\n表结构:")
            cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # 检查前5条记录
            if count > 0:
                print("\n前5条记录:")
                cursor.execute("SELECT record_id, trade_no, out_trade_no, total_amount FROM alipay_wap_pay_records LIMIT 5")
                for row in cursor.fetchall():
                    print(f"  ID: {row[0]}, 交易号: {row[1]}, 商户号: {row[2]}, 金额: {row[3]}")
        else:
            print("❌ alipay_wap_pay_records表不存在")
        
        # 关闭连接
        conn.close()
        
    except Exception as e:
        print(f"检查失败: {str(e)}")

if __name__ == '__main__':
    check_table_exists()
