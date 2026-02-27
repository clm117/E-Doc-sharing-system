#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Excel格式的所有程序模块实现的功能清单
"""

import os
import re
import pandas as pd

def extract_file_info(file_path):
    """
    提取单个Python文件的功能描述
    
    Args:
        file_path: Python文件路径
    
    Returns:
        dict: 包含文件名、功能描述等信息的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取文件名
        file_name = os.path.basename(file_path)
        
        # 提取文件顶部的注释作为功能描述
        # 查找三重引号或#开头的注释
        description = ""
        
        # 查找三重引号注释
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL) or re.search(r"'''*(.*?)*'''", content, re.DOTALL)
        if docstring_match:
            description = docstring_match.group(1).strip()
        else:
            # 查找#开头的注释行
            lines = content.split('\n')
            comment_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    comment_lines.append(stripped[1:].strip())
                elif not stripped:  # 跳过空行
                    continue
                else:
                    break  # 遇到非注释行停止
            description = ' '.join(comment_lines)
        
        # 提取主要功能模块
        # 根据文件名和内容判断模块类型
        module_type = ""
        if file_name == 'app.py':
            module_type = '主程序'
        elif 'encrypt' in file_name:
            module_type = '加密相关'
        elif 'generate' in file_name:
            module_type = '生成工具'
        elif 'test' in file_name.lower():
            module_type = '测试脚本'
        elif 'check' in file_name:
            module_type = '检查工具'
        elif 'create' in file_name:
            module_type = '创建工具'
        elif 'import' in file_name or 'execute' in file_name or 'update' in file_name:
            module_type = '数据处理'
        else:
            module_type = '其他'
        
        # 提取文件大小
        file_size = os.path.getsize(file_path)
        
        # 提取最后修改时间
        last_modified = os.path.getmtime(file_path)
        last_modified_str = pd.to_datetime(last_modified, unit='s').strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            '文件名': file_name,
            '模块类型': module_type,
            '功能描述': description,
            '文件大小(字节)': file_size,
            '最后修改时间': last_modified_str
        }
    except Exception as e:
        print(f"处理文件{file_path}失败: {str(e)}")
        return {
            '文件名': os.path.basename(file_path),
            '模块类型': '未知',
            '功能描述': f'读取失败: {str(e)}',
            '文件大小(字节)': 0,
            '最后修改时间': ''
        }

def main():
    """
    主函数
    """
    # 获取当前目录下的所有Python文件
    current_dir = os.getcwd()
    python_files = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith('.py')]
    
    # 提取每个文件的信息
    module_list = []
    for file_path in python_files:
        file_info = extract_file_info(file_path)
        module_list.append(file_info)
    
    # 创建DataFrame
    df = pd.DataFrame(module_list)
    
    # 按模块类型排序
    df = df.sort_values('模块类型')
    
    # 重置索引
    df = df.reset_index(drop=True)
    
    # 添加序号列
    df.insert(0, '序号', range(1, len(df) + 1))
    
    # 保存到Excel文件
    output_file = os.path.join(current_dir, '程序模块功能清单.xlsx')
    df.to_excel(output_file, index=False)
    
    print(f"程序模块功能清单已生成: {output_file}")
    print(f"共包含{len(df)}个Python模块")
    
    # 打印模块类型统计
    print("\n模块类型统计:")
    type_counts = df['模块类型'].value_counts()
    for module_type, count in type_counts.items():
        print(f"{module_type}: {count}个")

if __name__ == '__main__':
    main()