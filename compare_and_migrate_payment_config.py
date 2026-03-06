#!/usr/bin/env python3
# 比较Oracle和SQLite的payment_config表结构，并重新迁移数据

import sqlite3

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 检查SQLite的payment_config表结构
def check_sqlite_structure():
    print("检查SQLite的payment_config表结构...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(payment_config);")
    columns = cursor.fetchall()
    
    sqlite_structure = {}
    for col in columns:
        sqlite_structure[col[1]] = col[2]
    
    print("SQLite表结构:")
    for col_name, col_type in sqlite_structure.items():
        print(f"  {col_name}: {col_type}")
    
    # 检查数据
    cursor.execute("SELECT * FROM payment_config;")
    data = cursor.fetchall()
    print(f"SQLite表数据: {len(data)} 条记录")
    for row in data:
        print(f"  {row}")
    
    conn.close()
    return sqlite_structure

# 完善SQLite的payment_config表结构
def enhance_sqlite_structure():
    print("完善SQLite的payment_config表结构...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查是否需要添加字段
        cursor.execute("PRAGMA table_info(payment_config);")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # 可能需要添加的字段
        potential_columns = [
            ('currency', 'TEXT', 'CNY'),  # 货币类型
            ('payment_method', 'TEXT', 'alipay'),  # 支付方式
            ('expire_time', 'INTEGER', 3600),  # 支付过期时间（秒）
            ('max_amount', 'REAL', None),  # 最大金额
            ('min_amount', 'REAL', 0.01),  # 最小金额
        ]
        
        for col_name, col_type, default_value in potential_columns:
            if col_name not in existing_columns:
                if default_value is not None:
                    if isinstance(default_value, str):
                        default_clause = f"DEFAULT '{default_value}'"
                    else:
                        default_clause = f"DEFAULT {default_value}"
                else:
                    default_clause = ""
                
                alter_sql = f"ALTER TABLE payment_config ADD COLUMN {col_name} {col_type} {default_clause}"
                cursor.execute(alter_sql)
                print(f"添加字段: {col_name} ({col_type}) {default_clause}")
        
        conn.commit()
        print("SQLite表结构完善完成")
    except Exception as e:
        print(f"完善表结构失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# 重新迁移payment_config数据
def migrate_payment_config():
    print("重新迁移payment_config数据...")
    
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
        
        # 插入到SQLite
        count = 0
        for record in records:
            sqlite_cursor.execute(
                "INSERT INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                record
            )
            count += 1
        
        print(f"成功迁移 {count} 条payment_config记录")
        
        sqlite_conn.commit()
    except Exception as e:
        print(f"迁移payment_config表失败: {str(e)}")
        sqlite_conn.rollback()
    finally:
        # 关闭连接
        sqlite_cursor.close()
        sqlite_conn.close()

# 验证迁移结果
def verify_migration():
    print("验证迁移结果...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 检查表结构
    cursor.execute("PRAGMA table_info(payment_config);")
    columns = cursor.fetchall()
    print("更新后的SQLite表结构:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # 检查数据
    cursor.execute("SELECT * FROM payment_config;")
    data = cursor.fetchall()
    print(f"更新后的SQLite表数据: {len(data)} 条记录")
    for row in data:
        print(f"  {row}")
    
    conn.close()

# 主函数
def main():
    print("开始比较和迁移payment_config表...")
    
    # 检查SQLite表结构
    sqlite_structure = check_sqlite_structure()
    
    # 完善SQLite表结构
    enhance_sqlite_structure()
    
    # 重新迁移数据
    migrate_payment_config()
    
    # 验证迁移结果
    verify_migration()
    
    print("\n操作完成！")

if __name__ == '__main__':
    main()