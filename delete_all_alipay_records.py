import cx_Oracle

# Oracle数据库连接配置（与app.py保持一致）
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def delete_all_records():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("警告：即将删除alipay_wap_pay_records表中的所有数据！")
        print("=" * 50)
        
        # 1. 查询当前数据统计
        print("\n1. 查询当前数据统计...")
        count_sql = """
        SELECT COUNT(*) as total_count
        FROM alipay_wap_pay_records
        """
        cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]
        print(f"  - 总记录数：{total_count}条")
        
        # 2. 删除所有数据
        print("\n2. 删除所有数据...")
        delete_sql = "DELETE FROM alipay_wap_pay_records"
        cursor.execute(delete_sql)
        deleted_count = cursor.rowcount
        connection.commit()
        print(f"✅ 删除成功：{deleted_count}条记录")
        
        # 3. 验证删除
        print("\n3. 验证删除...")
        verify_sql = """
        SELECT COUNT(*) as remaining_count
        FROM alipay_wap_pay_records
        """
        cursor.execute(verify_sql)
        remaining_count = cursor.fetchone()[0]
        
        if remaining_count == 0:
            print(f"✅ 验证成功：表中已无数据")
        else:
            print(f"❌ 验证失败：表中仍有{remaining_count}条记录")
        
        # 4. 验证表结构
        print("\n4. 验证表结构...")
        try:
            # 查询表中的列数
            column_count_sql = """
            SELECT COUNT(*) as column_count
            FROM user_tab_columns
            WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
            """
            cursor.execute(column_count_sql)
            column_count = cursor.fetchone()[0]
            print(f"  - 表中列数：{column_count}个")
            
            # 查询索引数
            index_count_sql = """
            SELECT COUNT(*) as index_count
            FROM user_indexes
            WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
            """
            cursor.execute(index_count_sql)
            index_count = cursor.fetchone()[0]
            print(f"  - 索引数：{index_count}个")
            
            print(f"✅ 表结构验证成功：{column_count}个列，{index_count}个索引")
        except Exception as e:
            print(f"⚠️  表结构验证失败：{str(e)}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("=" * 50)
        print("删除完成！")
        print("=" * 50)
        print(f"\n总结：")
        print(f"  - 删除记录数：{deleted_count}条")
        print(f"  - 剩余记录数：{remaining_count}条")
        print(f"  - 表结构：保留")
        print(f"  - 索引：保留")
        
    except Exception as e:
        print(f"❌ 删除失败: {str(e)}")

if __name__ == '__main__':
    print("=" * 50)
    print("开始删除alipay_wap_pay_records表中的所有数据...")
    print("=" * 50)
    delete_all_records()
    print("=" * 50)
    print("执行完成！")
    print("=" * 50)
