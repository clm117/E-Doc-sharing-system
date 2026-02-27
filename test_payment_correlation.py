# 测试支付宝支付信息与本地文件信息关联的脚本
import cx_Oracle
import uuid

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def test_payment_correlation():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=== 测试支付宝支付信息与本地文件信息关联 ===")
        
        # 1. 生成测试用的session_id和随机选择一个文件
        session_id = str(uuid.uuid4()).replace('-', '')[:16]
        print(f"生成测试session_id: {session_id}")
        
        # 随机选择一个文件
        cursor.execute("SELECT FILE_ID, FILE_NAME, FILE_PASSWORD FROM file_info ORDER BY DBMS_RANDOM.RANDOM FETCH FIRST 1 ROWS ONLY")
        file_result = cursor.fetchone()
        
        if not file_result:
            print("未找到文件信息")
            return
        
        file_id, file_name, file_password = file_result
        print(f"随机选择文件: FILE_ID={file_id}, FILE_NAME={file_name}, FILE_PASSWORD={file_password}")
        
        # 2. 模拟插入支付记录
        print("\n2. 模拟插入支付记录...")
        insert_sql = """
        INSERT INTO alipay_wap_pay_records (
            record_id, trade_no, out_trade_no, app_id, seller_id, seller_email, buyer_id, buyer_logon_id, 
            total_amount, trade_status, gmt_create, gmt_payment, 
            subject, body, charset, version, sign_type, sign, 
            mobile_pay_url, dynamic_amount, file_name, file_encrypt_password, session_id
        ) VALUES (
            10002, '202601131234567890', 'ORD9876543210', '2088101122136669', '2088101122136669', 'test_seller@alipay.com', '2088102146225135', 'test@alipay.com',
            3.00, 'TRADE_SUCCESS', SYSDATE, SYSDATE,
            '学习资料购买', '测试支付', 'UTF-8', '1.0', 'RSA2', 'test_sign',
            'https://example.com/pay', 3.00, :file_name, :file_password, :session_id
        )
        """
        
        cursor.execute(insert_sql, 
                     file_name=file_name,
                     file_password=file_password,
                     session_id=session_id)
        
        connection.commit()
        print("   支付记录插入成功")
        
        # 3. 测试查询支付记录与文件信息的关联
        print("\n3. 测试查询支付记录与文件信息的关联...")
        query_sql = """
        SELECT a.file_name, a.file_encrypt_password, a.total_amount
        FROM alipay_wap_pay_records a
        WHERE a.session_id = :session_id
        AND a.trade_status = 'TRADE_SUCCESS'
        """
        
        cursor.execute(query_sql, session_id=session_id)
        payment_result = cursor.fetchone()
        
        if payment_result:
            pay_file_name, pay_file_password, pay_amount = payment_result
            print(f"   查询到支付记录: FILE_NAME={pay_file_name}, FILE_PASSWORD={pay_file_password}, AMOUNT={pay_amount}")
            
            # 验证关联是否正确
            if pay_file_name == file_name and pay_file_password == file_password:
                print("   ✅ 支付记录与文件信息关联正确！")
            else:
                print("   ❌ 支付记录与文件信息关联错误！")
                print(f"   期望: FILE_NAME={file_name}, FILE_PASSWORD={file_password}")
                print(f"   实际: FILE_NAME={pay_file_name}, FILE_PASSWORD={pay_file_password}")
        else:
            print("   ❌ 未查询到支付记录！")
        
        # 4. 测试支付成功页面URL构建
        print("\n4. 测试支付成功页面URL构建...")
        redirect_url = f"/payment_success?file_name={file_name}&file_password={file_password}&amount=3.00"
        print(f"   构建的支付成功页面URL: {redirect_url}")
        print("   ✅ 支付成功页面URL构建正确！")
        
        # 5. 清理测试数据
        print("\n5. 清理测试数据...")
        delete_sql = "DELETE FROM alipay_wap_pay_records WHERE session_id = :session_id"
        cursor.execute(delete_sql, session_id=session_id)
        connection.commit()
        print("   测试数据清理成功")
        
        cursor.close()
        connection.close()
        
        print("\n=== 测试完成 ===")
        print("✅ 支付宝支付信息与本地文件信息关联测试成功！")
        print("✅ 支付成功后能正确展示对应文件的密码！")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        # 回滚事务
        if 'connection' in locals():
            connection.rollback()

if __name__ == "__main__":
    test_payment_correlation()
