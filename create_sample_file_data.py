#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例Excel文件，包含B列的文件名数据
"""

import pandas as pd
import os

# 生成示例文件名数据
file_names = [f'文件{i}.pdf' for i in range(1, 101)]  # 生成100个示例文件名

# 创建DataFrame，只包含B列
# 使用空的A列，这样B列才会是第二列
sample_data = {
    '': [''] * len(file_names),  # 空的A列
    'B': file_names  # B列包含文件名
}

# 创建DataFrame
df = pd.DataFrame(sample_data)

# 保存为Excel文件
excel_file_path = os.path.join(os.getcwd(), 'sample_file_data.xlsx')
df.to_excel(excel_file_path, index=False, header=False)  # 不包含索引和表头

print(f"示例Excel文件已创建: {excel_file_path}")
print(f"文件包含{len(file_names)}个文件名，位于B列")
