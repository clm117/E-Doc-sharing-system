#!/usr/bin/env python3
# 测试脚本：模拟CMD环境下的SQLite查询

import sqlite3
import os

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

def test_cmd_style_queries():
    print("=== 测试CMD风格的SQLite查询 ===")
    
    try:
        # 连接SQLite数据库
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        print("✅ 成功连接到SQLite数据库")
        
        # 测试1: 查询file_info表（用户说这个可以工作）
        print("\n1. 测试查询file_info表:")
        cursor.execute("SELECT * FROM file_info LIMIT 3")
        file_info_records = cursor.fetchall()
        print(f"   返回记录数: {len(file_info_records)}")
        for row in file_info_records:
            print(f"   ID: {row[0]}, 名称: {row[1][:30]}...")
        
        # 测试2: 查询alipay_wap_pay_records表（用户说这个不工作）
        print("\n2. 测试查询alipay_wap_pay_records表:")
        cursor.execute("SELECT * FROM alipay_wap_pay_records LIMIT 3")
        alipay_records = cursor.fetchall()
        print(f"   返回记录数: {len(alipay_records)}")
        for row in alipay_records:
            print(f"   ID: {row[0]}, 交易号: {row[5]}, 金额: {row[11]}")
        
        # 测试3: 检查表名大小写
        print("\n3. 测试表名大小写:")
        test_names = ['alipay_wap_pay_records', 'ALIPAY_WAP_PAY_RECORDS', 'Alipay_Wap_Pay_Records']
        for name in test_names:
            try:
                cursor.execute(f"SELECT * FROM {name} LIMIT 1")
                count = len(cursor.fetchall())
                print(f"   表名 '{name}': 成功 (返回 {count} 条记录)")
            except Exception as e:
                print(f"   表名 '{name}': 失败 - {e}")
        
        # 测试4: 检查SQLite命令行工具的使用方式
        print("\n4. SQLite命令行工具使用指南:")
        print("   在CMD中正确的查询方式:")
        print("   1. 进入项目目录: cd D:\\Program Files (x86)\\Trae CN\\111code")
        print("   2. 启动SQLite: sqlite3 docshare.db")
        print("   3. 执行查询: SELECT * FROM alipay_wap_pay_records LIMIT 5;")
        print("   4. 退出: .quit")
        
        # 测试5: 检查数据库文件权限
        print("\n5. 检查数据库文件权限:")
        if os.path.exists(SQLITE_DB_PATH):
            print(f"   文件存在: {SQLITE_DB_PATH}")
            print(f"   文件大小: {os.path.getsize(SQLITE_DB_PATH) / 1024:.2f} KB")
            print(f"   可读: {os.access(SQLITE_DB_PATH, os.R_OK)}")
            print(f"   可写: {os.access(SQLITE_DB_PATH, os.W_OK)}")
        else:
            print("   文件不存在")
        
        # 关闭连接
        conn.close()
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_cmd_style_queries()
