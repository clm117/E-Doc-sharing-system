#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本：演示如何从Oracle数据库读取qr_code_url字段，生成二维码并在index.html中显示
"""

import os
import cx_Oracle
from io import BytesIO
import qrcode

# 数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/orcleshow',
    'encoding': 'UTF-8'
}

def generate_qr_code_from_db():
    """
    从数据库中读取qr_code_url，生成二维码
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 查询最新的一条记录
        query = "SELECT qr_code_url, dynamic_amount FROM alipay_wap_pay_records ORDER BY record_id DESC FETCH FIRST 1 ROWS ONLY"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            qr_code_url = result[0]
            dynamic_amount = result[1]
            
            print(f"从数据库获取到二维码URL: {qr_code_url}")
            print(f"动态金额: {dynamic_amount}")
            
            # 生成二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_code_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 保存二维码图片
            img_path = os.path.join(os.getcwd(), "static", "qrcode.png")
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            img.save(img_path)
            print(f"二维码已生成并保存到: {img_path}")
            
            return qr_code_url, dynamic_amount
        else:
            print("数据库中没有记录")
            return None, None
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"数据库错误: {error.code} - {error.message}")
        return None, None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def insert_sample_data():
    """
    插入示例数据到数据库
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 示例数据
        sample_data = {
            'trade_no': '2026010922001104560500123456',
            'out_trade_no': 'TEST202601090001',
            'app_id': '2021000112345678',
            'total_amount': 3.00,
            'seller_id': '2088123456789012',
            'buyer_id': '2088123456789013',
            'buyer_logon_id': 'test@example.com',
            'trade_status': 'WAIT_BUYER_PAY',
            'gmt_create': '2026-01-09 10:00:00',
            'subject': '测试商品',
            'body': '这是一个测试商品的描述',
            'charset': 'UTF-8',
            'version': '1.0',
            'sign_type': 'RSA2',
            'sign': 'test_sign',
            'file_name': 'test_file.txt',
            'mobile_pay_url': 'http://192.168.100.174:5000/mobile_payment_simple',
            'dynamic_amount': 3.00,
            # 这里的URL将用于生成二维码，扫描后跳转到mobile_payment_simple.html
            'qr_code_url': 'http://192.168.100.174:5000/mobile_payment_simple'
        }
        
        # 插入数据
        insert_sql = """
        INSERT INTO alipay_wap_pay_records (
            trade_no, out_trade_no, app_id, total_amount, seller_id, 
            buyer_id, buyer_logon_id, trade_status, gmt_create, 
            subject, body, charset, version, sign_type, sign, 
            file_name, mobile_pay_url, dynamic_amount, qr_code_url
        ) VALUES (
            :trade_no, :out_trade_no, :app_id, :total_amount, :seller_id, 
            :buyer_id, :buyer_logon_id, :trade_status, TO_DATE(:gmt_create, 'YYYY-MM-DD HH24:MI:SS'), 
            :subject, :body, :charset, :version, :sign_type, :sign, 
            :file_name, :mobile_pay_url, :dynamic_amount, :qr_code_url
        )
        """
        
        cursor.execute(insert_sql, sample_data)
        connection.commit()
        print("示例数据已插入到数据库")
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"数据库错误: {error.code} - {error.message}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def main():
    """
    主函数
    """
    print("1. 插入示例数据到数据库...")
    insert_sample_data()
    
    print("\n2. 从数据库读取qr_code_url，生成二维码...")
    qr_code_url, dynamic_amount = generate_qr_code_from_db()
    
    if qr_code_url:
        print(f"\n3. 生成的二维码信息:")
        print(f"   - 二维码URL: {qr_code_url}")
        print(f"   - 动态金额: {dynamic_amount}元")
        print(f"   - 扫描二维码后，将跳转到: {qr_code_url}")
        print(f"   - 该页面为: mobile_payment_simple.html")
    
    print("\n4. 在index.html中使用二维码:")
    print("   <img src='/qrcode' alt='支付二维码' title='扫描二维码进行支付'>")
    print("   其中，/qrcode路由将从数据库读取qr_code_url，生成并返回二维码图片")

if __name__ == "__main__":
    main()
