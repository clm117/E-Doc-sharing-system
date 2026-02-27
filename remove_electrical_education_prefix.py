#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除file_info表中STANDARD_NAME字段中的"学校电化教学指导丛书："字符
"""

import cx_Oracle


def remove_electrical_education_prefix():
    """
    删除file_info表中STANDARD_NAME字段中的"学校电化教学指导丛书："字符
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
        
        print("=== 开始删除file_info表中STANDARD_NAME字段的'学校电化教学指导丛书：'前缀 ===")
        
        # 更新SQL语句：替换STANDARD_NAME字段中的"学校电化教学指导丛书："为空字符串
        update_sql = """
        UPDATE file_info
        SET STANDARD_NAME = REPLACE(STANDARD_NAME, '学校电化教学指导丛书：', '')
        WHERE STANDARD_NAME LIKE '%学校电化教学指导丛书：%'
        """
        
        # 执行更新
        cursor.execute(update_sql)
        updated_count = cursor.rowcount
        
        # 提交事务
        connection.commit()
        
        print(f"成功更新了 {updated_count} 条记录，删除了'学校电化教学指导丛书：'前缀")
        
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
    remove_electrical_education_prefix()
