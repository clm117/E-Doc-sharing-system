#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新file_info表中已存在记录的file_author、file_isbn字段
"""

import os
import cx_Oracle
import re


def update_existing_records():
    """
    更新file_info表中已存在记录的file_author、file_isbn字段
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    # 从文件名提取作者信息：[***译制]中[]里"译制"前的文字
    def extract_author(filename):
        # 匹配[***译制]格式，提取译制前的文字
        match = re.search(r'\[(.*?)译制\]', filename)
        if match:
            return match.group(1).strip()
        # 如果没有[***译制]格式，尝试匹配[***编著]格式
        match = re.search(r'\[(.*?)编著\]', filename)
        if match:
            return match.group(1).strip()
        # 如果没有明显的作者标识，返回默认值
        return "未知作者"
    
    # 提取ISBN号：出版社后面的字符
    def extract_isbn(filename):
        # 匹配出版社后面的ISBN号格式 [ISBN]
        # 示例：[机械工业出版社][978-7-111-71236-7]
        match = re.search(r'\[.*?出版社\]\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', filename)
        if match:
            return match.group(1).strip()
        # 如果没有匹配到，尝试直接匹配ISBN格式
        match = re.search(r'\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', filename)
        if match:
            return match.group(1).strip()
        # 如果没有ISBN号，返回空
        return None
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询所有已存在的记录
        cursor.execute("SELECT FILE_NAME FROM file_info")
        existing_records = cursor.fetchall()
        
        print(f"找到{len(existing_records)}条已存在记录")
        
        # 更新记录的SQL语句
        update_sql = """
        UPDATE file_info
        SET FILE_AUTHOR = :file_author,
            FILE_ISBN = :file_isbn
        WHERE FILE_NAME = :file_name
        """
        
        updated_count = 0
        
        # 遍历每个已存在的记录
        for record in existing_records:
            file_name = record[0]
            
            # 提取或生成字段值
            file_author = extract_author(file_name)
            file_isbn = extract_isbn(file_name)
            
            # 准备更新的数据
            data = {
                'file_author': file_author,
                'file_isbn': file_isbn,
                'file_name': file_name
            }
            
            try:
                # 执行更新
                cursor.execute(update_sql, data)
                updated_count += cursor.rowcount
                print(f"更新成功：{file_name}")
            except Exception as e:
                # 其他错误
                print(f"更新失败 {file_name}: {str(e)}")
        
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
    update_existing_records()