#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成实现当前功能运用到的软件及其版本清单，包括Python库清单
"""

import os
import sys
import subprocess

def get_system_info():
    """获取系统信息"""
    return {
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
    for package in used_packages:
        if package in installed_dict:
            used_packages[package] = installed_dict[package]
        else:
            used_packages[package] = "未安装（标准库）"
    
    return used_packages

def main():
    """主函数"""
    print("=" * 60)
    print("实现当前功能运用到的软件及其版本清单")
    print("=" * 60)
    
    # 1. 系统软件信息
    print("\n1. 系统软件信息")
    print("-" * 40)
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")
    
    # 2. 数据库软件信息
    print("\n2. 数据库软件信息")
    print("-" * 40)
    print("Oracle数据库: 11g/12c (根据配置文件)")
    print("Oracle连接驱动: cx_Oracle (版本见Python库清单)")
    
    # 3. 使用到的Python库清单
    print("\n3. 使用到的Python库清单")
    print("-" * 40)
    print("{:<20} {:<15}".format("库名称", "版本"))
    print("-" * 40)
    
    used_packages = get_used_python_packages()
    for package, version in used_packages.items():
        print("{:<20} {:<15}".format(package, version))
    
    # 4. 其他相关软件
    print("\n4. 其他相关软件")
    print("-" * 40)
    print("文本编辑器/IDE: Trae IDE")
    print("浏览器: 用于访问Flask应用")
    
    print("\n" + "=" * 60)
    print("清单生成完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()