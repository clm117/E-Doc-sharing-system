#!/usr/bin/env python3
# 比较Oracle和SQLite的payment_config表结构，并重新迁移数据

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

# 检查Oracle的payment_config表结构
def check_oracle_structure():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库")
        return None
    
    print("检查Oracle的payment_config表结构...")
    try:
        conn = cx_Oracle.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 获取表结构
        cursor.execute("SELECT * FROM payment_config WHERE ROWNUM <= 1")
        columns = [desc[0] for desc in cursor.description]
        
        # 获取数据类型
        oracle_structure = {}
        for col in columns:
            # 尝试获取数据类型
            try:
                cursor.execute(f"SELECT DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'PAYMENT_CONFIG' AND COLUMN_NAME = '{col.upper()}'")
                result = cursor.fetchone()
                if result:
                    oracle_structure[col] = result[0]
                else:
                    oracle_structure[col] = "UNKNOWN"
            except:
                oracle_structure[col] = "UNKNOWN"
        
        print("Oracle表结构:")
        for col_name, col_type in oracle_structure.items():
            print(f"  {col_name}: {col_type}")
        
        # 检查数据
        cursor.execute("SELECT * FROM payment_config")
        data = cursor.fetchall()
        print(f"Oracle表数据: {len(data)} 条记录")
        for row in data:
            print(f"  {row}")
        
        conn.close()
        return oracle_structure
    except Exception as e:
        print(f"检查Oracle表结构失败: {str(e)}")
        return None

# 完善SQLite的payment_config表结构
def enhance_sqlite_structure():
    print("完善SQLite的payment_config表结构...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查是否需要添加字段
        cursor.execute("PRAGMA table_info(payment_config);")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # 可能需要添加的字段（基于Oracle常见字段）
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
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过数据迁移")
        return
    
    print("重新迁移payment_config数据...")
    
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
        
        # 插入到SQLite
        count = 0
        for row in rows:
            price_id, price_type, amount, payment_url, description, status, create_time, update_time = row
            # 转换日期格式
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            sqlite_cursor.execute(
                "INSERT INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (price_id, price_type, amount, payment_url, description, status, create_time_str, update_time_str)
            )
            count += 1
        
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
    except Exception as e:
        print(f"迁移payment_config表失败: {str(e)}")
        sqlite_conn.rollback()
    finally:
        # 关闭连接
        oracle_cursor.close()
        oracle_conn.close()
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
    
    # 检查Oracle表结构
    oracle_structure = check_oracle_structure()
    
    # 比较两个表结构
    if oracle_structure:
        print("\n比较表结构差异...")
        # 转换为小写进行比较
        sqlite_cols_lower = set(col.lower() for col in sqlite_structure.keys())
        oracle_cols_lower = set(col.lower() for col in oracle_structure.keys())
        
        common_cols = sqlite_cols_lower & oracle_cols_lower
        only_sqlite = sqlite_cols_lower - oracle_cols_lower
        only_oracle = oracle_cols_lower - sqlite_cols_lower
        
        print(f"共同字段: {common_cols}")
        print(f"仅SQLite有: {only_sqlite}")
        print(f"仅Oracle有: {only_oracle}")
    
    # 完善SQLite表结构
    enhance_sqlite_structure()
    
    # 重新迁移数据
    migrate_payment_config()
    
    # 验证迁移结果
    verify_migration()
    
    print("\n操作完成！")

if __name__ == '__main__':
    main()