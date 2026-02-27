#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将指定目录下的PDF文件写入file_info表
"""

import os
import cx_Oracle
import random
import re


def insert_pdf_files():
    """
    将指定目录下的PDF文件写入file_info表
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
    
    # 生成6位随机数字密码
    def generate_6digit_password():
        return ''.join(random.choice('0123456789') for _ in range(6))
    
    # 从文件名提取作者信息：[***译制]中[]里"译制"前的文字
    def extract_author(filename):
        # 移除.pdf后缀
        name = os.path.splitext(filename)[0]
        # 匹配[***译制]格式，提取译制前的文字
        match = re.search(r'\[(.*?)译制\]', name)
        if match:
            return match.group(1).strip()
        # 如果没有[***译制]格式，返回默认值
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
    
    # 生成搜索关键字
    def generate_search_keywords(filename):
        # 简单实现，可根据实际情况调整
        name = os.path.splitext(filename)[0]
        # 移除特殊字符，保留主要词语
        keywords = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', name)
        # 分割为关键词列表
        keyword_list = keywords.split()
        # 去重并限制长度
        unique_keywords = list(set(keyword_list))[:10]  # 最多10个关键字
        return ",".join(unique_keywords)
    
    # 提取ISBN号：出版社后面的字符
    def extract_isbn(filename):
        # 移除.pdf后缀
        name = os.path.splitext(filename)[0]
        # 匹配出版社后面的ISBN号格式 [ISBN]
        # 示例：[机械工业出版社][978-7-111-71236-7]
        match = re.search(r'\[.*?出版社\]\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', name)
        if match:
            return match.group(1).strip()
        # 如果没有匹配到，尝试直接匹配ISBN格式
        match = re.search(r'\[(\d{1,5}-\d{1,7}-\d{1,6}-\d{1,3}|\d{13})\]', name)
        if match:
            return match.group(1).strip()
        # 如果没有ISBN号，返回空
        return None
    
    # 生成文件标签
    def generate_file_tags(filename):
        # 简单实现，可根据实际情况调整
        # 基于文件名内容生成标签
        name = os.path.splitext(filename)[0].lower()
        tags = []
        
        # 计算机相关标签
        if any(word in name for word in ['计算机', '编程', '代码', '软件', '算法', '数据']):
            tags.append('计算机科学')
        if any(word in name for word in ['c语言', 'c++', 'c#', 'cpp']):
            tags.append('C语言')
        if 'python' in name:
            tags.append('Python')
        if 'java' in name:
            tags.append('Java')
        if any(word in name for word in ['数据库', 'sql', 'oracle', 'mysql']):
            tags.append('数据库')
        if any(word in name for word in ['网络', 'web', '互联网']):
            tags.append('网络技术')
        
        # 通用标签
        if any(word in name for word in ['基础', '入门', '教程']):
            tags.append('基础教程')
        if any(word in name for word in ['高级', '进阶', '深入']):
            tags.append('高级进阶')
        if '原理' in name:
            tags.append('原理分析')
        if '实践' in name:
            tags.append('实践指南')
        
        # 去重
        unique_tags = list(set(tags))
        # 如果没有生成标签，添加默认标签
        if not unique_tags:
            unique_tags.append('计算机科学')
        
        return ",".join(unique_tags)
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 获取目录下的所有PDF文件（包括子目录）
        pdf_files = []
        for root, dirs, files in os.walk(pdf_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file)
        
        print(f"找到{len(pdf_files)}个PDF文件")
        
        # 插入记录的SQL语句
        insert_sql = """
        INSERT INTO file_info (
            file_id, file_name, file_password, 
            file_author, standard_name, search_keywords, file_tags,
            file_isbn, download_count, file_price_type
        ) VALUES (
            :file_id, :file_name, :file_password, 
            :file_author, :standard_name, :search_keywords, :file_tags,
            :file_isbn, 0, :file_price_type
        )
        """
        
        inserted_count = 0
        skipped_count = 0
        
        # 遍历每个PDF文件
        for pdf_file in pdf_files:
            # 生成随机6位密码
            file_password = generate_6digit_password()
            
            # 提取或生成字段值
            file_author = extract_author(pdf_file)
            standard_name = generate_standard_name(pdf_file)
            search_keywords = generate_search_keywords(pdf_file)
            file_tags = generate_file_tags(pdf_file)
            file_isbn = extract_isbn(pdf_file)
            
            # 准备插入的数据
            data = {
                'file_id': None,  # 设为NULL，由触发器自动生成
                'file_name': pdf_file,
                'file_password': file_password,
                'file_author': file_author,
                'standard_name': standard_name,
                'search_keywords': search_keywords,
                'file_tags': file_tags,
                'file_isbn': file_isbn,
                'file_price_type': 1  # 根据要求，所有记录设为1
            }
            
            try:
                # 执行插入
                cursor.execute(insert_sql, data)
                inserted_count += 1
                print(f"插入成功：{pdf_file}")
            except cx_Oracle.IntegrityError as e:
                # 唯一约束冲突，文件已存在
                if "UK_FILE_INFO_FILE_NAME" in str(e):
                    skipped_count += 1
                    print(f"跳过已存在的文件：{pdf_file}")
                else:
                    # 其他完整性错误
                    print(f"插入失败 {pdf_file}: {str(e)}")
            except Exception as e:
                # 其他错误
                print(f"插入失败 {pdf_file}: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n操作完成！")
        print(f"成功插入: {inserted_count}个文件")
        print(f"跳过已存在: {skipped_count}个文件")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    insert_pdf_files()
