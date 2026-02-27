#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将指定目录下的PDF文件和说明文件逐一加密压缩
"""

import os
import zipfile
import cx_Oracle


def get_file_passwords():
    """
    连接Oracle数据库，获取file_info表中的file_name和file_password映射关系
    
    Returns:
        dict: 文件名为键，密码为值的字典
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    passwords = {}
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询file_info表
        query = "SELECT file_name, file_password FROM file_info"
        cursor.execute(query)
        
        # 获取所有结果
        for file_name, file_password in cursor.fetchall():
            passwords[file_name] = file_password
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"成功从数据库获取{len(passwords)}个文件的密码")
        return passwords
        
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        return {}


def encrypt_file(file_path, password, output_path):
    """
    对单个文件进行加密压缩
    
    Args:
        file_path: 要压缩的文件路径
        password: 压缩密码
        output_path: 输出压缩包路径
    """
    try:
        # 创建压缩文件
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加文件到压缩包，设置密码
            zipf.write(file_path, os.path.basename(file_path))
            # 设置密码
            zipf.setpassword(password.encode('utf-8'))
        
        print(f"成功压缩文件: {file_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"压缩文件失败 {file_path}: {str(e)}")
        return False


def main():
    """
    主函数
    """
    # 获取文件密码映射
    file_passwords = get_file_passwords()
    
    if not file_passwords:
        print("未获取到文件密码，无法进行压缩")
        return
    
    # 指定目录
    target_dir = r"D:\Program Files (x86)\Trae CN\111code\加密文件"
    
    # 检查目录是否存在
    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        return
    
    # 获取目录下的所有文件
    files = os.listdir(target_dir)
    
    # 遍历文件，处理PDF文件和说明文件
    for file_name in files:
        file_path = os.path.join(target_dir, file_name)
        
        # 跳过子目录
        if os.path.isdir(file_path):
            continue
        
        # 处理PDF文件
        if file_name.lower().endswith('.pdf'):
            # 找到对应的密码
            password = file_passwords.get(file_name, None)
            if password:
                # 构建输出路径
                output_path = os.path.join(target_dir, f"{os.path.splitext(file_name)[0]}.zip")
                # 加密压缩
                encrypt_file(file_path, password, output_path)
            else:
                print(f"未找到文件{file_name}的密码")
        
        # 处理说明文件
        elif file_name == "密码链接说明.txt":
            # 找到对应的密码（使用第一个文件的密码，或者指定一个默认密码）
            # 这里假设说明文件使用第一个PDF文件的密码
            if file_passwords:
                # 获取第一个文件的密码
                password = next(iter(file_passwords.values()))
                # 构建输出路径
                output_path = os.path.join(target_dir, "密码链接说明.zip")
                # 加密压缩
                encrypt_file(file_path, password, output_path)
            else:
                print("未找到任何文件密码，无法压缩说明文件")


if __name__ == '__main__':
    main()
