import sqlite3

# 连接SQLite数据库
conn = sqlite3.connect('docshare.db')
cursor = conn.cursor()

# 清空表
cursor.execute("DELETE FROM payment_config")
print("已清空payment_config表")

# 插入两条记录
records = [
    (1, '1', 3.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y', '2026-01-12 16:33:23', '2026-01-12 16:33:23'),
    (2, '2', 5.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买 高级配置', 'Y', '2026-01-13 09:25:42', '2026-01-13 09:25:42')
]

for record in records:
    cursor.execute(
        "INSERT INTO payment_config (config_id, price_type, amount, payment_url, description, status, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        record
    )
    print(f"已插入记录: {record}")

# 提交事务
conn.commit()
print("数据提交成功")

# 验证结果
cursor.execute("SELECT COUNT(*) FROM payment_config")
count = cursor.fetchone()[0]
print(f"\n当前payment_config表记录数: {count}")

cursor.execute("SELECT * FROM payment_config")
data = cursor.fetchall()
for row in data:
    print(row)

# 关闭连接
conn.close()
print("操作完成")