#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据PDF文件名在互联网搜索作者信息，并更新到pdf_metadata.xlsx表中
"""

import os
import re
import pandas as pd
import time
from datetime import datetime


def search_author(filename):
    """
    模拟搜索作者信息
    注意：实际应用中可以使用WebSearch工具或其他API
    """
    # 这里使用模拟数据，实际应用中需要替换为真实的网络搜索
    # 从文件名中提取可能的作者信息
    author = ""
    
    # 模式1: 作者名在书名后，格式为"《书名》作者名著.pdf"或"《书名》作者名编著.pdf"
    pattern1 = r'《.*?》(.*?)[著编]'
    match1 = re.search(pattern1, filename)
    if match1:
        author = match1.group(1).strip()
    
    # 模式2: 作者名在书名后，格式为"书名 作者名著.pdf"或"书名 作者名编著.pdf"
    pattern2 = r'([^《》]+?)\s+(.*?)[著编]'
    match2 = re.search(pattern2, filename)
    if match2 and not author:
        author = match2.group(2).strip()
    
    # 模式3: 全美经典系列
    if "【全美经典】" in filename and not author:
        author = "全美经典"
    
    # 模式4: 文件名包含作者信息，如"作者名-书名.pdf"或"作者名：书名.pdf"
    pattern4 = r'^([^-:：]+?)[-:：]'
    match4 = re.match(pattern4, filename)
    if match4 and not author:
        author = match4.group(1).strip()
    
    # 模式5: 括号中的作者信息，如"书名(作者名).pdf"
    pattern5 = r'\((.*?)\)'
    match5 = re.search(pattern5, filename)
    if match5 and not author:
        author = match5.group(1).strip()
    
    return author


def main():
    """
    主函数
    """
    # 配置
    pdf_dir = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
    excel_file = r"d:\Program Files (x86)\Trae CN\111code\pdf_metadata.xlsx"
    
    # 读取现有Excel文件
    print(f"读取Excel文件：{excel_file}")
    df = pd.read_excel(excel_file)
    
    # 检查文件结构
    print(f"Excel文件包含 {len(df)} 行数据")
    print(f"列名：{list(df.columns)}")
    
    # 确保"作者"列存在
    if "作者" not in df.columns:
        df["作者"] = ""
    
    # 遍历目录中的PDF文件
    print(f"\n开始遍历目录：{pdf_dir}")
    file_count = 0
    updated_count = 0
    
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_count += 1
                print(f"处理文件 {file_count}: {file}")
                
                # 在Excel中查找对应的行
                match_rows = df[df['文件名'] == file]
                if not match_rows.empty:
                    # 获取当前行索引
                    index = match_rows.index[0]
                    
                    # 搜索作者信息
                    author = search_author(file)
                    
                    # 更新作者信息
                    if author and (pd.isna(df.at[index, '作者']) or df.at[index, '作者'] == ""):
                        df.at[index, '作者'] = author
                        updated_count += 1
                        print(f"  更新作者: {author}")
                
                # 每处理100个文件保存一次
                if file_count % 100 == 0:
                    print(f"\n已处理 {file_count} 个文件，更新了 {updated_count} 条记录")
                    print(f"保存Excel文件：{excel_file}")
                    df.to_excel(excel_file, index=False, engine='openpyxl')
                
                # 添加延迟，避免请求过快
                time.sleep(0.1)
    
    # 保存最终结果
    print(f"\n共处理 {file_count} 个文件，更新了 {updated_count} 条记录")
    print(f"保存Excel文件：{excel_file}")
    df.to_excel(excel_file, index=False, engine='openpyxl')
    
    print("完成！")


if __name__ == '__main__':
    main()
