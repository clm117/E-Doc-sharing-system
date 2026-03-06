#!/usr/bin/env python3
# 调试脚本：详细检查alipay_wap_pay_records表

import sqlite3

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 详细检查alipay_wap_pay_records表
def debug_alipay_table():
    print("=== 详细检查alipay_wap_pay_records表 ===")
    
    try:
        # 连接SQLite数据库
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        print("✅ 成功连接到SQLite数据库")
        
        # 1. 检查表是否存在
        print("\n1. 检查表是否存在:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alipay_wap_pay_records'")
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ alipay_wap_pay_records表存在")
        else:
            print("❌ alipay_wap_pay_records表不存在")
            conn.close()
            return
        
        # 2. 检查表结构
        print("\n2. 检查表结构:")
        cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
        columns = cursor.fetchall()
        print(f"表包含 {len(columns)} 个字段:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # 3. 检查记录数
        print("\n3. 检查记录数:")
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        count = cursor.fetchone()[0]
        print(f"表中记录数: {count}")
        
        # 4. 尝试不同的查询方式
        print("\n4. 尝试不同的查询方式:")
        
        # 方式1: 直接查询所有记录
        print("  方式1: SELECT * FROM alipay_wap_pay_records LIMIT 5")
        cursor.execute("SELECT * FROM alipay_wap_pay_records LIMIT 5")
        records1 = cursor.fetchall()
        print(f"  返回记录数: {len(records1)}")
        if records1:
            print("  第一条记录: ", records1[0][:5])  # 只显示前5个字段
        
        # 方式2: 查询特定字段
        print("\n  方式2: SELECT record_id, trade_no, out_trade_no, total_amount FROM alipay_wap_pay_records LIMIT 5")
        cursor.execute("SELECT record_id, trade_no, out_trade_no, total_amount FROM alipay_wap_pay_records LIMIT 5")
        records2 = cursor.fetchall()
        print(f"  返回记录数: {len(records2)}")
        for row in records2:
            print(f"  ID: {row[0]}, 交易号: {row[1]}, 商户号: {row[2]}, 金额: {row[3]}")
        
        # 方式3: 按条件查询
        print("\n  方式3: SELECT * FROM alipay_wap_pay_records WHERE record_id = 5021")
        cursor.execute("SELECT * FROM alipay_wap_pay_records WHERE record_id = 5021")
        records3 = cursor.fetchall()
        print(f"  返回记录数: {len(records3)}")
        if records3:
            print("  找到记录: ", records3[0][:3])  # 只显示前3个字段
        
        # 5. 检查数据库文件大小
        print("\n5. 检查数据库文件信息:")
        import os
        if os.path.exists(SQLITE_DB_PATH):
            file_size = os.path.getsize(SQLITE_DB_PATH)
            print(f"数据库文件大小: {file_size / 1024:.2f} KB")
        else:
            print("数据库文件不存在")
        
        # 6. 检查是否有其他相关表
        print("\n6. 检查相关表:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%alipay%'")
        related_tables = cursor.fetchall()
        print("与alipay相关的表:", [table[0] for table in related_tables])
        
        # 7. 检查索引
        print("\n7. 检查索引:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='alipay_wap_pay_records'")
        indexes = cursor.fetchall()
        print("表的索引:", [idx[0] for idx in indexes])
        
        # 8. 检查事务状态
        print("\n8. 检查事务状态:")
        cursor.execute("PRAGMA foreign_keys")
        foreign_keys = cursor.fetchone()[0]
        print(f"外键约束: {'启用' if foreign_keys else '禁用'}")
        
        # 关闭连接
        conn.close()
        print("\n=== 检查完成 ===")
        
    except Exception as e:
        print(f"检查失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_alipay_table()
