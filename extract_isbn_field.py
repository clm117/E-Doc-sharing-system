#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅对黑皮书目录的521个文件，提取[978 之后最近一个]之前的所有字符包含978作为ISBN
"""

import os
import cx_Oracle
import re


def extract_isbn_field():
    """
    仅对黑皮书目录的521个文件，提取[978 之后最近一个]之前的所有字符包含978作为ISBN
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
    
    # 处理file_isbn字段：提取[978 之后最近一个]之前的所有字符包含978
    def extract_isbn_from_filename(filename):
        # 匹配[978 开头，最近一个]之前的内容
        match = re.search(r'\[978[^\]]+', filename)
        if match:
            # 提取匹配的内容，去掉开头的[
            isbn = match.group(0).lstrip('[')
            return isbn
        # 如果没有匹配到，返回None
        return None
    
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
        
        # 更新记录的SQL语句
        update_sql = """
        UPDATE file_info
        SET FILE_ISBN = :extracted_isbn
        WHERE FILE_NAME = :file_name
        """
        
        updated_count = 0
        skipped_count = 0
        
        # 遍历每个黑皮书PDF文件
        for pdf_file in blackbook_files:
            try:
                # 从文件名中提取ISBN
                extracted_isbn = extract_isbn_from_filename(pdf_file)
                
                if extracted_isbn:
                    # 执行更新
                    cursor.execute(update_sql, {
                        'extracted_isbn': extracted_isbn,
                        'file_name': pdf_file
                    })
                    updated_count += 1
                    print(f"更新成功: {pdf_file}")
                    print(f"  ISBN: {extracted_isbn}")
                else:
                    skipped_count += 1
                    print(f"跳过: {pdf_file}（未找到符合要求的ISBN）")
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
        print(f"跳过: {skipped_count}条记录（未找到符合要求的ISBN）")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    extract_isbn_field()