#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版：从Excel文件B列读取文件名，只导入必要字段到file_info表
其他字段暂为空
"""

import pandas as pd
import cx_Oracle
import random
import datetime
import os

# 数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# Excel文件路径 - 使用生成的示例文件
EXCEL_FILE_PATH = r"sample_file_data.xlsx"

# 生成随机6位数字密码
def generate_6digit_password():
    """生成6位随机数字密码"""
    return ''.join(random.choice('0123456789') for _ in range(6))

# 生成18位唯一标识
def generate_file_id(seq):
    """生成18位唯一标识：日期+9位序列"""
    date_part = datetime.datetime.now().strftime('%Y%m%d')
    seq_part = f'{seq:09d}'
    return date_part + seq_part

# 主函数
def main():
    print("开始导入Excel数据到file_info表...")
    
    try:
        # 1. 读取Excel文件
        print(f"正在读取Excel文件: {EXCEL_FILE_PATH}")
        # 读取B列数据
        df = pd.read_excel(EXCEL_FILE_PATH, usecols='B')
        
        # 去除空值
        df = df.dropna()
        
        # 获取B列数据列表
        file_names = df.iloc[:, 0].tolist()
        
        print(f"成功读取B列数据，共{len(file_names)}条记录")
        
        # 2. 连接Oracle数据库
        print("正在连接Oracle数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 3. 插入数据到数据库
        print("正在插入数据到file_info表...")
        
        # 插入记录的SQL语句 - 只插入必要字段
        insert_sql = """
        INSERT INTO file_info (
            file_id, file_name, file_password
        ) VALUES (
            :file_id, :file_name, :file_password
        )
        """
        
        # 准备数据并插入
        batch_size = 100  # 每100条提交一次
        inserted_count = 0
        skipped_count = 0
        
        # 用于跟踪已插入的文件名
        inserted_file_names = set()
        
        for i, file_name in enumerate(file_names, 1):
            # 检查文件名是否已存在
            if file_name in inserted_file_names:
                skipped_count += 1
                print(f"跳过重复文件名: {file_name}")
                continue
            
            # 生成18位唯一标识
            file_id = generate_file_id(i)
            
            # 生成随机6位密码
            file_password = generate_6digit_password()
            
            # 准备插入的数据 - 只包含必要字段
            data = {
                'file_id': file_id,
                'file_name': file_name,
                'file_password': file_password
            }
            
            try:
                # 执行插入
                cursor.execute(insert_sql, data)
                inserted_count += 1
                inserted_file_names.add(file_name)
                
                # 每100条记录提交一次
                if inserted_count % batch_size == 0:
                    connection.commit()
                    print(f"已插入{inserted_count}条记录")
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                if error.code == 1:  # ORA-00001: 违反唯一约束条件
                    skipped_count += 1
                    print(f"跳过重复文件名(数据库中已存在): {file_name}")
                    continue
                else:
                    raise  # 其他错误重新抛出
        
        # 提交剩余的记录
        connection.commit()
        print(f"数据导入完成，共插入{inserted_count}条记录，跳过{skipped_count}条重复记录")
        
        # 4. 查询插入的数据数量，验证导入结果
        cursor.execute("SELECT COUNT(*) FROM file_info")
        total_count = cursor.fetchone()[0]
        print(f"file_info表中共有{total_count}条记录")
        
        # 5. 显示前5条记录，验证数据结构
        print("\n前5条记录示例：")
        cursor.execute("SELECT file_id, file_name, file_password, file_major_class, file_mid_class, file_minor_class FROM file_info WHERE ROWNUM <= 5")
        columns = [col[0] for col in cursor.description]
        print("|" + "|" .join(f"{col:<20}" for col in columns) + "|")
        print("|" + "|" .join("-"*20 for _ in columns) + "|")
        for row in cursor.fetchall():
            print("|" + "|" .join(f"{str(val):<20}" for val in row) + "|")
        
    except Exception as e:
        print(f"导入过程中发生错误: {str(e)}")
        # 回滚事务
        if 'connection' in locals():
            connection.rollback()
    finally:
        # 关闭数据库连接
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
    print("\n数据导入任务结束")

if __name__ == "__main__":
    main()
