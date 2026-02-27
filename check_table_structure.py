import cx_Oracle

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def check_table_structure():
    try:
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("查询alipay_wap_pay_records表结构...")
        print("=" * 80)
        
        # 查询表的所有列
        cursor.execute("""
            SELECT column_name, data_type, data_length, nullable
            FROM user_tab_columns
            WHERE table_name = 'FILE_INFO'
            ORDER BY column_id
        "")
        
        columns = cursor.fetchall()
        
        print(f"表 'ALIPAY_WAP_PAY_RECORDS' 共有 {len(columns)} 个列：\n")
        
        for col in columns:
            column_name, data_type, data_length, nullable = col
            nullable_str = "NULL" if nullable == 'Y' else "NOT NULL"
            print(f"  {column_name:<30} {data_type:<15} 长度:{data_length:<6} {nullable_str}")
        
        print("\n" + "=" * 80)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 查询失败：{str(e)}")

if __name__ == '__main__':
    check_table_structure()
