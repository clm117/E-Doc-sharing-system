import sqlite3

# 连接SQLite数据库
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 1. 检查表结构
print("1. 检查表结构:")
cursor.execute("PRAGMA table_info(payment_config);")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]}")

# 2. 检查当前记录
print("\n2. 检查当前记录:")
cursor.execute("SELECT * FROM payment_config;")
rows = cursor.fetchall()
print(f"当前记录数: {len(rows)}")
for row in rows:
    print(row)

# 3. 清空表并插入两条记录
print("\n3. 清空表并插入两条记录:")
cursor.execute("DELETE FROM payment_config")
print("已清空表")

# 插入两条记录
record1 = (1, '1', 3.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y', '2026-01-12 16:33:23', '2026-01-12 16:33:23', 'CNY', 'alipay', 3600, None, 0.01)
record2 = (2, '2', 5.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买 高级配置', 'Y', '2026-01-13 09:25:42', '2026-01-13 09:25:42', 'CNY', 'alipay', 3600, None, 0.01)

# 动态构建插入语句，根据表结构
cursor.execute("PRAGMA table_info(payment_config);")
cols = [col[1] for col in cursor.fetchall()]
col_str = ', '.join(cols)
placeholders = ', '.join(['?' for _ in cols])

insert_sql = f"INSERT INTO payment_config ({col_str}) VALUES ({placeholders})"

cursor.execute(insert_sql, record1)
cursor.execute(insert_sql, record2)

# 提交事务
conn.commit()
print("已插入两条记录")

# 4. 验证结果
print("\n4. 验证结果:")
cursor.execute("SELECT * FROM payment_config;")
rows = cursor.fetchall()
print(f"当前记录数: {len(rows)}")
for row in rows:
    print(row)

# 关闭连接
conn.close()
print("\n操作完成！")