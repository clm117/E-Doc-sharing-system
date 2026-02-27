#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅对黑皮书目录的521个文件，清除file_author中最后一个[之前的包含这个[的所有字符
"""

import os
import cx_Oracle


def clean_author_field():
    """
    仅对黑皮书目录的521个文件，清除file_author中最后一个[之前的包含这个[的所有字符
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    # PDF文件目录
    pdf_dir = r"D:\2.enjoy\2.学习资料\【162】 计算机科学丛书（黑皮书500+）"
    
    # 处理file_author字段：清除最后一个[之前的包含这个[的所有字符
    def clean_author(author):
        if not author:
            return author
        # 找到最后一个[的位置
        last_bracket_pos = author.rfind('[')
        if last_bracket_pos != -1:
            # 清除最后一个[之前的所有字符，包括这个[
            return author[last_bracket_pos + 1:]
        # 如果没有[，直接返回
        return author
    
    try:
        # 获取黑皮书目录下的所有PDF文件
        blackbook_files = []
        for root, dirs, files in os.walk(pdf_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    blackbook_files.append(file)
        
        print(f"找到{len(blackbook_files)}个黑皮书PDF文件")
        
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询这些文件的当前file_author值
        print("\n=== 查询当前file_author值 ===")
        select_sql = "SELECT FILE_NAME, FILE_AUTHOR FROM file_info WHERE FILE_NAME = :file_name"
        
        # 更新记录的SQL语句
        update_sql = """
        UPDATE file_info
        SET FILE_AUTHOR = :cleaned_author
        WHERE FILE_NAME = :file_name
        """
        
        updated_count = 0
        
        # 遍历每个黑皮书PDF文件
        for pdf_file in blackbook_files:
            try:
                # 查询当前file_author值
                cursor.execute(select_sql, {'file_name': pdf_file})
                result = cursor.fetchone()
                if result:
                    file_name, current_author = result
                    # 处理file_author字段
                    cleaned_author = clean_author(current_author)
                    
                    # 如果有变化，执行更新
                    if current_author != cleaned_author:
                        # 执行更新
                        cursor.execute(update_sql, {
                            'cleaned_author': cleaned_author,
                            'file_name': file_name
                        })
                        updated_count += 1
                        print(f"更新: {file_name}")
                        print(f"  原作者: {current_author}")
                        print(f"  处理后: {cleaned_author}")
                    else:
                        print(f"跳过: {file_name}（无需处理）")
                else:
                    print(f"跳过: {file_name}（数据库中不存在）")
            except Exception as e:
                # 其他错误
                print(f"处理失败 {pdf_file}: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n操作完成！")
        print(f"成功更新: {updated_count}条记录")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    clean_author_field()