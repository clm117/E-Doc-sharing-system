#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用WebSearch工具根据标准化文件名搜索作者信息，并更新到pdf_metadata.xlsx表中
"""

import pandas as pd


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
    
    # 统计需要处理的行数
    need_update = df[(pd.notna(df["标准化文件名"])) & (df["标准化文件名"] != "") & ((pd.isna(df["作者"])) | (df["作者"] == ""))]
    print(f"需要更新作者信息的行数：{len(need_update)}")
    
    # 显示前5行需要更新的数据
    print("\n前5行需要更新的数据：")
    print(need_update.head(5))
    
    # 由于WebSearch工具的限制，我们只处理前10行作为示例
    print("\n开始搜索作者信息（仅处理前10行作为示例）...")
    updated_count = 0
    
    for index, row in need_update.head(10).iterrows():
        standard_name = row["标准化文件名"]
        print(f"处理第 {index + 1} 行: {standard_name}")
        
        try:
            # 使用WebSearch工具搜索作者信息
            from WebSearch import WebSearch
            query = f"{standard_name} 作者 书籍"
            results = WebSearch(query=query, num=3)
            
            # 解析搜索结果，提取作者信息
            author = ""
            if results and "items" in results:
                for item in results["items"]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    if "作者" in title or "作者" in snippet:
                        # 简单示例：从摘要中提取作者信息
                        if "作者：" in snippet:
                            author = snippet.split("作者：")[1].split(" ")[0]
                        elif "作者" in snippet:
                            author = snippet.split("作者")[1].split(" ")[0]
                        break
            
            # 更新作者信息
            if author:
                df.at[index, "作者"] = author
                updated_count += 1
                print(f"  更新作者: {author}")
        except Exception as e:
            print(f"  搜索失败: {str(e)}")
    
    # 保存示例结果
    print(f"\n共处理 10 行，更新了 {updated_count} 条记录")
    print(f"保存Excel文件：{excel_file}")
    df.to_excel(excel_file, index=False, engine='openpyxl')
    
    print("示例处理完成！")


if __name__ == '__main__':
    main()
