#!/usr/bin/env python3
# 更新file_info表，添加缺失的字段

import sqlite3

# SQLite数据库路径
DB_PATH = 'docshare.db'

# 更新file_info表结构
def update_file_info_table():
    print("更新file_info表结构...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查file_price_type字段是否存在
        cursor.execute("PRAGMA table_info(file_info);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'file_price_type' not in columns:
            # 添加file_price_type字段
            cursor.execute("ALTER TABLE file_info ADD COLUMN file_price_type TEXT DEFAULT '1';")
            print("添加file_price_type字段成功")
            
            # 创建file_price_type字段的索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_price_type ON file_info(file_price_type);")
            print("创建file_price_type字段索引成功")
        else:
            print("file_price_type字段已存在")
        
        conn.commit()
        print("表结构更新完成")
        
    except Exception as e:
        print(f"更新表结构时出错: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# 主函数
def main():
    print("开始更新file_info表结构...")
    update_file_info_table()
    print("\n操作完成！")

if __name__ == '__main__':
    main()
