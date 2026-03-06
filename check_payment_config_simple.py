import sqlite3

# 检查当前SQLite的payment_config表内容
try:
    conn = sqlite3.connect('docshare.db')
    cursor = conn.cursor()
    
    # 检查数据
    cursor.execute("SELECT * FROM payment_config;")
    data = cursor.fetchall()
    print(f"当前记录数: {len(data)}")
    for row in data:
        print(row)
    
    conn.close()
except Exception as e:
    print(f"错误: {str(e)}")