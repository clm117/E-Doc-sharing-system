#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Excel格式的环境配置清单
"""

import pandas as pd
import os
import sys

def get_python_version():
    """获取Python版本"""
    return sys.version

def get_installed_packages():
    """获取已安装的Python包"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, encoding='utf-8')
        packages = []
        for line in result.stdout.split('\n')[2:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({'Package': parts[0], 'Version': parts[1]})
        return packages
    except Exception as e:
        print(f"获取已安装包失败: {str(e)}")
        return []

def main():
    """主函数"""
    # 创建Excel writer对象
    output_file = os.path.join(os.getcwd(), '环境配置清单.xlsx')
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # 1. 系统环境信息
    system_env = {
        '项目名称': ['学习资料支付系统'],
        '操作系统': [os.name],
        'Python版本': [get_python_version().split()[0]],
        'Python路径': [sys.executable],
        '当前工作目录': [os.getcwd()]
    }
    df_system = pd.DataFrame(system_env)
    df_system.to_excel(writer, sheet_name='系统环境', index=False)
    
    # 2. 项目文件结构
    project_structure = [
        {'类型': '主程序', '文件路径': 'app.py', '功能描述': 'Flask应用主程序'},
        {'类型': '模板文件', '文件路径': 'templates/index.html', '功能描述': '首页模板'},
        {'类型': '模板文件', '文件路径': 'templates/payment.html', '功能描述': '支付页面模板'},
        {'类型': '模板文件', '文件路径': 'templates/payment_success.html', '功能描述': '支付成功页面模板'},
        {'类型': '模板文件', '文件路径': 'templates/mobile_payment.html', '功能描述': '手机支付页面模板'},
        {'类型': '模板文件', '文件路径': 'templates/mobile_payment_simple.html', '功能描述': '简洁版手机支付页面模板'},
        {'类型': '工具脚本', '文件路径': 'encrypt_pdf_and_compress.py', '功能描述': 'PDF加密和压缩脚本'},
        {'类型': '工具脚本', '文件路径': 'markdown_to_word.py', '功能描述': 'Markdown转Word脚本'},
        {'类型': '文档', '文件路径': '数据库说明书.md', '功能描述': '数据库设计说明书'},
        {'类型': '文档', '文件路径': '详细设计说明书.md', '功能描述': '系统详细设计说明书'}
    ]
    df_structure = pd.DataFrame(project_structure)
    df_structure.to_excel(writer, sheet_name='项目文件结构', index=False)
    
    # 3. 数据库配置
    db_config = {
        '数据库类型': ['Oracle'],
        '用户名': ['system'],
        '密码': ['oracle123'],
        'DSN': ['localhost:1521/ORCLM'],
        '编码': ['UTF-8']
    }
    df_db = pd.DataFrame(db_config)
    df_db.to_excel(writer, sheet_name='数据库配置', index=False)
    
    # 4. 已安装Python包
    packages = get_installed_packages()
    df_packages = pd.DataFrame(packages)
    df_packages.to_excel(writer, sheet_name='已安装Python包', index=False)
    
    # 5. 功能模块清单
    features = [
        {'功能模块': '支付流程', '实现文件': 'app.py', '描述': '处理支付初始化、状态检查等'}, 
        {'功能模块': '二维码生成', '实现文件': 'app.py', '描述': '生成包含支付链接的二维码'},
        {'功能模块': 'PDF加密', '实现文件': 'encrypt_pdf_and_compress.py', '描述': '使用PyPDF2加密PDF文件'},
        {'功能模块': '文件压缩', '实现文件': 'encrypt_pdf_and_compress.py', '描述': '生成加密压缩包'},
        {'功能模块': '文档转换', '实现文件': 'markdown_to_word.py', '描述': '将Markdown转换为Word文档'}
    ]
    df_features = pd.DataFrame(features)
    df_features.to_excel(writer, sheet_name='功能模块清单', index=False)
    
    # 保存Excel文件
    writer.close()
    
    print(f"环境配置清单已生成: {output_file}")

if __name__ == '__main__':
    main()