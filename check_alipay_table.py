# 检查alipay_wap_pay_records表结构的脚本
import cx_Oracle

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def check_alipay_table():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=== alipay_wap_pay_records表结构 ===")
        # 查询alipay_wap_pay_records表的列信息
        cursor.execute("SELECT column_name, data_type, data_length, nullable FROM user_tab_columns WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS' ORDER BY column_id")
        columns = cursor.fetchall()
        for col in columns:
            print(f"{col[0]:<30} {col[1]:<20} {col[2]:<5} {'NULL' if col[3] == 'Y' else 'NOT NULL'}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"检查失败: {str(e)}")

if __name__ == "__main__":
    check_alipay_table()
