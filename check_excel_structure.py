#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查示例Excel文件的结构
"""

import pandas as pd
import os

# 读取Excel文件
excel_file_path = r"sample_files.xlsx"
df = pd.read_excel(excel_file_path)

# 显示文件结构
print(f"Excel文件路径: {excel_file_path}")
print(f"表名列表: {pd.ExcelFile(excel_file_path).sheet_names}")
print(f"\n数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"\n数据预览:")
print(df.head())
print(f"\n数据信息:")
df.info()
