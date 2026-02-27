import cx_Oracle
from datetime import datetime, timedelta

# Oracle数据库连接配置（与app.py保持一致）
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def clean_old_records():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 清理策略配置
        days_to_keep = 30  # 保留最近30天的记录
        max_records_per_file = 10  # 每个file_id最多保留10条记录
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        print(f"清理策略：保留最近{days_to_keep}天的记录，每个file_id最多保留{max_records_per_file}条")
        print(f"截止日期：{cutoff_date}")
        
        # 1. 清理超过30天的记录
        print("\n1. 清理超过30天的记录...")
        delete_old_sql = """
        DELETE FROM alipay_wap_pay_records
        WHERE gmt_create < TO_DATE(:cutoff_date, 'YYYY-MM-DD HH24:MI:SS')
        """
        cursor.execute(delete_old_sql, cutoff_date=cutoff_date.strftime('%Y-%m-%d %H:%M:%S'))
        old_deleted = cursor.rowcount
        connection.commit()
        print(f"✅ 删除超过{days_to_keep}天的记录：{old_deleted}条")
        
        # 2. 清理已关闭的记录（TRADE_CLOSED），保留最近10条
        print("\n2. 清理已关闭的记录（TRADE_CLOSED），保留最近10条...")
        
        # 先查询每个file_id的TRADE_CLOSED记录数量
        count_closed_sql = """
        SELECT file_id, COUNT(*) as count
        FROM alipay_wap_pay_records
        WHERE trade_status = 'TRADE_CLOSED'
        GROUP BY file_id
        HAVING COUNT(*) > :max_records
        """
        cursor.execute(count_closed_sql, max_records=max_records_per_file)
        file_ids_to_clean = cursor.fetchall()
        
        if file_ids_to_clean:
            print(f"找到{len(file_ids_to_clean)}个file_id需要清理...")
            
            # 删除多余的TRADE_CLOSED记录
            for file_id_info in file_ids_to_clean:
                file_id_to_delete = file_id_info[0]
                count_to_delete = file_id_info[1]
                
                # 查询要删除的记录ID
                select_ids_sql = """
                SELECT record_id
                FROM (
                    SELECT record_id
                    FROM alipay_wap_pay_records
                    WHERE file_id = :file_id
                    AND trade_status = 'TRADE_CLOSED'
                    ORDER BY gmt_create DESC
                    OFFSET :offset ROWS
                )
                WHERE rownum <= :offset
                """
                cursor.execute(select_ids_sql, file_id=file_id_to_delete, offset=max_records_per_file)
                records_to_delete = cursor.fetchall()
                
                if records_to_delete:
                    record_ids = [str(r[0]) for r in records_to_delete]
                    
                    # 删除记录
                    delete_closed_sql = """
                    DELETE FROM alipay_wap_pay_records
                    WHERE record_id IN ({})
                    """.format(','.join(record_ids))
                    cursor.execute(delete_closed_sql)
                    connection.commit()
                    print(f"  - file_id={file_id_to_delete}：删除{len(record_ids)}条记录（保留最近{max_records_per_file}条）")
        
        closed_deleted = cursor.rowcount
        print(f"✅ 删除TRADE_CLOSED记录：{closed_deleted}条")
        
        # 3. 清理已取消的记录（TRADE_CANCELLED）
        print("\n3. 清理已取消的记录（TRADE_CANCELLED）...")
        delete_cancelled_sql = """
        DELETE FROM alipay_wap_pay_records
        WHERE trade_status = 'TRADE_CANCELLED'
        AND gmt_create < TO_DATE(:cutoff_date, 'YYYY-MM-DD HH24:MI:SS')
        """
        cursor.execute(delete_cancelled_sql, cutoff_date=cutoff_date.strftime('%Y-%m-%d %H:%M:%S'))
        cancelled_deleted = cursor.rowcount
        connection.commit()
        print(f"✅ 删除TRADE_CANCELLED记录：{cancelled_deleted}条")
        
        # 4. 清理失败的记录（TRADE_FAILED）
        print("\n4. 清理失败的记录（TRADE_FAILED）...")
        delete_failed_sql = """
        DELETE FROM alipay_wap_pay_records
        WHERE trade_status = 'TRADE_FAILED'
        AND gmt_create < TO_DATE(:cutoff_date, 'YYYY-MM-DD HH24:MI:SS')
        """
        cursor.execute(delete_failed_sql, cutoff_date=cutoff_date.strftime('%Y-%m-%d %H:%M:%S'))
        failed_deleted = cursor.rowcount
        connection.commit()
        print(f"✅ 删除TRADE_FAILED记录：{failed_deleted}条")
        
        # 5. 统计清理结果
        print("\n" + "=" * 50)
        print("清理统计：")
        print(f"  - 删除超过{days_to_keep}天的记录：{old_deleted}条")
        print(f"  - 删除TRADE_CLOSED记录：{closed_deleted}条")
        print(f"  - 删除TRADE_CANCELLED记录：{cancelled_deleted}条")
        print(f"  - 删除TRADE_FAILED记录：{failed_deleted}条")
        print(f"  - 总计删除：{old_deleted + closed_deleted + cancelled_deleted + failed_deleted}条")
        print("=" * 50)
        
        # 6. 验证清理后的数据
        print("\n验证清理后的数据...")
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
        
        # 关闭连接
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("清理完成！")
        
    except Exception as e:
        print(f"❌ 清理失败: {str(e)}")

if __name__ == '__main__':
    print("=" * 50)
    print("开始清理alipay_wap_pay_records表...")
    print("=" * 50)
    clean_old_records()
    print("=" * 50)
    print("执行完成！")
    print("=" * 50)
