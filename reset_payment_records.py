import cx_Oracle

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def reset_payment_records():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始重置alipay_wap_pay_records表...")
        print("=" * 80)
        
        # 查询当前记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        total_count = cursor.fetchone()[0]
        print(f"\n当前总记录数：{total_count}")
        
        # 查询当前支付状态分布
        print("\n当前支付状态分布：")
        cursor.execute("""
            SELECT trade_status, COUNT(*) as count
            FROM alipay_wap_pay_records
            GROUP BY trade_status
            ORDER BY trade_status
        """)
        for row in cursor.fetchall():
            print(f"  - {row[0]}：{row[1]}条")
        
        # 重置所有记录
        print("\n开始重置记录...")
        update_sql = """
        UPDATE alipay_wap_pay_records
        SET 
            trade_status = 'TRADE_PENDING',
            seller_email = NULL,
            gmt_payment = NULL,
            gmt_refund = NULL,
            gmt_close = NULL,
            body = NULL,
            point_amount = NULL,
            invoice_amount = NULL,
            fund_bill_list = NULL,
            passback_params = NULL,
            create_time = NULL,
            update_time = NULL,
            user_id = NULL
        """
        
        cursor.execute(update_sql)
        updated_rows = cursor.rowcount
        connection.commit()
        
        print(f"✅ 成功更新 {updated_rows} 条记录")
        
        # 验证更新结果
        print("\n验证更新结果...")
        cursor.execute("""
            SELECT trade_status, COUNT(*) as count
            FROM alipay_wap_pay_records
            GROUP BY trade_status
            ORDER BY trade_status
        """)
        print("更新后的支付状态分布：")
        for row in cursor.fetchall():
            print(f"  - {row[0]}：{row[1]}条")
        
        # 查询user_id为NULL的记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records WHERE user_id IS NULL")
        null_user_id_count = cursor.fetchone()[0]
        print(f"\nuser_id为NULL的记录数：{null_user_id_count}")
        
        # 查询buyer_id为NULL的记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records WHERE buyer_id IS NULL")
        null_buyer_id_count = cursor.fetchone()[0]
        print(f"buyer_id为NULL的记录数：{null_buyer_id_count}")
        
        # 查询gmt_payment为NULL的记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records WHERE gmt_payment IS NULL")
        null_gmt_payment_count = cursor.fetchone()[0]
        print(f"gmt_payment为NULL的记录数：{null_gmt_payment_count}")
        
        # 显示几条示例记录
        print("\n示例记录（前3条）：")
        cursor.execute("""
            SELECT file_id, file_name, session_id, user_id, trade_status, 
                   buyer_id, gmt_payment, gmt_refund
            FROM alipay_wap_pay_records
            WHERE ROWNUM <= 3
            ORDER BY record_id
        """)
        for row in cursor.fetchall():
            print(f"  - file_id: {row[0]}, file_name: {row[1][:30] if row[1] else 'NULL'}..., "
                  f"session_id: {row[2]}, user_id: {row[3]}, status: {row[4]}, "
                  f"buyer_id: {row[5]}, gmt_payment: {row[6]}")
        
        print("\n" + "=" * 80)
        print("重置完成！")
        print("=" * 80)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 重置失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始重置alipay_wap_pay_records表")
    print("=" * 80)
    reset_payment_records()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
