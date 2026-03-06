import sqlite3

# 连接SQLite数据库
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 检查表是否存在
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment_config';")
if cursor.fetchone():
    print("payment_config表存在")
    
    # 检查记录数
    cursor.execute("SELECT COUNT(*) FROM payment_config")
    count = cursor.fetchone()[0]
    print(f"记录数: {count}")
    
    # 检查所有记录
    cursor.execute("SELECT * FROM payment_config")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
else:
    print("payment_config表不存在")

# 关闭连接
conn.close()