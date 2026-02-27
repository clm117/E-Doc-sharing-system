#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Excel文件更新Oracle数据库file_info表
根据文件名关联，更新作者、标准化文件名、搜索关键字、标签和ISBN号
"""

import pandas as pd
import cx_Oracle
import logging
import time

# 配置日志，确保使用正确的编码
logging.basicConfig(
    level=logging.INFO,  # 恢复为INFO级别，减少日志量
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_file_info.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# Excel文件路径
EXCEL_FILE = 'pdf_metadata.xlsx'

# SQL更新语句
UPDATE_SQL = """
UPDATE file_info
SET FILE_AUTHOR = :author,
    STANDARD_NAME = :standard_name,
    SEARCH_KEYWORDS = :search_keywords,
    FILE_TAGS = :tags,
    FILE_ISBN = :isbn
WHERE FILE_NAME = :filename
"""

# 批次大小
BATCH_SIZE = 100

def update_file_info_from_excel():
    """从Excel文件更新file_info表"""
    start_time = time.time()
    logger.info("开始从Excel更新file_info表")
    
    try:
        # 1. 读取Excel文件
        logger.info(f"读取Excel文件: {EXCEL_FILE}")
        df = pd.read_excel(EXCEL_FILE)
        logger.info(f"成功读取 {len(df)} 行数据")
        
        # 2. 连接到Oracle数据库
        logger.info("连接到Oracle数据库")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 3. 准备数据和执行更新
        updated_count = 0
        error_count = 0
        
        for idx, row in df.iterrows():
            try:
                # 获取数据，处理空值和字段长度限制
                filename = row['文件名']
                
                # 处理AUTHOR字段，按字节长度截断（数据库按字节计算长度）
                author_raw = row['作者']
                author = None
                if pd.notna(author_raw):
                    author_str = str(author_raw)
                    # 按UTF-8字节长度截断，确保不超过90字节
                    author_bytes = author_str.encode('utf-8')[:90]  # 留10字节余量
                    # 转换回字符串
                    author = author_bytes.decode('utf-8', errors='ignore')
                    # 记录字节长度和字符长度
                    logger.info(f"第{idx+1}行：作者字段 - 字符长度：{len(author)}, 字节长度：{len(author_bytes)}, 值：{author[:50]}...")
                
                # 处理STANDARD_NAME字段，按字节长度截断
                standard_name_raw = row['标准化文件名']
                standard_name = None
                if pd.notna(standard_name_raw):
                    standard_name_str = str(standard_name_raw)
                    standard_name_bytes = standard_name_str.encode('utf-8')[:230]  # 留25字节余量
                    standard_name = standard_name_bytes.decode('utf-8', errors='ignore')
                
                # 处理SEARCH_KEYWORDS字段，按字节长度截断
                search_keywords_raw = row['搜索关键字']
                search_keywords = None
                if pd.notna(search_keywords_raw):
                    search_keywords_str = str(search_keywords_raw)
                    search_keywords_bytes = search_keywords_str.encode('utf-8')[:450]  # 留50字节余量
                    search_keywords = search_keywords_bytes.decode('utf-8', errors='ignore')
                
                # 处理TAGS字段，按字节长度截断
                tags_raw = row['标签']
                tags = None
                if pd.notna(tags_raw):
                    tags_str = str(tags_raw)
                    tags_bytes = tags_str.encode('utf-8')[:230]  # 留25字节余量
                    tags = tags_bytes.decode('utf-8', errors='ignore')
                
                # 处理ISBN字段，按字节长度截断
                isbn_raw = row['ISBN号']
                isbn = None
                if pd.notna(isbn_raw):
                    isbn_str = str(isbn_raw)
                    isbn_bytes = isbn_str.encode('utf-8')[:18]  # 留2字节余量
                    isbn = isbn_bytes.decode('utf-8', errors='ignore')
                
                # 执行更新，使用try-except捕获单个记录的错误
                try:
                    cursor.execute(UPDATE_SQL, {
                        'author': author,
                        'standard_name': standard_name,
                        'search_keywords': search_keywords,
                        'tags': tags,
                        'isbn': isbn,
                        'filename': filename
                    })
                    logger.debug(f"第{idx+1}行：执行更新，影响行数：{cursor.rowcount}")
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    logger.error(f"第{idx+1}行：数据库更新失败 - 错误码：{error.code}, 错误信息：{error.message}")
                    logger.error(f"第{idx+1}行：作者值：{author}, 长度：{len(author) if author else 0}")
                    raise
                
                updated_count += cursor.rowcount
                
                # 批次提交
                if (idx + 1) % BATCH_SIZE == 0:
                    connection.commit()
                    logger.info(f"已提交 {idx + 1} 条记录")
                    
            except Exception as e:
                error_count += 1
                logger.error(f"处理第 {idx + 1} 行数据失败: {str(e)}")
                logger.error(f"失败数据: {row.to_dict()}")
        
        # 提交剩余数据
        connection.commit()
        
        # 4. 关闭连接
        cursor.close()
        connection.close()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 5. 记录结果
        logger.info("更新完成!")
        logger.info(f"总记录数: {len(df)}")
        logger.info(f"成功更新: {updated_count}")
        logger.info(f"更新失败: {error_count}")
        logger.info(f"耗时: {elapsed_time:.2f} 秒")
        
        print(f"\n更新完成!")
        print(f"总记录数: {len(df)}")
        print(f"成功更新: {updated_count}")
        print(f"更新失败: {error_count}")
        print(f"耗时: {elapsed_time:.2f} 秒")
        
    except Exception as e:
        logger.error(f"更新过程中发生错误: {str(e)}")
        print(f"更新过程中发生错误: {str(e)}")

if __name__ == "__main__":
    update_file_info_from_excel()