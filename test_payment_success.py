# 测试支付成功功能的脚本
import cx_Oracle
import random
import time

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def test_payment_success():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 生成测试用的session_id（16位）
        import uuid
        session_id = str(uuid.uuid4()).replace('-', '')[:16]
        print(f"生成测试session_id: {session_id}")
        
        # 获取一个随机的file信息
        cursor.execute("SELECT file_name, file_password FROM file_info WHERE rownum = 1")
        file_result = cursor.fetchone()
        
        if not file_result:
            print("未找到文件信息")
            return
        
        file_name, file_password = file_result
        
        # 生成随机订单号
        out_trade_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
        trade_no = f"20260112{random.randint(1000000000000000000, 9999999999999999999)}"
        amount = 3.00
        
        # 插入测试支付记录
        insert_sql = """
        INSERT INTO alipay_wap_pay_records (
            trade_no, out_trade_no, buyer_id, buyer_logon_id, 
            seller_email, total_amount, trade_status, gmt_create, 
            gmt_payment, subject, body, file_name, 
            file_encrypt_password, session_id
        ) VALUES (
            :trade_no, :out_trade_no, '2088102146225135', 'test@alipay.com', 
            'test_seller@alipay.com', :total_amount, 'TRADE_SUCCESS', SYSDATE, 
            SYSDATE, :subject, :body, :file_name, 
            :file_password, :session_id
        )
        """
        
        cursor.execute(insert_sql, 
                     trade_no=trade_no,
                     out_trade_no=out_trade_no,
                     total_amount=amount,
                     subject="学习资料购买",
                     body=f"购买{file_name}",
                     file_name=file_name,
                     file_password=file_password,
                     session_id=session_id)
        
        connection.commit()
        
        print(f"测试支付记录插入成功！")
        print(f"请访问以下URL测试刷新功能：")
        print(f"http://127.0.0.1:5000/?session_id={session_id}")
        print(f"点击'点击刷新'按钮，应该跳转到payment_success.html")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    test_payment_success()
