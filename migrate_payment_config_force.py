#!/usr/bin/env python3
# 强制从Oracle迁移payment_config数据到SQLite

import sqlite3

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 手动插入payment_config数据
def insert_payment_config_data():
    print("开始手动插入payment_config数据...")
    
    # 连接SQLite数据库
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        # 清空SQLite的payment_config表
        sqlite_cursor.execute("DELETE FROM payment_config")
        print("清空SQLite的payment_config表")
        
        # 插入两条记录
        records = [
            (1, '1', 3.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y', '2026-01-12 16:33:23', '2026-01-12 16:33:23'),
            (2, '2', 5.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买 高级配置', 'Y', '2026-01-13 09:25:42', '2026-01-13 09:25:42')
        ]
        
        for record in records:
            sqlite_cursor.execute(
                "INSERT INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                record
            )
            print(f"已插入记录: {record}")
        
        sqlite_conn.commit()
        print("数据提交成功")
        
        # 验证结果
        sqlite_cursor.execute("SELECT * FROM payment_config;")
        final_data = sqlite_cursor.fetchall()
        print(f"\n插入后SQLite表记录数: {len(final_data)}")
        for row in final_data:
            print(f"  {row}")
        
    except Exception as e:
        print(f"插入payment_config数据失败: {str(e)}")
        sqlite_conn.rollback()
    finally:
        # 关闭连接
        sqlite_cursor.close()
        sqlite_conn.close()

# 主函数
def main():
    print("开始插入payment_config数据...")
    insert_payment_config_data()
    print("\n操作完成！")

if __name__ == '__main__':
    main()