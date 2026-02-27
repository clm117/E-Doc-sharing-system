# 详细检查表结构的Python脚本
import cx_Oracle

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def check_table_structure_detailed():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=== payment_config表结构 ===")
        # 查询payment_config表的列信息
        cursor.execute("SELECT column_name, data_type, data_length, nullable FROM user_tab_columns WHERE table_name = 'PAYMENT_CONFIG' ORDER BY column_id")
        columns = cursor.fetchall()
        for col in columns:
            print(f"{col[0]:<30} {col[1]:<20} {col[2]:<5} {'NULL' if col[3] == 'Y' else 'NOT NULL'}")
        
        print("\n=== payment_config表数据 ===")
        # 查询payment_config表的所有数据
        cursor.execute("SELECT * FROM payment_config")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        print("\n=== file_info表结构 ===")
        # 查询file_info表的列信息
        cursor.execute("SELECT column_name, data_type, data_length, nullable FROM user_tab_columns WHERE table_name = 'FILE_INFO' ORDER BY column_id")
        columns = cursor.fetchall()
        for col in columns:
            print(f"{col[0]:<30} {col[1]:<20} {col[2]:<5} {'NULL' if col[3] == 'Y' else 'NOT NULL'}")
        
        print("\n=== file_info表前5行数据 ===")
        # 查询file_info表的前5行数据
        cursor.execute("SELECT * FROM file_info WHERE rownum <= 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"检查表结构失败: {str(e)}")

if __name__ == "__main__":
    check_table_structure_detailed()
