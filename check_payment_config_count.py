import sqlite3

# 检查当前SQLite的payment_config表记录数
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM payment_config")
count = cursor.fetchone()[0]
print(f"当前payment_config表记录数: {count}")
cursor.execute("SELECT * FROM payment_config")
data = cursor.fetchall()
for row in data:
    print(row)
conn.close()