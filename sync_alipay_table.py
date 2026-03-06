#!/usr/bin/env python3
# 同步脚本：比较Oracle和SQLite的alipay_wap_pay_records表结构并迁移数据

import sqlite3
import sys

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

# 获取SQLite表结构
def get_sqlite_table_structure():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
    columns = cursor.fetchall()
    
    structure = {}
    for col in columns:
        structure[col[1]] = col[2]
    
    conn.close()
    return structure

# 获取Oracle表结构
def get_oracle_table_structure():
    if not ORACLE_AVAILABLE:
        return {}
    
    try:
        conn = cx_Oracle.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 获取表结构
        cursor.execute("SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'")
        columns = cursor.fetchall()
        
        structure = {}
        for col in columns:
            column_name = col[0].lower()
            data_type = col[1].lower()
            # 转换Oracle数据类型到SQLite
            if 'varchar' in data_type or 'char' in data_type:
                sqlite_type = 'TEXT'
            elif 'number' in data_type or 'float' in data_type or 'double' in data_type:
                sqlite_type = 'REAL'
            elif 'int' in data_type:
                sqlite_type = 'INTEGER'
            elif 'date' in data_type or 'timestamp' in data_type:
                sqlite_type = 'TEXT'
            else:
                sqlite_type = 'TEXT'
            structure[column_name] = sqlite_type
        
        conn.close()
        return structure
    except Exception as e:
        print(f"获取Oracle表结构失败: {str(e)}")
        return {}

# 比较并更新表结构
def update_table_structure():
    print("开始比较Oracle和SQLite的alipay_wap_pay_records表结构...")
    
    # 获取两个表的结构
    sqlite_struct = get_sqlite_table_structure()
    oracle_struct = get_oracle_table_structure()
    
    print(f"SQLite表字段数: {len(sqlite_struct)}")
    print(f"Oracle表字段数: {len(oracle_struct)}")
    
    # 找出缺失的字段
    missing_fields = []
    for column, data_type in oracle_struct.items():
        if column not in sqlite_struct:
            missing_fields.append((column, data_type))
    
    if missing_fields:
        print(f"发现 {len(missing_fields)} 个缺失字段:")
        for field in missing_fields:
            print(f"  - {field[0]} ({field[1]})")
        
        # 更新SQLite表结构
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        for field_name, field_type in missing_fields:
            try:
                # 添加新字段
                cursor.execute(f"ALTER TABLE alipay_wap_pay_records ADD COLUMN {field_name} {field_type}")
                print(f"  ✅ 添加字段: {field_name} ({field_type})")
            except Exception as e:
                print(f"  ❌ 添加字段 {field_name} 失败: {str(e)}")
        
        conn.commit()
        conn.close()
    else:
        print("✅ 表结构已经与Oracle一致")

# 迁移全量数据
def migrate_full_data():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过数据迁移")
        return
    
    print("开始从Oracle迁移全量数据到SQLite...")
    
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
    
    # 获取Oracle表的所有字段
    oracle_cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'")
    oracle_columns = [col[0].lower() for col in oracle_cursor.fetchall()]
    print(f"Oracle表包含 {len(oracle_columns)} 个字段")
    
    # 构建查询语句
    columns_str = ", ".join([col.upper() for col in oracle_columns])
    query = f"SELECT {columns_str} FROM ALIPAY_WAP_PAY_RECORDS"
    
    try:
        # 执行查询
        oracle_cursor.execute(query)
        rows = oracle_cursor.fetchall()
        print(f"从Oracle获取到 {len(rows)} 条记录")
        
        if rows:
            # 清空SQLite表
            sqlite_cursor.execute("DELETE FROM alipay_wap_pay_records")
            print("已清空SQLite表")
            
            # 构建插入语句
            placeholders = ", ".join(["?"] * len(oracle_columns))
            insert_query = f"INSERT INTO alipay_wap_pay_records ({', '.join(oracle_columns)}) VALUES ({placeholders})"
            
            # 批量插入
            inserted_count = 0
            for row in rows:
                # 处理日期字段
                processed_row = []
                for i, value in enumerate(row):
                    column_name = oracle_columns[i]
                    if value and not isinstance(value, str) and ('date' in column_name or 'time' in column_name):
                        processed_row.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        processed_row.append(value)
                
                try:
                    sqlite_cursor.execute(insert_query, processed_row)
                    inserted_count += 1
                    if inserted_count % 100 == 0:
                        print(f"已插入 {inserted_count} 条记录...")
                except Exception as e:
                    print(f"插入记录失败: {str(e)}")
                    print(f"记录数据: {processed_row[:5]}...")
            
            sqlite_conn.commit()
            print(f"成功迁移 {inserted_count} 条记录")
        
    except Exception as e:
        print(f"迁移数据失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 关闭连接
    oracle_cursor.close()
    oracle_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()
    print("数据迁移完成")

# 验证结果
def verify_result():
    print("验证同步结果...")
    
    # 连接SQLite数据库
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 检查记录数
    cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
    count = cursor.fetchone()[0]
    print(f"SQLite表记录数: {count}")
    
    # 检查字段数
    cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
    columns = cursor.fetchall()
    print(f"SQLite表字段数: {len(columns)}")
    print("表字段:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # 检查前5条记录
    if count > 0:
        print("\n前5条记录:")
        cursor.execute("SELECT record_id, trade_no, out_trade_no, total_amount FROM alipay_wap_pay_records LIMIT 5")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, 交易号: {row[1]}, 商户号: {row[2]}, 金额: {row[3]}")
    
    conn.close()
    print("验证完成")

# 主函数
def main():
    print("开始同步alipay_wap_pay_records表...")
    
    # 1. 更新表结构
    update_table_structure()
    
    # 2. 迁移全量数据
    migrate_full_data()
    
    # 3. 验证结果
    verify_result()
    
    print("同步完成！")

if __name__ == '__main__':
    main()
