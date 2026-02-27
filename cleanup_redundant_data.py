#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理file_info表中冗余数据：删除不存在对应PDF文件的记录
"""

import os
import cx_Oracle


def cleanup_redundant_data():
    """
    连接Oracle数据库，清理file_info表中冗余数据
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    # 指定PDF文件目录
    pdf_dir = r"D:\Program Files (x86)\Trae CN\111code\加密文件"
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询file_info表中的所有记录
        query = "SELECT FILE_NAME, FILE_ID FROM file_info"
        cursor.execute(query)
        
        # 获取所有结果
        all_records = cursor.fetchall()
        print(f"成功从数据库获取{len(all_records)}个文件记录")
        
        deleted_count = 0
        
        # 遍历每个记录，检查文件是否存在
        for file_name, record_id in all_records:
            # 构建PDF文件路径
            pdf_path = os.path.join(pdf_dir, file_name)
            
            # 检查文件是否存在
            if not os.path.exists(pdf_path):
                # 文件不存在，删除该记录
                delete_query = "DELETE FROM file_info WHERE FILE_ID = :file_id"
                cursor.execute(delete_query, file_id=record_id)
                deleted_count += 1
                print(f"删除冗余记录：{file_name} (ID: {record_id})")
        
        # 提交事务
        connection.commit()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print(f"\n清理完成！共删除{deleted_count}条冗余记录")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    cleanup_redundant_data()
