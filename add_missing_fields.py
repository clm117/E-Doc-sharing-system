#!/usr/bin/env python3
# 添加缺失的字段到file_info表

import sqlite3

# SQLite数据库路径
DB_PATH = 'docshare.db'

# 添加缺失的字段
def add_missing_fields():
    print("添加缺失的字段...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查file_author字段是否存在
        cursor.execute("PRAGMA table_info(file_info);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'file_author' not in columns:
            # 添加file_author字段
            cursor.execute("ALTER TABLE file_info ADD COLUMN file_author TEXT DEFAULT NULL;")
            print("添加file_author字段成功")
        else:
            print("file_author字段已存在")
        
        # 创建file_author字段的索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_author ON file_info(file_author);")
        print("创建file_author字段索引成功")
        
        conn.commit()
        print("字段添加和索引创建完成")
        
    except Exception as e:
        print(f"添加字段时出错: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# 检查表结构
def check_table_structure():
    print("\n检查表结构...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查file_info表结构
        cursor.execute("PRAGMA table_info(file_info);")
        file_info_columns = cursor.fetchall()
        print("file_info表字段:")
        for column in file_info_columns:
            print(f"  {column[1]} ({column[2]})")
        
    except Exception as e:
        print(f"检查表结构时出错: {str(e)}")
    finally:
        conn.close()

# 主函数
def main():
    print("开始添加缺失的字段...")
    add_missing_fields()
    check_table_structure()
    print("\n操作完成！")

if __name__ == '__main__':
    main()
