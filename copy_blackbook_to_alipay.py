#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将黑皮书目录的521个文件数据复制到alipay_wap_pay_records表中，自动生成session_id
"""

import os
import cx_Oracle
import re
import uuid
import random
from datetime import datetime


def copy_blackbook_to_alipay():
    """
    将黑皮书目录的521个文件数据复制到alipay_wap_pay_records表中，自动生成session_id
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    # PDF文件目录
    pdf_dir = r"D:\2.enjoy\2.学习资料\【162】 计算机科学丛书（黑皮书500+）"
    
    try:
        # 获取黑皮书目录下的所有PDF文件
        blackbook_files = []
        for root, dirs, files in os.walk(pdf_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    blackbook_files.append(file)
        
        print(f"找到{len(blackbook_files)}个黑皮书PDF文件")
        
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询黑皮书文件在file_info表中的相关数据
        select_sql = """
        SELECT FILE_ID, FILE_NAME, FILE_AUTHOR, FILE_ISBN, STANDARD_NAME
        FROM file_info
        WHERE FILE_NAME = :file_name
        """
        
        # 插入alipay_wap_pay_records表的SQL语句
        insert_sql = """
        INSERT INTO alipay_wap_pay_records (
            RECORD_ID,
            TRADE_NO,
            OUT_TRADE_NO,
            APP_ID,
            TOTAL_AMOUNT,
            SELLER_ID,
            BUYER_ID,
            BUYER_LOGON_ID,
            TRADE_STATUS,
            GMT_CREATE,
            SUBJECT,
            BODY,
            CHARSET,
            VERSION,
            SIGN_TYPE,
            SIGN,
            FILE_NAME,
            MOBILE_PAY_URL,
            DYNAMIC_AMOUNT,
            QR_CODE_URL,
            CREATE_TIME,
            UPDATE_TIME,
            SESSION_ID,
            FILE_ENCRYPT_PASSWORD
        ) VALUES (
            NULL,  -- 由触发器自动生成
            :trade_no,
            :out_trade_no,
            :app_id,
            :total_amount,
            :seller_id,
            :buyer_id,
            :buyer_logon_id,
            :trade_status,
            :gmt_create,
            :subject,
            :body,
            :charset,
            :version,
            :sign_type,
            :sign,
            :file_name,
            :mobile_pay_url,
            :dynamic_amount,
            :qr_code_url,
            SYSDATE,
            SYSDATE,
            :session_id,
            :file_encrypt_password
        )
        """
        
        inserted_count = 0
        skipped_count = 0
        
        # 遍历每个黑皮书PDF文件
        for pdf_file in blackbook_files:
            try:
                # 查询file_info表中的相关数据
                cursor.execute(select_sql, {'file_name': pdf_file})
                result = cursor.fetchone()
                
                if result:
                    file_id, file_name, file_author, file_isbn, standard_name = result
                    
                    # 自动生成session_id（使用UUID的前20个字符，确保不超过长度限制）
                    session_id = str(uuid.uuid4())[:20]
                    
                    # 生成其他必填字段的随机值
                    trade_no = f"TRADE{random.randint(10000000, 99999999)}"
                    out_trade_no = f"OUT{random.randint(10000000, 99999999)}"
                    app_id = "2021000116698765"
                    total_amount = round(random.uniform(0.01, 999.99), 2)
                    seller_id = "2088102146225135"
                    buyer_id = f"2088{random.randint(1000000000000000, 9999999999999999)}"
                    buyer_logon_id = f"test{random.randint(100000, 999999)}@example.com"
                    trade_status = "WAIT_BUYER_PAY"
                    gmt_create = datetime.now()
                    subject = f"购买电子书：{standard_name if standard_name else file_name}"
                    body = f"作者：{file_author}，ISBN：{file_isbn}"
                    charset = "UTF-8"
                    version = "1.0"
                    sign_type = "RSA2"
                    sign = "test_sign_" + str(random.randint(10000000, 99999999))
                    file_encrypt_password = str(random.randint(100000, 999999))
                    mobile_pay_url = "http://localhost:8080/mobile_pay.html"
                    dynamic_amount = total_amount
                    qr_code_url = f"http://localhost:8080/qr_code_{random.randint(100000, 999999)}.png"
                    
                    # 准备插入数据
                    insert_data = {
                        'trade_no': trade_no,
                        'out_trade_no': out_trade_no,
                        'app_id': app_id,
                        'total_amount': total_amount,
                        'seller_id': seller_id,
                        'buyer_id': buyer_id,
                        'buyer_logon_id': buyer_logon_id,
                        'trade_status': trade_status,
                        'gmt_create': gmt_create,
                        'subject': subject,
                        'body': body,
                        'charset': charset,
                        'version': version,
                        'sign_type': sign_type,
                        'sign': sign,
                        'file_name': file_name,
                        'mobile_pay_url': mobile_pay_url,
                        'dynamic_amount': dynamic_amount,
                        'qr_code_url': qr_code_url,
                        'session_id': session_id,
                        'file_encrypt_password': file_encrypt_password
                    }
                    
                    # 执行插入
                    cursor.execute(insert_sql, insert_data)
                    inserted_count += 1
                    print(f"插入成功: {file_name}")
                    print(f"  Session ID: {session_id}")
                else:
                    skipped_count += 1
                    print(f"跳过: {file_name}（file_info表中不存在）")
            except Exception as e:
                # 其他错误
                skipped_count += 1
                print(f"处理失败 {file_name}: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n操作完成！")
        print(f"成功插入: {inserted_count}条记录")
        print(f"跳过: {skipped_count}条记录")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    copy_blackbook_to_alipay()