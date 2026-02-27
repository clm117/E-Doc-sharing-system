import cx_Oracle
import time
import random
import uuid

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def init_remaining_records():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始初始化剩余文件的支付记录...")
        print("=" * 50)
        
        # 1. 查询还没有支付记录的文件
        print("\n1. 查询还没有支付记录的文件...")
        query_files = """
        SELECT f.file_id, f.file_name, f.file_password
        FROM file_info f
        WHERE NOT EXISTS (
            SELECT 1 FROM alipay_wap_pay_records r 
            WHERE r.file_id = f.file_id
        )
        ORDER BY f.file_id
        """
        cursor.execute(query_files)
        files = cursor.fetchall()
        print(f"✅ 查询到{len(files)}个未创建支付记录的文件")
        
        if not files:
            print("⚠️  所有文件都已创建支付记录")
            cursor.close()
            connection.close()
            return
        
        # 2. 为每个文件创建待支付记录
        print("\n2. 为每个文件创建待支付记录...")
        success_count = 0
        failed_count = 0
        
        for i, file_info in enumerate(files):
            file_id, file_name, file_password = file_info
            
            # 生成session_id
            session_id = str(uuid.uuid4()).replace('-', '')[:16]
            
            # 生成user_id
            user_id = str(uuid.uuid4()).replace('-', '')[:16]
            
            # 生成订单号
            out_trade_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
            
            # 生成trade_no
            trade_no = f"TRADE{int(time.time() * 1000)}{random.randint(1000, 9999)}"
            
            try:
                # 插入待支付记录
                insert_sql = """
                INSERT INTO alipay_wap_pay_records (
                    trade_no, out_trade_no, app_id, total_amount, 
                    seller_id, seller_email, buyer_id, buyer_logon_id, 
                    trade_status, gmt_create, gmt_payment, gmt_refund, gmt_close, 
                    subject, body, charset, version, sign_type, sign, 
                    point_amount, invoice_amount, fund_bill_list, passback_params, 
                    file_name, mobile_pay_url, dynamic_amount, qr_code_url, 
                    create_time, update_time, file_encrypt_password, session_id, file_id, user_id
                ) VALUES (
                    :trade_no, :out_trade_no, '2021001162681234', 3.00, 
                    '2088101122136669', 'test_seller@alipay.com', '2088102146225135', 'test@alipay.com', 
                    'TRADE_PENDING', SYSDATE, NULL, NULL, NULL, 
                    '学习资料购买', :body, 'UTF-8', '1.0', 'RSA2', 'test_sign_1234567890', 
                    0, 3.00, NULL, NULL, 
                    :file_name, 'https://mobilepay.alipay.com/test', 3.00, 'https://qr.alipay.com/test', 
                    SYSDATE, SYSDATE, :file_password, :session_id, :file_id, :user_id
                )
                """
                
                cursor.execute(insert_sql, 
                             trade_no=trade_no,
                             out_trade_no=out_trade_no,
                             body=f"购买{file_name}",
                             file_name=file_name,
                             file_password=file_password,
                             session_id=session_id,
                             file_id=file_id,
                             user_id=user_id)
                
                connection.commit()
                success_count += 1
                print(f"✅ [{i+1}/{len(files)}] 创建成功：file_id={file_id}, session_id={session_id}, user_id={user_id}")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ [{i+1}/{len(files)}] 创建失败：file_id={file_id}, 错误：{str(e)}")
            
            # 每10个文件暂停一下
            if (i + 1) % 10 == 0:
                print(f"\n已处理{i+1}个文件，暂停一下...")
                connection.commit()
                time.sleep(1)
        
        # 3. 统计结果
        print("\n" + "=" * 50)
        print("初始化统计：")
        print(f"  - 总文件数：{len(files)}")
        print(f"  - 成功创建：{success_count}条")
        print(f"  - 失败创建：{failed_count}条")
        print(f"  - 总计：{success_count + failed_count}条")
        print("=" * 50)
        
        # 4. 验证数据
        print("\n4. 验证初始化数据...")
        verify_sql = """
        SELECT trade_status, COUNT(*) as count
        FROM alipay_wap_pay_records
        GROUP BY trade_status
        ORDER BY trade_status
        """
        cursor.execute(verify_sql)
        verify_result = cursor.fetchall()
        
        print("当前数据统计：")
        for row in verify_result:
            trade_status, count = row
            print(f"  - {trade_status}：{count}条")
        
        # 查询总记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        total = cursor.fetchone()[0]
        print(f"  - 总记录数：{total}")
        
        # 查询不同的file_id数量
        cursor.execute("SELECT COUNT(DISTINCT file_id) FROM alipay_wap_pay_records WHERE file_id IS NOT NULL")
        distinct_file_ids = cursor.fetchone()[0]
        print(f"  - 不同的file_id数量：{distinct_file_ids}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("=" * 50)
        print("初始化完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 初始化失败：{str(e)}")

if __name__ == '__main__':
    print("=" * 50)
    print("开始初始化剩余文件的支付记录...")
    print("=" * 50)
    init_remaining_records()
    print("=" * 50)
    print("执行完成！")
    print("=" * 50)
