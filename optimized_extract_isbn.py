#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版本：仅对黑皮书目录的521个文件，精确提取[978 之后最近一个]之前的所有字符包含978作为ISBN
"""

import os
import cx_Oracle
import re


def optimized_extract_isbn():
    """
    优化版本：仅对黑皮书目录的521个文件，精确提取[978 之后最近一个]之前的所有字符包含978作为ISBN
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
    
    # 优化的ISBN提取函数：精确匹配[978 之后最近一个]之前的所有字符
    def extract_isbn_optimized(filename):
        # 精确匹配[978开头，后面跟任意字符（包括空格），直到最近的]结束
        # 使用非贪婪匹配确保只匹配到最近的]
        match = re.search(r'\[978[^\]]*\]', filename)
        if match:
            # 提取匹配的内容，去掉开头的[和结尾的]
            isbn_content = match.group(0).strip('[]')
            # 确保内容包含978
            if '978' in isbn_content:
                return isbn_content.strip()
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
                extracted_isbn = extract_isbn_optimized(pdf_file)
                
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
                    # 打印详细的文件名，方便调试
                    print(f"  完整文件名: {pdf_file}")
            except Exception as e:
                # 其他错误
                skipped_count += 1
                print(f"处理失败 {pdf_file}: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n操作完成！")
        print(f"成功更新: {updated_count}条记录")
        print(f"跳过: {skipped_count}条记录")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    optimized_extract_isbn()