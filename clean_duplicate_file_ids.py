import cx_Oracle

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def clean_duplicate_file_ids():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始清理alipay_wap_pay_records表中file_id重复的数据...")
        print("=" * 80)
        
        # 1. 查询当前统计信息
        print("\n1. 查询当前统计信息...")
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        total_count = cursor.fetchone()[0]
        print(f"当前总记录数：{total_count}")
        
        cursor.execute("SELECT COUNT(DISTINCT file_id) FROM alipay_wap_pay_records WHERE file_id IS NOT NULL")
        distinct_file_id_count = cursor.fetchone()[0]
        print(f"不同的file_id数量：{distinct_file_id_count}")
        
        duplicate_count = total_count - distinct_file_id_count
        print(f"重复记录数：{duplicate_count}")
        
        # 2. 查询重复的file_id及其数量
        print("\n2. 查询重复的file_id...")
        cursor.execute("""
            SELECT file_id, COUNT(*) as count
            FROM alipay_wap_pay_records
            WHERE file_id IS NOT NULL
            GROUP BY file_id
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        duplicate_files = cursor.fetchall()
        print(f"找到{len(duplicate_files)}个重复的file_id")
        
        if duplicate_files:
            print("\n重复最多的10个file_id：")
            for i, (file_id, count) in enumerate(duplicate_files[:10]):
                print(f"  {i+1}. file_id={file_id}, 重复次数={count}")
        
        # 3. 删除重复记录（保留record_id最小的那条）
        print("\n3. 开始删除重复记录...")
        deleted_count = 0
        
        for file_id, count in duplicate_files:
            # 查询该file_id的所有记录，按record_id排序
            cursor.execute("""
                SELECT record_id
                FROM alipay_wap_pay_records
                WHERE file_id = :file_id
                ORDER BY record_id
            """, file_id=file_id)
            records = cursor.fetchall()
            
            # 保留第一条，删除其余的
            if len(records) > 1:
                records_to_delete = records[1:]  # 从第二条开始删除
                
                for record in records_to_delete:
                    record_id = record[0]
                    cursor.execute("""
                        DELETE FROM alipay_wap_pay_records
                        WHERE record_id = :record_id
                    """, record_id=record_id)
                    deleted_count += 1
        
        connection.commit()
        print(f"✅ 成功删除 {deleted_count} 条重复记录")
        
        # 4. 验证清理结果
        print("\n4. 验证清理结果...")
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        new_total_count = cursor.fetchone()[0]
        print(f"清理后总记录数：{new_total_count}")
        
        cursor.execute("SELECT COUNT(DISTINCT file_id) FROM alipay_wap_pay_records WHERE file_id IS NOT NULL")
        new_distinct_file_id_count = cursor.fetchone()[0]
        print(f"不同的file_id数量：{new_distinct_file_id_count}")
        
        # 检查是否还有重复
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT file_id, COUNT(*) as count
                FROM alipay_wap_pay_records
                WHERE file_id IS NOT NULL
                GROUP BY file_id
                HAVING COUNT(*) > 1
            )
        """)
        remaining_duplicates = cursor.fetchone()[0]
        print(f"剩余重复file_id数量：{remaining_duplicates}")
        
        # 查询支付状态分布
        print("\n支付状态分布：")
        cursor.execute("""
            SELECT trade_status, COUNT(*) as count
            FROM alipay_wap_pay_records
            GROUP BY trade_status
            ORDER BY trade_status
        """)
        for row in cursor.fetchall():
            print(f"  - {row[0]}：{row[1]}条")
        
        # 显示几条示例记录
        print("\n示例记录（前3条）：")
        cursor.execute("""
            SELECT record_id, file_id, file_name, session_id, user_id, trade_status
            FROM alipay_wap_pay_records
            WHERE ROWNUM <= 3
            ORDER BY record_id
        """)
        for row in cursor.fetchall():
            print(f"  - record_id: {row[0]}, file_id: {row[1]}, file_name: {row[2][:30] if row[2] else 'NULL'}..., "
                  f"session_id: {row[3]}, user_id: {row[4]}, status: {row[5]}")
        
        print("\n" + "=" * 80)
        print("清理完成！")
        print("=" * 80)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 清理失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始清理alipay_wap_pay_records表中file_id重复的数据")
    print("=" * 80)
    clean_duplicate_file_ids()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
