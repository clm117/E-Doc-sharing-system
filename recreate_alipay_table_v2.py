#!/usr/bin/env python3
# 重建脚本v2：彻底重建alipay_wap_pay_records表并迁移数据（添加trade_status字段）

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

# 重建表结构
def recreate_table():
    print("重建alipay_wap_pay_records表结构...")
    
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alipay_wap_pay_records'")
        if cursor.fetchone():
            # 2. 删除原表
            cursor.execute('DROP TABLE alipay_wap_pay_records')
            print("✅ 删除原表成功")
        
        # 3. 创建新表，包含所有Oracle字段
        cursor.execute('''
            CREATE TABLE alipay_wap_pay_records (
                file_id TEXT,
                user_id TEXT,
                record_id INTEGER,
                trade_no TEXT,
                out_trade_no TEXT,
                app_id TEXT,
                total_amount REAL,
                seller_id TEXT,
                seller_email TEXT,
                buyer_id TEXT,
                buyer_logon_id TEXT,
                trade_status TEXT,
                gmt_create TEXT,
                gmt_payment TEXT,
                gmt_refund TEXT,
                gmt_close TEXT,
                subject TEXT,
                body TEXT,
                charset TEXT,
                version TEXT,
                sign_type TEXT,
                sign TEXT,
                auth_app_id TEXT,
                point_amount REAL,
                invoice_amount REAL,
                fund_bill_list TEXT,
                passback_params TEXT,
                file_name TEXT,
                mobile_pay_url TEXT,
                dynamic_amount REAL,
                qr_code_url TEXT,
                create_time TEXT,
                update_time TEXT,
                file_encrypt_password TEXT,
                session_id TEXT,
                code TEXT,
                msg TEXT,
                sub_code TEXT,
                sub_msg TEXT,
                receipt_amount REAL,
                buyer_pay_amount REAL,
                refund_fee REAL
            )
        ''')
        print("✅ 创建新表成功")
        
        # 4. 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alipay_trade_no ON alipay_wap_pay_records(trade_no)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alipay_out_trade_no ON alipay_wap_pay_records(out_trade_no)')
        print("✅ 创建索引成功")
        
        conn.commit()
        print("✅ 表重建完成")
        
    except Exception as e:
        print(f"重建表结构失败: {str(e)}")
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
    print(f"字段列表: {', '.join(oracle_columns)}")
    
    # 构建查询语句
    columns_str = ", ".join([col.upper() for col in oracle_columns])
    query = f"SELECT {columns_str} FROM ALIPAY_WAP_PAY_RECORDS"
    
    try:
        # 执行查询
        oracle_cursor.execute(query)
        rows = oracle_cursor.fetchall()
        print(f"从Oracle获取到 {len(rows)} 条记录")
        
        if rows:
            # 构建插入语句
            placeholders = ", ".join(["?"] * len(oracle_columns))
            insert_query = f"INSERT INTO alipay_wap_pay_records ({', '.join(oracle_columns)}) VALUES ({placeholders})"
            print(f"插入语句: {insert_query[:150]}...")
            
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
                    # 打印插入语句和参数，便于调试
                    print(f"插入语句: {insert_query}")
                    print(f"参数: {processed_row[:5]}...")
                    break
            
            if inserted_count > 0:
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
    print("验证重建结果...")
    
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
    
    # 检查表结构
    print("表字段:")
    for col in columns:
        print(f"  {col[1]} ({col[2]}")
    
    # 检查前5条记录
    if count > 0:
        print("\n前5条记录:")
        cursor.execute("SELECT record_id, trade_no, out_trade_no, total_amount, trade_status FROM alipay_wap_pay_records LIMIT 5")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, 交易号: {row[1]}, 商户号: {row[2]}, 金额: {row[3]}, 状态: '{row[4]}'")
    
    conn.close()
    print("验证完成")

# 主函数
def main():
    print("开始重建alipay_wap_pay_records表...")
    
    # 1. 重建表结构
    recreate_table()
    
    # 2. 迁移全量数据
    migrate_full_data()
    
    # 3. 验证结果
    verify_result()
    
    print("重建完成！")

if __name__ == '__main__':
    main()
