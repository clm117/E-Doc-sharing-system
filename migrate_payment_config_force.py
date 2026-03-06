#!/usr/bin/env python3
# 强制从Oracle迁移payment_config数据到SQLite

import sqlite3

# 尝试导入cx_Oracle
ORACLE_AVAILABLE = False
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    print("警告：未安装cx_Oracle，无法从Oracle数据库迁移数据")

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 重新迁移payment_config数据
def migrate_payment_config():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过数据迁移")
        return
    
    print("开始强制迁移payment_config数据...")
    
    # 连接Oracle数据库
    try:
        oracle_conn = cx_Oracle.connect(**DB_CONFIG)
        oracle_cursor = oracle_conn.cursor()
        print("成功连接到Oracle数据库")
    except Exception as e:
        print(f"连接Oracle数据库失败: {str(e)}")
        return
    
    # 连接SQLite数据库
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        # 清空SQLite的payment_config表
        sqlite_cursor.execute("DELETE FROM payment_config")
        print("清空SQLite的payment_config表")
        
        # 查询Oracle中的payment_config数据，使用大写字段名
        oracle_cursor.execute("SELECT PRICE_ID, PRICE_TYPE, AMOUNT, PAYMENT_URL, DESCRIPTION, STATUS, CREATE_TIME, UPDATE_TIME FROM payment_config")
        rows = oracle_cursor.fetchall()
        
        print(f"从Oracle获取到 {len(rows)} 条记录")
        for row in rows:
            print(f"  记录: {row}")
        
        # 插入到SQLite
        count = 0
        for row in rows:
            price_id, price_type, amount, payment_url, description, status, create_time, update_time = row
            # 转换日期格式
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            # 执行插入
            sqlite_cursor.execute(
                "INSERT INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (price_id, price_type, amount, payment_url, description, status, create_time_str, update_time_str)
            )
            count += 1
            print(f"  已插入第 {count} 条记录")
        
        # 如果Oracle中没有数据，插入默认数据
        if count == 0:
            sqlite_cursor.execute(
                "INSERT INTO payment_config (price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('1', 3.00, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y', '2026-03-05 00:50:10', '2026-03-05 00:50:10')
            )
            print("插入默认支付配置数据")
        else:
            print(f"成功迁移 {count} 条payment_config记录")
        
        sqlite_conn.commit()
        print("数据提交成功")
        
        # 验证迁移结果
        sqlite_cursor.execute("SELECT * FROM payment_config;")
        final_data = sqlite_cursor.fetchall()
        print(f"\n迁移后SQLite表记录数: {len(final_data)}")
        for row in final_data:
            print(f"  {row}")
        
    except Exception as e:
        print(f"迁移payment_config表失败: {str(e)}")
        sqlite_conn.rollback()
    finally:
        # 关闭连接
        oracle_cursor.close()
        oracle_conn.close()
        sqlite_cursor.close()
        sqlite_conn.close()

# 主函数
def main():
    print("开始强制迁移payment_config表...")
    migrate_payment_config()
    print("\n操作完成！")

if __name__ == '__main__':
    main()