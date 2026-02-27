#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据标准化文件名搜索作者信息的简单脚本
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
    
    # 显示前10行数据，了解数据格式
    print("\n前10行数据：")
    print(df.head(10))
    
    # 统计需要处理的行数
    need_update = df[(pd.notna(df["标准化文件名"])) & (df["标准化文件名"] != "") & ((pd.isna(df["作者"])) | (df["作者"] == ""))]
    print(f"\n需要更新作者信息的行数：{len(need_update)}")
    
    print("\n完成初步分析！")


if __name__ == '__main__':
    main()
