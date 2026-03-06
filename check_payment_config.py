import sqlite3

# 检查SQLite的payment_config表结构
try:
    conn = sqlite3.connect('docshare.db')
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute('PRAGMA table_info(payment_config);')
    columns = cursor.fetchall()
    
    print('SQLite payment_config表结构:')
    for col in columns:
        print(f"字段名: {col[1]}, 类型: {col[2]}, 是否主键: {col[5]}")
    
    # 获取表数据
    cursor.execute('SELECT * FROM payment_config;')
    data = cursor.fetchall()
    
    print('\nSQLite payment_config表数据:')
    for row in data:
        print(row)
    
    conn.close()
except Exception as e:
    print(f"SQLite检查失败: {str(e)}")