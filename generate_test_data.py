#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成10行测试数据并插入到alipay_wap_pay_records表中
"""

import cx_Oracle
import datetime

# 数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/orcl',
    'encoding': 'UTF-8'
}

def generate_test_data():
    """
    生成10行测试数据并插入到数据库
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 生成10行测试数据
        for i in range(1, 11):
            # 生成唯一的交易号和订单号
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            trade_no = f'20260109220011045605{i:06d}'
            out_trade_no = f'TEST20260109{i:04d}'
            
            # 测试数据
            test_data = {
                'trade_no': trade_no,
                'out_trade_no': out_trade_no,
                'app_id': '2021000112345678',
                'total_amount': 3.00 + (i * 0.5),  # 金额递增，从3.00开始
                'seller_id': '2088123456789012',
                'buyer_id': f'2088123456789{i:03d}',
                'buyer_logon_id': f'test{i}@example.com',
                'trade_status': 'WAIT_BUYER_PAY' if i % 2 == 0 else 'TRADE_SUCCESS',  # 交替设置支付状态
                'gmt_create': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'subject': f'测试商品{i}',
                'body': f'这是第{i}个测试商品的描述',
                'charset': 'UTF-8',
                'version': '1.0',
                'sign_type': 'RSA2',
                'sign': f'test_sign{i}',
                'file_name': f'test_file{i}.txt',
                'mobile_pay_url': 'http://192.168.100.174:5000/mobile_payment_simple',
                'dynamic_amount': 3.00 + (i * 0.5),  # 动态金额与总金额一致
                'qr_code_url': 'http://192.168.100.174:5000/mobile_payment_simple'  # 二维码URL
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
            
            cursor.execute(insert_sql, test_data)
            print(f"已插入第{i}行测试数据")
        
        # 提交事务
        connection.commit()
        print("\n10行测试数据已成功插入到数据库")
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"数据库错误: {error.code} - {error.message}")
        # 回滚事务
        if 'connection' in locals():
            connection.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def check_data_count():
    """
    检查表中的数据行数
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 查询数据行数
        query = "SELECT COUNT(*) FROM alipay_wap_pay_records"
        cursor.execute(query)
        result = cursor.fetchone()
        
        print(f"\nalipay_wap_pay_records表中的数据行数: {result[0]}")
        
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
    print("开始生成10行测试数据...")
    generate_test_data()
    check_data_count()

if __name__ == "__main__":
    main()
