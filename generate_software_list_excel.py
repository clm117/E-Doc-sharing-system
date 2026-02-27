#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Excel格式的软件及版本清单，包括Python库清单
"""

import os
import sys
import subprocess
import pandas as pd

def get_system_info():
    """获取系统信息"""
    return {
        "项目名称": "学习资料支付系统",
        "操作系统": os.name,
        "Python版本": sys.version.split()[0],
        "Python路径": sys.executable
    }

def get_installed_python_packages():
    """获取已安装的Python包及其版本"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, encoding='utf-8')
        packages = []
        for line in result.stdout.split('\n')[2:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append((parts[0], parts[1]))
        return packages
    except Exception as e:
        print(f"获取已安装包失败: {str(e)}")
        return []

def get_used_python_packages():
    """获取当前项目中使用到的Python包"""
    # 根据项目代码分析使用到的Python包
    used_packages = {
        'Flask': '',
        'qrcode': '',
        'cx_Oracle': '',
        'PyPDF2': '',
        'pandas': '',
        'openpyxl': '',
        'zipfile': '',  # 标准库
        'os': '',       # 标准库
        'sys': ''       # 标准库
    }
    
    # 获取已安装包列表
    installed_packages = get_installed_python_packages()
    installed_dict = dict(installed_packages)
    
    # 填充已安装包的版本
    package_list = []
    for package in used_packages:
        if package in installed_dict:
            package_list.append({
                '库名称': package,
                '版本': installed_dict[package],
                '类型': '第三方库'
            })
        else:
            package_list.append({
                '库名称': package,
                '版本': '标准库',
                '类型': '标准库'
            })
    
    return package_list

def main():
    """主函数"""
    # 获取数据
    system_info = get_system_info()
    python_packages = get_used_python_packages()
    
    # 创建Excel writer对象
    output_file = os.path.join(os.getcwd(), '软件及版本清单.xlsx')
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # 1. 系统软件信息
    system_data = {
        '类别': ['项目名称', '操作系统', 'Python版本', 'Python路径'],
        '信息': [system_info['项目名称'], system_info['操作系统'], 
                system_info['Python版本'], system_info['Python路径']]
    }
    df_system = pd.DataFrame(system_data)
    df_system.to_excel(writer, sheet_name='系统软件', index=False)
    
    # 2. 数据库软件信息
    db_data = {
        '类别': ['数据库类型', 'Oracle版本', '连接驱动', '驱动版本'],
        '信息': ['Oracle', '11g/12c (根据配置文件)', 'cx_Oracle', 
                next((pkg['版本'] for pkg in python_packages if pkg['库名称'] == 'cx_Oracle'), '')]
    }
    df_db = pd.DataFrame(db_data)
    df_db.to_excel(writer, sheet_name='数据库软件', index=False)
    
    # 3. Python库清单
    df_packages = pd.DataFrame(python_packages)
    df_packages.to_excel(writer, sheet_name='Python库清单', index=False)
    
    # 4. 其他相关软件
    other_data = {
        '类别': ['文本编辑器/IDE', '浏览器'],
        '信息': ['Trae IDE', '用于访问Flask应用']
    }
    df_other = pd.DataFrame(other_data)
    df_other.to_excel(writer, sheet_name='其他软件', index=False)
    
    # 保存Excel文件
    writer.close()
    
    print(f"Excel格式的软件及版本清单已生成: {output_file}")
    print(f"文件路径: {output_file}")

if __name__ == '__main__':
    main()