#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新file_info表中的file_author、file_name和file_isbn字段
"""

import os
import cx_Oracle
import re


def update_file_info_fields():
    """
    更新file_info表中的file_author、file_name和file_isbn字段
    """
    # Oracle数据库连接配置
    db_config = {
        'user': 'system',
        'password': 'oracle123',
        'dsn': 'localhost:1521/ORCLM',
        'encoding': 'UTF-8'
    }
    
    # PDF文件目录
    pdf_dir = r"D:\2.enjoy\2.学习资料\【16