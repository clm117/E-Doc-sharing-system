#!/usr/bin/env python3
# 迁移脚本：更新file_info表中缺失的字段数据

import sqlite3
import sys

# 尝试导入cx_Oracle
ORACLE_AVAILABLE = False
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    print("警告：未安装cx_Oracle，无法从Oracle数据库迁移数据")

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 检查并更新缺失字段
def update_missing_fields():
    if not ORACLE_AVAILABLE:
        print("无法连接Oracle数据库，跳过数据迁移")
        return
    
    print("开始检查并更新file_info表中缺失的字段数据...")
    
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
    
    # 检查SQLite表中这些字段的当前状态
    print("检查SQLite表中缺失字段的当前状态...")
    sqlite_cursor.execute("SELECT file_id, file_author, standard_name, search_keywords, file_tags, file_isbn FROM file_info LIMIT 10")
    sample_rows = sqlite_cursor.fetchall()
    print("前10条记录的缺失字段状态:")
    for row in sample_rows:
        print(f"ID: {row[0]}, author: '{row[1]}', standard: '{row[2]}', keywords: '{row[3]}', tags: '{row[4]}', isbn: '{row[5]}'")
    
    # 从Oracle获取完整的字段数据
    print("从Oracle获取完整的字段数据...")
    try:
        # 尝试获取包含所有字段的查询
        query_tries = [
            "SELECT file_id, file_author, standard_name, search_keywords, file_tags, file_isbn FROM file_info",
            "SELECT file_id, file_author, standard_name, search_keywords, file_tags FROM file_info",
            "SELECT file_id, file_author FROM file_info"
        ]
        
        oracle_rows = []
        for query in query_tries:
            try:
                oracle_cursor.execute(query)
                oracle_rows = oracle_cursor.fetchall()
                print(f"成功执行查询: {query[:100]}...")
                print(f"获取到 {len(oracle_rows)} 条记录")
                break
            except Exception as e:
                print(f"查询失败: {str(e)}")
                print("尝试下一个查询...")
                continue
        
        if not oracle_rows:
            print("无法从Oracle获取字段数据")
            return
        
        # 更新SQLite表中的字段
        print("更新SQLite表中的字段数据...")
        updated_count = 0
        
        for row in oracle_rows:
            file_id = row[0]
            
            # 根据返回的字段数量确定如何处理
            if len(row) == 6:
                file_author, standard_name, search_keywords, file_tags, file_isbn = row[1:]
            elif len(row) == 5:
                file_author, standard_name, search_keywords, file_tags = row[1:]
                file_isbn = None
            elif len(row) == 2:
                file_author = row[1]
                standard_name = None
                search_keywords = None
                file_tags = None
                file_isbn = None
            else:
                continue
            
            try:
                sqlite_cursor.execute(
                    "UPDATE file_info SET file_author = ?, standard_name = ?, search_keywords = ?, file_tags = ?, file_isbn = ? WHERE file_id = ?",
                    (file_author, standard_name, search_keywords, file_tags, file_isbn, file_id)
                )
                updated_count += 1
                if updated_count % 100 == 0:
                    print(f"已更新 {updated_count} 条记录...")
            except Exception as e:
                print(f"更新记录 {file_id} 失败: {str(e)}")
        
        sqlite_conn.commit()
        print(f"成功更新 {updated_count} 条记录")
        
    except Exception as e:
        print(f"更新字段数据失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 验证更新结果
    print("验证更新结果...")
    sqlite_cursor.execute("SELECT file_id, file_author, standard_name, search_keywords, file_tags, file_isbn FROM file_info LIMIT 10")
    updated_sample = sqlite_cursor.fetchall()
    print("更新后的前10条记录:")
    for row in updated_sample:
        print(f"ID: {row[0]}, author: '{row[1]}', standard: '{row[2]}', keywords: '{row[3]}', tags: '{row[4]}', isbn: '{row[5]}'")
    
    # 统计有值的记录数
    sqlite_cursor.execute("SELECT COUNT(*) FROM file_info WHERE file_author IS NOT NULL OR file_author != ''")
    author_count = sqlite_cursor.fetchone()[0]
    print(f"\nfile_author字段有值的记录数: {author_count}")
    
    sqlite_cursor.execute("SELECT COUNT(*) FROM file_info WHERE standard_name IS NOT NULL OR standard_name != ''")
    standard_count = sqlite_cursor.fetchone()[0]
    print(f"standard_name字段有值的记录数: {standard_count}")
    
    sqlite_cursor.execute("SELECT COUNT(*) FROM file_info WHERE search_keywords IS NOT NULL OR search_keywords != ''")
    keywords_count = sqlite_cursor.fetchone()[0]
    print(f"search_keywords字段有值的记录数: {keywords_count}")
    
    sqlite_cursor.execute("SELECT COUNT(*) FROM file_info WHERE file_tags IS NOT NULL OR file_tags != ''")
    tags_count = sqlite_cursor.fetchone()[0]
    print(f"file_tags字段有值的记录数: {tags_count}")
    
    sqlite_cursor.execute("SELECT COUNT(*) FROM file_info WHERE file_isbn IS NOT NULL OR file_isbn != ''")
    isbn_count = sqlite_cursor.fetchone()[0]
    print(f"file_isbn字段有值的记录数: {isbn_count}")
    
    # 关闭连接
    oracle_cursor.close()
    oracle_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()
    print("字段更新完成")

# 主函数
def main():
    print("开始更新file_info表中缺失的字段数据...")
    
    # 更新缺失字段
    update_missing_fields()
    
    print("字段更新完成！")

if __name__ == '__main__':
    main()
