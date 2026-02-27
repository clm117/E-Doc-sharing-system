#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将指定目录下的PDF文件加密，并与说明文件一起压缩成加密压缩包
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

def encrypt_pdf(file_path, password):
    """
    对PDF文件进行加密
    
    Args:
        file_path: 要加密的PDF文件路径
        password: 加密密码
    
    Returns:
        str: 加密后的PDF文件路径
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        # 创建加密后的PDF文件路径
        encrypted_file_path = os.path.join(os.path.dirname(file_path), f"encrypted_{os.path.basename(file_path)}")
        
        # 打开原始PDF文件
        reader = PdfReader(file_path)
        writer = PdfWriter()
        
        # 将所有页面添加到writer
        for page in reader.pages:
            writer.add_page(page)
        
        # 设置加密
        writer.encrypt(password)
        
        # 保存加密后的PDF文件
        with open(encrypted_file_path, "wb") as out_file:
            writer.write(out_file)
        
        print(f"成功加密PDF文件: {file_path} -> {encrypted_file_path}")
        return encrypted_file_path
    except Exception as e:
        print(f"PDF加密失败 {file_path}: {str(e)}")
        return file_path

def compress_files(file1_path, file2_path, output_path, password):
    """
    将两个文件压缩成一个加密压缩包
    
    Args:
        file1_path: 第一个文件路径
        file2_path: 第二个文件路径
        output_path: 输出压缩包路径
        password: 压缩密码
    """
    try:
        # 创建压缩文件
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加第一个文件到压缩包
            zipf.write(file1_path, os.path.basename(file1_path))
            # 添加第二个文件到压缩包
            zipf.write(file2_path, os.path.basename(file2_path))
            # 设置密码
            zipf.setpassword(password.encode('utf-8'))
        
        print(f"成功压缩文件: {output_path}")
        return True
    except Exception as e:
        print(f"压缩文件失败 {output_path}: {str(e)}")
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
    
    # 检查说明文件是否存在
    info_file = os.path.join(target_dir, "密码链接说明.txt")
    if not os.path.exists(info_file):
        print(f"说明文件不存在: {info_file}")
        return
    
    # 获取目录下的所有PDF文件，过滤掉已加密的
    pdf_files = []
    for file_name in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith('.pdf') and not file_name.startswith('encrypted_'):
            pdf_files.append(file_name)
    
    print(f"找到{len(pdf_files)}个PDF文件需要处理")
    
    # 处理计数
    total_files = len(pdf_files)
    processed_files = 0
    success_files = 0
    failed_files = 0
    
    # 遍历文件，处理PDF文件
    for file_name in pdf_files:
        processed_files += 1
        
        try:
            file_path = os.path.join(target_dir, file_name)
            
            # 找到对应的密码
            password = file_passwords.get(file_name, None)
            if password:
                print(f"[{processed_files}/{total_files}] 处理文件: {file_name}，密码: {password}")
                
                # 加密PDF文件
                encrypted_pdf_path = encrypt_pdf(file_path, password)
                
                # 构建输出路径
                output_path = os.path.join(target_dir, f"{os.path.splitext(file_name)[0]}.zip")
                
                # 压缩文件：将加密后的PDF和说明文件一起压缩
                if compress_files(encrypted_pdf_path, info_file, output_path, password):
                    success_files += 1
                    
                    # 如果生成了临时加密PDF文件，删除它
                    if encrypted_pdf_path != file_path and os.path.exists(encrypted_pdf_path):
                        try:
                            os.remove(encrypted_pdf_path)
                            print(f"删除临时加密PDF文件: {encrypted_pdf_path}")
                        except Exception as e:
                            print(f"删除临时文件失败 {encrypted_pdf_path}: {str(e)}")
                else:
                    failed_files += 1
            else:
                print(f"[{processed_files}/{total_files}] 未找到文件{file_name}的密码")
                failed_files += 1
        except Exception as e:
            print(f"[{processed_files}/{total_files}] 处理文件{file_name}时发生异常: {str(e)}")
            failed_files += 1
            import traceback
            traceback.print_exc()
            # 继续处理下一个文件
            continue
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"成功处理: {success_files}个文件")
    print(f"失败处理: {failed_files}个文件")

if __name__ == '__main__':
    main()