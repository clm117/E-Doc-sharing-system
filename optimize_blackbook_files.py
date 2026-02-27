#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅对黑皮书目录的521个文件优化file_info表中的数据
"""

import os
import cx_Oracle
import re


def optimize_blackbook_files():
    """
    仅对黑皮书目录的521个文件优化file_info表中的数据
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
    
    # 从文件名提取作者信息：[***译制]中[]里译制前面，最近的[后面的文字
    def extract_author(filename):
        # 匹配[***译制]格式，提取译制前的文字
        matches = re.findall(r'\[(.*?)译制\]', filename)
        if matches:
            # 获取最后一个匹配项
            return matches[-1].strip()
        # 如果没有[***译制]格式，尝试匹配[***编著]格式
        matches = re.findall(r'\[(.*?)编著\]', filename)
        if matches:
            return matches[-1].strip()
        # 如果没有明显的作者标识，返回默认值
        return "未知作者"
    
    # 生成标准化文件名：去掉《》
    def generate_standard_name(filename):
        # 移除.pdf后缀并处理特殊字符
        name = os.path.splitext(filename)[0]
        # 移除《》符号
        name = name.replace('《', '').replace('》', '')
        # 移除可能的括号内容和特殊字符
        name = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}', '', name)
        # 移除多余的空格
        name = re.sub(r'\s+', ' ', name).strip()
        return name
    
    # 提取ISBN号：出版社后面的字符
    def extract_isbn(filename):
        # 移除.pdf后缀
        name = os.path.splitext(filename)[0]
        # 匹配出版社后面的ISBN号格式 [ISBN]
        # 示例：[机械工业出版社][978-7-111-16513-2]
        match = re.search(r'\[.*?出版社\]\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', name)
        if match:
            return match.group(1).strip()
        # 如果没有匹配到，尝试直接匹配ISBN格式
        match = re.search(r'\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', name)
        if match:
            return match.group(1).strip()
        # 如果没有ISBN号，返回空
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
        SET FILE_AUTHOR = :file_author,
            STANDARD_NAME = :standard_name,
            FILE_ISBN = :file_isbn
        WHERE FILE_NAME = :file_name
        """
        
        updated_count = 0
        skipped_count = 0
        
        # 遍历每个黑皮书PDF文件
        for pdf_file in blackbook_files:
            # 提取字段值
            file_author = extract_author(pdf_file)
            standard_name = generate_standard_name(pdf_file)
            file_isbn = extract_isbn(pdf_file)
            
            # 准备更新的数据
            data = {
                'file_author': file_author,
                'standard_name': standard_name,
                'file_isbn': file_isbn,
                'file_name': pdf_file
            }
            
            try:
                # 执行更新
                cursor.execute(update_sql, data)
                if cursor.rowcount > 0:
                    updated_count += cursor.rowcount
                    print(f"更新成功：{pdf_file}")
                else:
                    skipped_count += 1
                    print(f"跳过：{pdf_file}（数据库中不存在）")
            except Exception as e:
                # 其他错误
                print(f"更新失败 {pdf_file}: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n操作完成！")
        print(f"成功更新: {updated_count}条记录")
        print(f"跳过: {skipped_count}条记录（数据库中不存在）")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    optimize_blackbook_files()