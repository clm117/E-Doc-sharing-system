import sqlite3

# 检查当前SQLite的payment_config表内容
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info(payment_config);")
columns = cursor.fetchall()
print("表结构:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# 检查数据
cursor.execute("SELECT * FROM payment_config;")
data = cursor.fetchall()
print(f"\n当前记录数: {len(data)}")
for row in data:
    print(f"  {row}")

conn.close()