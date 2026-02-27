# 简单测试脚本，直接插入一条支付成功记录
import cx_Oracle
import uuid

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def simple_test():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 生成session_id
        session_id = str(uuid.uuid4()).replace('-', '')[:16]
        
        # 直接插入一条支付成功记录
        sql = """
        INSERT INTO alipay_wap_pay_records (record_id, trade_no, out_trade_no, app_id, seller_email, 
            buyer_id, buyer_logon_id, total_amount, trade_status, gmt_create, gmt_payment, 
            subject, body, file_name, file_encrypt_password, session_id)
        VALUES (10001, '202601121234567890', 'ORD1234567890', '2088101122136669', 'test_seller@alipay.com',
            '2088102146225135', 'test@alipay.com', 3.00, 'TRADE_SUCCESS', SYSDATE, SYSDATE,
            '学习资料购买', '测试支付', '测试文件', '123456', :session_id)
        """
        
        cursor.execute(sql, session_id=session_id)
        connection.commit()
        
        print(f"测试记录插入成功！")
        print(f"Session ID: {session_id}")
        print(f"请访问：http://127.0.0.1:5000/?session_id={session_id}")
        print(f"点击'点击刷新'按钮或等待3秒自动刷新，应该跳转到payment_success.html")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    simple_test()
