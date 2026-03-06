#!/usr/bin/env python3
# 修复脚本：修改alipay_wap_pay_records表结构并重新迁移数据

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

# 修改表结构，允许code字段为NULL
def modify_table_structure():
    print("修改alipay_wap_pay_records表结构...")
    
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 由于SQLite不支持直接修改列约束，我们需要重建表
        # 1. 创建临时表
        cursor.execute('''
            CREATE TABLE alipay_wap_pay_records_temp (
                record_id INTEGER,
                code TEXT,
                msg TEXT,
                sub_code TEXT,
                sub_msg TEXT,
                trade_no TEXT,
                out_trade_no TEXT,
                buyer_id TEXT,
                buyer_logon_id TEXT,
                seller_id TEXT,
                seller_email TEXT,
                total_amount REAL,
                receipt_amount REAL,
                invoice_amount REAL,
                buyer_pay_amount REAL,
                point_amount REAL,
                refund_fee REAL,
                subject TEXT,
                body TEXT,
                gmt_create TEXT,
                gmt_payment TEXT,
                gmt_refund TEXT,
                gmt_close TEXT,
                file_id TEXT,
                create_time TEXT,
                update_time TEXT,
                user_id TEXT,
                app_id TEXT,
                charset TEXT,
                version TEXT,
                sign_type TEXT,
                sign TEXT,
                auth_app_id TEXT,
                fund_bill_list TEXT,
                passback_params TEXT,
                file_name TEXT,
                mobile_pay_url TEXT,
                dynamic_amount REAL,
                qr_code_url TEXT,
                file_encrypt_password TEXT,
                session_id TEXT
            )
        ''')
        print("✅ 创建临时表成功")
        
        # 2. 复制数据（如果有的话）
        cursor.execute('''
            INSERT INTO alipay_wap_pay_records_temp 
            SELECT * FROM alipay_wap_pay_records
        ''')
        print("✅ 复制数据成功")
        
        # 3. 删除原表
        cursor.execute('DROP TABLE alipay_wap_pay_records')
        print("✅ 删除原表成功")
        
        # 4. 重命名临时表
        cursor.execute('ALTER TABLE alipay_wap_pay_records_temp RENAME TO alipay_wap_pay_records')
        print("✅ 重命名表成功")
        
        # 5. 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alipay_trade_no ON alipay_wap_pay_records(trade_no)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alipay_out_trade_no ON alipay_wap_pay_records(out_trade_no)')
        print("✅ 创建索引成功")
        
        conn.commit()
        print("✅ 表结构修改完成")
        
    except Exception as e:
        print(f"修改表结构失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

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
    print("验证修复结果...")
    
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
    
    # 检查code字段是否允许NULL
    cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
    code_column = None
    for col in columns:
        if col[1] == 'code':
            code_column = col
            break
    if code_column:
        print(f"code字段类型: {code_column[2]}")
    
    # 检查前5条记录
    if count > 0:
        print("\n前5条记录:")
        cursor.execute("SELECT record_id, code, trade_no, out_trade_no, total_amount FROM alipay_wap_pay_records LIMIT 5")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, code: '{row[1]}', 交易号: {row[2]}, 商户号: {row[3]}, 金额: {row[4]}")
    
    conn.close()
    print("验证完成")

# 主函数
def main():
    print("开始修复alipay_wap_pay_records表...")
    
    # 1. 修改表结构
    modify_table_structure()
    
    # 2. 迁移全量数据
    migrate_full_data()
    
    # 3. 验证结果
    verify_result()
    
    print("修复完成！")

if __name__ == '__main__':
    main()
