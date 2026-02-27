#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据PDF文件生成包含作者、标准化文件名、搜索关键字、标签、ISBN号的Excel表
"""

import os
import re
import pandas as pd
from datetime import datetime


def extract_author_from_filename(filename):
    """
    从文件名中提取作者信息
    """
    # 模式1: 作者名在书名后，格式为"《书名》作者名著.pdf"或"《书名》作者名编著.pdf"
    pattern1 = r'《.*?》(.*?)[著编]'
    match1 = re.search(pattern1, filename)
    if match1:
        return match1.group(1).strip()
    
    # 模式2: 作者名在书名后，格式为"书名 作者名著.pdf"或"书名 作者名编著.pdf"
    pattern2 = r'([^《》]+?)\s+(.*?)[著编]'
    match2 = re.search(pattern2, filename)
    if match2:
        return match2.group(2).strip()
    
    # 模式3: 全美经典系列，作者信息不明确
    if "【全美经典】" in filename:
        return "全美经典"
    
    # 其他情况
    return ""


def generate_standard_filename(filename):
    """
    生成标准化文件名
    """
    # 移除前缀数字和特殊字符
    standard_name = re.sub(r'^[\d.、，【】\s]+', '', filename)
    # 移除文件扩展名
    standard_name = os.path.splitext(standard_name)[0]
    # 移除作者信息
    standard_name = re.sub(r'[《》].*?[《》]', '', standard_name)
    standard_name = re.sub(r'\s+.*?[著编]', '', standard_name)
    return standard_name.strip()


def generate_search_keywords(filename, standard_name):
    """
    生成搜索关键字
    """
    # 从文件名和标准化文件名中提取关键字
    keywords = []
    
    # 添加标准化文件名作为关键字
    keywords.append(standard_name)
    
    # 提取文件名中的数字前缀（如果有）
    prefix_match = re.match(r'^([\d.]+)', filename)
    if prefix_match:
        keywords.append(prefix_match.group(1))
    
    # 添加文件类型关键字
    keywords.append("PDF")
    
    # 添加类别关键字
    if "全美经典" in filename:
        keywords.append("全美经典")
    elif "素质教育文库" in filename:
        keywords.append("素质教育文库")
    elif "图灵" in filename:
        keywords.append("图灵")
    elif "马克思" in filename or "恩格斯" in filename or "列宁" in filename:
        keywords.append("经典著作")
    
    return ",".join(keywords)


def generate_tags(filename):
    """
    生成标签
    """
    tags = []
    
    # 根据文件名内容添加标签
    if "数学" in filename or "几何" in filename or "代数" in filename or "微积分" in filename:
        tags.append("数学")
    if "物理" in filename or "力学" in filename or "电磁" in filename:
        tags.append("物理")
    if "化学" in filename:
        tags.append("化学")
    if "历史" in filename or "通史" in filename or "古代史" in filename:
        tags.append("历史")
    if "教育" in filename or "教学" in filename or "教案" in filename:
        tags.append("教育")
    if "Python" in filename or "编程" in filename or "计算机" in filename or "软件" in filename:
        tags.append("计算机")
    if "心理学" in filename or "心理" in filename:
        tags.append("心理学")
    if "医学" in filename or "中医" in filename or "中药" in filename:
        tags.append("医学")
    if "文学" in filename or "小说" in filename or "散文" in filename:
        tags.append("文学")
    if "哲学" in filename:
        tags.append("哲学")
    if "经济" in filename or "金融" in filename:
        tags.append("经济")
    
    # 添加通用标签
    tags.append("电子书")
    tags.append("PDF")
    
    return ",".join(tags)


def get_isbn(filename):
    """
    尝试获取ISBN号
    注意：从文件名中很难获取ISBN号，这里返回空字符串
    实际应用中可以通过互联网搜索获取
    """
    # 从文件名中搜索ISBN号
    isbn_pattern = r'ISBN[：:]?\s*([0-9-]+)'
    match = re.search(isbn_pattern, filename)
    if match:
        return match.group(1)
    
    # 从文件名中搜索13位数字的ISBN
    isbn13_pattern = r'978[-]?\d{1,5}[-]?\d{1,7}[-]?\d{1,6}[-]?\d{1}'
    match13 = re.search(isbn13_pattern, filename)
    if match13:
        return match13.group(0)
    
    return ""


def main():
    """
    主函数
    """
    # 配置
    pdf_dir = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
    output_file = r"d:\Program Files (x86)\Trae CN\111code\pdf_metadata.xlsx"
    
    # 初始化数据列表
    data = []
    
    # 遍历目录中的PDF文件
    print(f"开始遍历目录：{pdf_dir}")
    file_count = 0
    
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_count += 1
                print(f"处理文件 {file_count}: {file}")
                
                # 构建完整文件路径
                file_path = os.path.join(root, file)
                
                # 提取元数据
                author = extract_author_from_filename(file)
                standard_name = generate_standard_filename(file)
                search_keywords = generate_search_keywords(file, standard_name)
                tags = generate_tags(file)
                isbn = get_isbn(file)
                
                # 添加到数据列表
                data.append({
                    '文件名': file,
                    '作者': author,
                    '标准化文件名': standard_name,
                    '搜索关键字': search_keywords,
                    '标签': tags,
                    'ISBN号': isbn
                })
    
    # 生成Excel文件
    print(f"\n共处理 {file_count} 个文件")
    print(f"生成Excel文件：{output_file}")
    
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print("完成！")


if __name__ == '__main__':
    main()
