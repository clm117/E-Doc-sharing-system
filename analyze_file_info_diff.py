#!/usr/bin/env python3
# 分析脚本：检查Oracle和SQLite中file_info表的差异

import sqlite3
import sys

# 尝试导入cx_Oracle
ORACLE_AVAILABLE = False
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    print("警告：未安装cx_Oracle，无法从Oracle数据库获取数据")

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 分析差异
def analyze_diff():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过分析")
        return
    
    print("开始分析Oracle和SQLite中file_info表的差异...")
    
    # 连接Oracle数据库
    try:
        oracle_conn = cx_Oracle.connect(**DB_CONFIG)
        oracle_cursor = oracle_conn.cursor()
        print("成功连接到Oracle数据库")
    except Exception as e:
        print(f"连接Oracle数据库失败: {str(e)}")
        return
    
    # 连接SQLite数据库
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()
    
    # 获取SQLite中已存在的file_id列表
    print("获取SQLite中已存在的file_id...")
    sqlite_cursor.execute("SELECT file_id FROM file_info")
    existing_file_ids = set([row[0] for row in sqlite_cursor.fetchall()])
    print(f"SQLite中已存在 {len(existing_file_ids)} 条记录")
    
    # 从Oracle获取所有file_info记录
    print("从Oracle获取file_info记录...")
    try:
        # 尝试基本字段查询
        oracle_cursor.execute("SELECT file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time FROM file_info")
        
        all_rows = oracle_cursor.fetchall()
        print(f"Oracle中共有 {len(all_rows)} 条file_info记录")
        
        # 过滤出SQLite中不存在的记录
        missing_rows = []
        for row in all_rows:
            file_id = row[0]
            if file_id not in existing_file_ids:
                missing_rows.append(row)
        
        print(f"SQLite中缺失 {len(missing_rows)} 条记录")
        
        # 显示前10条缺失的记录
        if missing_rows:
            print("\n前10条缺失的记录:")
            for row in missing_rows[:10]:
                print(f"  ID: {row[0]}, 名称: {row[1][:50]}...")
            
            # 尝试插入这些缺失的记录
            print("\n尝试插入缺失的记录...")
            inserted_count = 0
            for row in missing_rows:
                file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time = row
                
                # 处理日期字段
                if create_time and not isinstance(create_time, str):
                    create_time_str = create_time.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    create_time_str = create_time
                
                if update_time and not isinstance(update_time, str):
                    update_time_str = update_time.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    update_time_str = update_time
                
                try:
                    sqlite_cursor.execute(
                        "INSERT INTO file_info (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time, update_time, file_author, standard_name, search_keywords, file_tags, file_isbn, file_price_type, file_path, remark1, remark2, remark3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class, download_count, create_time_str, update_time_str, None, None, None, None, None, '1', None, None, None, None)
                    )
                    inserted_count += 1
                except Exception as e:
                    print(f"插入记录 {file_id} 失败: {str(e)}")
            
            sqlite_conn.commit()
            print(f"成功插入 {inserted_count} 条记录")
        else:
            print("没有缺失的记录")
            
    except Exception as e:
        print(f"分析失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 关闭连接
    oracle_cursor.close()
    oracle_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()
    print("差异分析完成")

# 验证结果
def verify_result():
    print("\n验证结果...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # 检查file_info表记录数
    cursor.execute("SELECT COUNT(*) FROM file_info")
    file_count = cursor.fetchone()[0]
    print(f"file_info表记录数: {file_count}")
    
    # 检查是否有重复的file_id
    cursor.execute("SELECT file_id, COUNT(*) FROM file_info GROUP BY file_id HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    if duplicates:
        print(f"发现 {len(duplicates)} 个重复的file_id")
    else:
        print("没有重复的file_id")
    
    conn.close()
    print("验证完成")

# 主函数
def main():
    print("开始分析file_info表差异...")
    
    # 分析差异
    analyze_diff()
    
    # 验证结果
    verify_result()
    
    print("差异分析完成！")

if __name__ == '__main__':
    main()
