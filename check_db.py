import sqlite3

# 连接SQLite数据库
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 检查payment_config表是否存在
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment_config';")
    if cursor.fetchone():
        print("payment_config表存在")
        
        # 获取表结构
        cursor.execute("PRAGMA table_info(payment_config);")
        columns = cursor.fetchall()
        print("表结构:")
        for col in columns:
            print(f"字段: {col[1]}, 类型: {col[2]}")
        
        # 获取表数据
        cursor.execute("SELECT * FROM payment_config;")
        data = cursor.fetchall()
        print("\n表数据:")
        for row in data:
            print(row)
    else:
        print("payment_config表不存在")
except Exception as e:
    print(f"错误: {str(e)}")
finally:
    conn.close()