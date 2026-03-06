#!/usr/bin/env python3
# 数据库迁移脚本：从Oracle迁移到SQLite（版本2）

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
        # 尝试不同的查询语句，适应Oracle表的实际结构
        try:
            # 尝试完整字段查询
            oracle_cursor.execute("SELECT file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time, file_author, standard_name, search_keywords, file_tags, file_isbn, file_price_type, file_path, remark1, remark2, remark3 FROM file_info")
        except Exception as e:
            print(f"完整字段查询失败: {str(e)}")
            print("尝试基本字段查询...")
            # 尝试基本字段查询
            oracle_cursor.execute("SELECT file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time FROM file_info")
        
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            # 根据返回的字段数量确定如何处理
            if len(row) == 19:
                file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time, file_author, standard_name, search_keywords, file_tags, file_isbn, file_price_type, file_path, remark1, remark2, remark3 = row
            else:
                # 基本字段
                file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time = row
                # 其他字段设为默认值
                file_author = None
                standard_name = None
                search_keywords = None
                file_tags = None
                file_isbn = None
                file_price_type = '1'
                file_path = None
                remark1 = None
                remark2 = None
                remark3 = None
            
            # 转换日期格式
            create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
            update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            
            sqlite_cursor.execute(
                "INSERT OR IGNORE INTO file_info (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time, file_author, standard_name, search_keywords, file_tags, file_isbn, file_price_type, file_path, remark1, remark2, remark3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time_str, update_time_str, file_author, standard_name, search_keywords, file_tags, file_isbn, file_price_type, file_path, remark1, remark2, remark3)
            )
        sqlite_conn.commit()
        print(f"成功迁移 {len(rows)} 条file_info记录")
    except Exception as e:
        print(f"迁移file_info表失败: {str(e)}")
    
    # 迁移payment_config表
    print("迁移payment_config表...")
    try:
        # 尝试不同的查询语句，适应Oracle表的实际结构
        try:
            # 尝试完整字段查询
            oracle_cursor.execute("SELECT config_id, price_type, amount, payment_url, description, status, create_time, update_time FROM payment_config")
        except Exception as e:
            print(f"完整字段查询失败: {str(e)}")
            print("尝试基本字段查询...")
            # 尝试基本字段查询
            oracle_cursor.execute("SELECT price_type, amount, payment_url, description, status FROM payment_config")
        
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            # 根据返回的字段数量确定如何处理
            if len(row) == 8:
                config_id, price_type, amount, payment_url, description, status, create_time, update_time = row
                # 转换日期格式
                create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
                update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            else:
                # 基本字段
                price_type, amount, payment_url, description, status = row
                config_id = None
                create_time_str = None
                update_time_str = None
            
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
        # 尝试不同的查询语句，适应Oracle表的实际结构
        try:
            # 尝试完整字段查询
            oracle_cursor.execute("SELECT record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create, gmt_payment, gmt_refund, gmt_close, file_id, create_time, update_time FROM alipay_wap_pay_records")
        except Exception as e:
            print(f"完整字段查询失败: {str(e)}")
            print("尝试基本字段查询...")
            # 尝试基本字段查询
            oracle_cursor.execute("SELECT record_id, code, msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, total_amount, subject, gmt_create, file_id FROM alipay_wap_pay_records")
        
        rows = oracle_cursor.fetchall()
        
        # 插入到SQLite
        for row in rows:
            # 根据返回的字段数量确定如何处理
            if len(row) == 26:
                record_id, code, msg, sub_code, sub_msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, seller_email, total_amount, receipt_amount, invoice_amount, buyer_pay_amount, point_amount, refund_fee, subject, body, gmt_create, gmt_payment, gmt_refund, gmt_close, file_id, create_time, update_time = row
                # 转换日期格式
                gmt_create_str = gmt_create.strftime('%Y-%m-%d %H:%M:%S') if gmt_create else None
                gmt_payment_str = gmt_payment.strftime('%Y-%m-%d %H:%M:%S') if gmt_payment else None
                gmt_refund_str = gmt_refund.strftime('%Y-%m-%d %H:%M:%S') if gmt_refund else None
                gmt_close_str = gmt_close.strftime('%Y-%m-%d %H:%M:%S') if gmt_close else None
                create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S') if create_time else None
                update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S') if update_time else None
            else:
                # 基本字段
                record_id, code, msg, trade_no, out_trade_no, buyer_id, buyer_logon_id, seller_id, total_amount, subject, gmt_create, file_id = row
                # 其他字段设为默认值
                sub_code = None
                sub_msg = None
                seller_email = None
                receipt_amount = None
                invoice_amount = None
                buyer_pay_amount = None
                point_amount = None
                refund_fee = None
                body = None
                gmt_payment = None
                gmt_refund = None
                gmt_close = None
                create_time = None
                update_time = None
                # 转换日期格式
                gmt_create_str = gmt_create.strftime('%Y-%m-%d %H:%M:%S') if gmt_create else None
                gmt_payment_str = None
                gmt_refund_str = None
                gmt_close_str = None
                create_time_str = None
                update_time_str = None
            
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
    
    # 迁移数据
    migrate_data()
    
    # 验证迁移结果
    verify_migration()
    
    print("数据库迁移完成！")

if __name__ == '__main__':
    main()
