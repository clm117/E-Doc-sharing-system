#!/usr/bin/env python3
# 数据库迁移脚本：从Oracle迁移到SQLite

import os
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

# 创建SQLite数据库和表
def create_sqlite_tables():
    print("创建SQLite数据库表...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 读取并执行建表脚本
    with open('create_sqlite_tables.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 执行SQL脚本
    cursor.executescript(sql_script)
    conn.commit()
    print("SQLite数据库表创建成功")
    conn.close()

# 从Oracle迁移数据到SQLite
def migrate_data():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过数据迁移")
        return
    
    print("开始从Oracle迁移数据...")
    
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
    
    # 迁移file_info表
    print("迁移file_info表...")
    try:
        # 查询Oracle中的file_info数据
        oracle_cursor.execute("SELECT file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time FROM file_info")
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time = row
            # 转换日期格式
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            sqlite_cursor.execute(
                "INSERT OR IGNORE INTO file_info (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time_str, update_time_str)
            )
        sqlite_conn.commit()
        print(f"成功迁移 {len(rows)} 条file_info记录")
    except Exception as e:
        print(f"迁移file_info表失败: {str(e)}")
    
    # 迁移payment_config表
    print("迁移payment_config表...")
    try:
        # 查询Oracle中的payment_config数据
        oracle_cursor.execute("SELECT config_id, price_type, amount, payment_url, description, status, create_time, update_time FROM payment_config")
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            config_id, price_type, amount, payment_url, description, status, create_time, update_time = row
            # 转换日期格式
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            sqlite_cursor.execute(
                "INSERT OR IGNORE INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (config_id, price_type, amount, payment_url, description, status, create_time_str, update_time_str)
            )
        sqlite_conn.commit()
        print(f"成功迁移 {len(rows)} 条payment_config记录")
    except Exception as e:
        print(f"迁移payment_config表失败: {str(e)}")
    
    # 迁移alipay_wap_pay_records表
    print("迁移alipay_wap_pay_records表...")
    try:
        # 查询Oracle中的alipay_wap_pay_records数据
        oracle_cursor.execute("SELECT record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create, gmt_payment, gmt_refund, gmt_close, file_id, create_time, update_time FROM alipay_wap_pay_records")
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create, gmt_payment, gmt_refund, gmt_close, file_id, create_time, update_time = row
            # 转换日期格式
            gmt_create_str = gmt_create.strftime('%Y-%m-%d %H:%M:%S') if gmt_create else None
            gmt_payment_str = gmt_payment.strftime('%Y-%m-%d %H:%M:%S') if gmt_payment else None
            gmt_refund_str = gmt_refund.strftime('%Y-%m-%d %H:%M:%S') if gmt_refund else None
            gmt_close_str = gmt_close.strftime('%Y-%m-%d %H:%M:%S') if gmt_close else None
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            sqlite_cursor.execute(
                "INSERT OR IGNORE INTO alipay_wap_pay_records (record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create, gmt_payment, gmt_refund, gmt_close, file_id, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create_str, gmt_payment_str, gmt_refund_str, gmt_close_str, file_id, create_time_str, update_time_str)
            )
        sqlite_conn.commit()
        print(f"成功迁移 {len(rows)} 条alipay_wap_pay_records记录")
    except Exception as e:
        print(f"迁移alipay_wap_pay_records表失败: {str(e)}")
    
    # 关闭连接
    oracle_cursor.close()
    oracle_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()
    print("数据迁移完成")

# 验证迁移结果
def verify_migration():
    print("验证迁移结果...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 检查file_info表
    cursor.execute("SELECT COUNT(*) FROM file_info")
    file_count = cursor.fetchone()[0]
    print(f"file_info表记录数: {file_count}")
    
    # 检查payment_config表
    cursor.execute("SELECT COUNT(*) FROM payment_config")
    config_count = cursor.fetchone()[0]
    print(f"payment_config表记录数: {config_count}")
    
    # 检查alipay_wap_pay_records表
    cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
    payment_count = cursor.fetchone()[0]
    print(f"alipay_wap_pay_records表记录数: {payment_count}")
    
    conn.close()
    print("迁移验证完成")

# 主函数
def main():
    print("开始数据库迁移...")
    
    # 创建SQLite表
    create_sqlite_tables()
    
    # 迁移数据
    migrate_data()
    
    # 验证迁移结果
    verify_migration()
    
    print("数据库迁移完成！")

if __name__ == '__main__':
    main()