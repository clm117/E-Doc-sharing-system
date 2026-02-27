#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用WebSearch工具根据标准化文件名搜索作者信息，并更新到pdf_metadata.xlsx表中
"""

import os
import pandas as pd
import time
from datetime import datetime

# 导入WebSearch工具
from WebSearch import web_search


def search_author_online(standard_name):
    """
    使用WebSearch工具在互联网上搜索作者信息
    """
    try:
        # 构建搜索查询
        query = f"{standard_name} 作者 书籍"
        print(f"搜索查询: {query}")
        
        # 使用WebSearch工具搜索
        results = web_search(query, num=3)
        
        # 解析搜索结果，提取作者信息
        author = ""
        if results:
            # 这里需要根据实际的WebSearch结果格式进行解析
            # 假设results返回的是包含搜索结果的列表，每个结果包含标题和摘要
            for result in results:
                # 从标题和摘要中提取作者信息
                # 这里需要根据实际情况调整提取逻辑
                if "作者" in result.get("title", "") or "作者" in result.get("snippet", ""):
                    # 简单示例：从摘要中提取作者信息
                    snippet = result.get("snippet", "")
                    # 假设作者信息格式为"作者：XXX"或"作者XXX"
                    if "作者：" in snippet:
                        author = snippet.split("作者：")[1].split(" ")[0]
                    elif "作者" in snippet:
                        author = snippet.split("作者")[1].split(" ")[0]
                    break
        
        return author.strip()
    except Exception as e:
        print(f"搜索失败: {str(e)}")
        return ""


def main():
    """
    主函数
    """
    # 配置
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
    
    # 确保"标准化文件名"列存在
    if "标准化文件名" not in df.columns:
        print("错误：Excel文件中没有'标准化文件名'列")
        return
    
    # 遍历Excel中的每一行
    print(f"\n开始搜索作者信息...")
    updated_count = 0
    
    for index, row in df.iterrows():
        standard_name = row["标准化文件名"]
        current_author = row["作者"]
        
        # 只处理标准化文件名不为空且当前作者为空的行
        if pd.notna(standard_name) and standard_name and (pd.isna(current_author) or current_author == ""):
            print(f"处理第 {index + 1} 行: {standard_name}")
            
            # 搜索作者信息
            author = search_author_online(standard_name)
            
            # 更新作者信息
            if author:
                df.at[index, "作者"] = author
                updated_count += 1
                print(f"  更新作者: {author}")
            
            # 添加延迟，避免请求过快
            time.sleep(1)
        
        # 每处理10行保存一次
        if (index + 1) % 10 == 0:
            print(f"\n已处理 {index + 1} 行，更新了 {updated_count} 条记录")
            print(f"保存Excel文件：{excel_file}")
            df.to_excel(excel_file, index=False, engine='openpyxl')
    
    # 保存最终结果
    print(f"\n共处理 {len(df)} 行，更新了 {updated_count} 条记录")
    print(f"保存Excel文件：{excel_file}")
    df.to_excel(excel_file, index=False, engine='openpyxl')
    
    print("完成！")


if __name__ == '__main__':
    main()
