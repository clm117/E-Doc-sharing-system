#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
当file_info.file_name=alipay_wap_pay_records.file_name时，取file_info.file_id数据更新alipay_wap_pay_records中的file_id
"""

import cx_Oracle


def update_alipay_file_id():
    """
    当file_info.file_name=alipay_wap_pay_records.file_name时，取file_info.file_id数据更新alipay_wap_pay_records中的file_id
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**db_config)
        cursor = connection.cursor()
        
        print("=== 开始更新alipay_wap_pay_records表的file_id字段 ===")
        
        # 更新SQL语句：通过file_name匹配，将file_info.file_id更新到alipay_wap_pay_records.file_id
        update_sql = """
        UPDATE alipay_wap_pay_records a
        SET a.file_id = (
            SELECT f.file_id
            FROM file_info f
            WHERE f.file_name = a.file_name
        )
        WHERE EXISTS (
            SELECT 1
            FROM file_info f
            WHERE f.file_name = a.file_name
        )
        """
        
        # 执行更新
        cursor.execute(update_sql)
        updated_count = cursor.rowcount
        
        # 提交事务
        connection.commit()
        
        print(f"成功更新了 {updated_count} 条记录的file_id字段")
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        print("=== 更新完成 ===")
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    update_alipay_file_id()