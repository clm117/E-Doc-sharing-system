import sqlite3

# 连接数据库
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 检查所有记录
print("当前payment_config表所有记录:")
cursor.execute("SELECT * FROM payment_config")
rows = cursor.fetchall()
print(f"总记录数: {len(rows)}")
for row in rows:
    print(row)

# 按price_type查询
print("\n按price_type查询:")
cursor.execute("SELECT * FROM payment_config WHERE price_type = '1'")
rows_type1 = cursor.fetchall()
print(f"price_type=1的记录数: {len(rows_type1)}")
for row in rows_type1:
    print(row)

cursor.execute("SELECT * FROM payment_config WHERE price_type = '2'")
rows_type2 = cursor.fetchall()
print(f"price_type=2的记录数: {len(rows_type2)}")
for row in rows_type2:
    print(row)

# 关闭连接
conn.close()