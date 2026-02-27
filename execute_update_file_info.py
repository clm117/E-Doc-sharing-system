#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行SQL脚本，更新file_info表结构
"""

import cx_Oracle

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def execute_sql_script():
    """
    执行SQL脚本，更新file_info表结构
    """
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 直接执行ALTER TABLE语句，避免文件读取和语句分割问题
        print("开始执行ALTER TABLE语句...")
        
        alter_sql = """
        ALTER TABLE file_info ADD (
            FILE_AUTHOR VARCHAR2(100) DEFAULT NULL,
            STANDARD_NAME VARCHAR2(200) DEFAULT NULL,
            SEARCH_KEYWORDS VARCHAR2(200) DEFAULT NULL,
            FILE_TAGS VARCHAR2(300) DEFAULT NULL,
            FILE_ISBN VARCHAR2(20) DEFAULT NULL,
            REMARK1 VARCHAR2(200) DEFAULT NULL,
            REMARK2 VARCHAR2(200) DEFAULT NULL,
            REMARK3 VARCHAR2(200) DEFAULT NULL
        )
        """
        
        print(f"执行ALTER TABLE语句")
        cursor.execute(alter_sql)
        
        # 提交事务
        connection.commit()
        
        print("\nSQL语句执行完成！")
        print("file_info表已成功添加新字段。")
        
        # 查看表结构，验证修改
        print("\n表结构验证：")
        cursor.execute("SELECT column_name, data_type, nullable FROM user_tab_columns WHERE table_name = 'FILE_INFO' ORDER BY column_id")
        columns = cursor.fetchall()
        for col in columns:
            print(f"{col[0]:<25} {col[1]:<20} 允许为空: {'是' if col[2] == 'Y' else '否'}")
        
        # 特别检查我们添加的新字段是否存在
        new_fields = ['FILE_AUTHOR', 'STANDARD_NAME', 'SEARCH_KEYWORDS', 'FILE_TAGS', 'FILE_ISBN', 'REMARK1', 'REMARK2', 'REMARK3']
        print("\n检查新添加的字段：")
        existing_columns = [col[0] for col in columns]
        for field in new_fields:
            if field in existing_columns:
                print(f"✓ {field}: 已成功添加")
            else:
                print(f"✗ {field}: 未添加")
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        # 发生异常时回滚事务
        if 'connection' in locals():
            connection.rollback()


if __name__ == '__main__':
    execute_sql_script()
