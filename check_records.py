import cx_Oracle

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def check_records():
    try:
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 80)
        print("查询alipay_wap_pay_records表数据统计")
        print("=" * 80)
        
        # 查询总记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        total = cursor.fetchone()[0]
        print(f"\n总记录数：{total}")
        
        # 按trade_status统计
        print("\n按支付状态统计：")
        cursor.execute("""
            SELECT trade_status, COUNT(*) as count
            FROM alipay_wap_pay_records
            GROUP BY trade_status
            ORDER BY trade_status
        """)
        for row in cursor.fetchall():
            print(f"  - {row[0]}：{row[1]}条")
        
        # 查询file_info表的总文件数
        cursor.execute("SELECT COUNT(*) FROM file_info")
        total_files = cursor.fetchone()[0]
        print(f"\nfile_info表总文件数：{total_files}")
        
        # 查询有多少个不同的file_id
        cursor.execute("SELECT COUNT(DISTINCT file_id) FROM alipay_wap_pay_records WHERE file_id IS NOT NULL")
        distinct_file_ids = cursor.fetchone()[0]
        print(f"alipay_wap_pay_records表中不同的file_id数量：{distinct_file_ids}")
        
        # 查询是否有file_id为NULL的记录
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records WHERE file_id IS NULL")
        null_file_ids = cursor.fetchone()[0]
        print(f"file_id为NULL的记录数：{null_file_ids}")
        
        # 查询最近创建的5条记录
        print("\n最近创建的5条记录：")
        cursor.execute("""
            SELECT file_id, file_name, session_id, user_id, trade_status, create_time
            FROM alipay_wap_pay_records
            WHERE file_id IS NOT NULL
            ORDER BY create_time DESC
            FETCH FIRST 5 ROWS ONLY
        """)
        for row in cursor.fetchall():
            print(f"  - file_id: {row[0]}, file_name: {row[1][:30]}..., session_id: {row[2]}, user_id: {row[3]}, status: {row[4]}")
        
        print("\n" + "=" * 80)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 查询失败：{str(e)}")

if __name__ == '__main__':
    check_records()
