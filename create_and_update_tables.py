#!/usr/bin/env python3
# 创建并更新SQLite表结构

import sqlite3

# SQLite数据库路径
DB_PATH = 'docshare.db'

# 创建表结构
def create_tables():
    print("创建表结构...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建file_info表
    create_file_info_table = """
    CREATE TABLE IF NOT EXISTS file_info (
        file_id TEXT NOT NULL PRIMARY KEY,
        file_name TEXT NOT NULL UNIQUE,
        file_password TEXT NOT NULL,
        file_major_class TEXT NOT NULL,
        file_mid_class TEXT NOT NULL,
        file_minor_class TEXT NOT NULL,
        download_count INTEGER DEFAULT 0 NOT NULL,
        create_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        -- 以下是从Oracle迁移的额外字段
        file_author TEXT DEFAULT NULL,
        standard_name TEXT DEFAULT NULL,
        search_keywords TEXT DEFAULT NULL,
        file_tags TEXT DEFAULT NULL,
        file_isbn TEXT DEFAULT NULL,
        file_price_type TEXT DEFAULT '1',
        file_path TEXT DEFAULT NULL,
        remark1 TEXT DEFAULT NULL,
        remark2 TEXT DEFAULT NULL,
        remark3 TEXT DEFAULT NULL
    );
    """
    
    # 创建alipay_wap_pay_records表
    create_alipay_table = """
    CREATE TABLE IF NOT EXISTS alipay_wap_pay_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        msg TEXT NOT NULL,
        sub_code TEXT,
        sub_msg TEXT,
        trade_no TEXT NOT NULL UNIQUE,
        out_trade_no TEXT NOT NULL UNIQUE,
        buyer_id TEXT NOT NULL,
        buyer_logon_id TEXT NOT NULL,
        seller_id TEXT NOT NULL,
        seller_email TEXT,
        total_amount REAL NOT NULL,
        receipt_amount REAL,
        invoice_amount REAL,
        buyer_pay_amount REAL,
        point_amount REAL,
        refund_fee REAL,
        subject TEXT NOT NULL,
        body TEXT,
        gmt_create TEXT NOT NULL,
        gmt_payment TEXT,
        gmt_refund TEXT,
        gmt_close TEXT,
        file_id TEXT NOT NULL,
        create_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY (file_id) REFERENCES file_info(file_id) ON DELETE CASCADE
    );
    """
    
    # 创建payment_config表
    create_payment_config_table = """
    CREATE TABLE IF NOT EXISTS payment_config (
        config_id INTEGER PRIMARY KEY AUTOINCREMENT,
        price_type TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_url TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Y' NOT NULL,
        create_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
        update_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    """
    
    try:
        # 执行创建表语句
        cursor.execute(create_file_info_table)
        print("file_info表创建成功")
        
        cursor.execute(create_alipay_table)
        print("alipay_wap_pay_records表创建成功")
        
        cursor.execute(create_payment_config_table)
        print("payment_config表创建成功")
        
        # 初始化支付配置数据
        init_payment_config = """
        INSERT OR IGNORE INTO payment_config (price_type, amount, payment_url, description, status)
        VALUES ('1', 3.00, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y');
        """
        cursor.execute(init_payment_config)
        print("支付配置数据初始化成功")
        
        # 创建索引
        create_indexes = [
            "CREATE INDEX IF NOT EXISTS idx_file_major_class ON file_info(file_major_class);",
            "CREATE INDEX IF NOT EXISTS idx_file_mid_class ON file_info(file_mid_class);",
            "CREATE INDEX IF NOT EXISTS idx_file_minor_class ON file_info(file_minor_class);",
            "CREATE INDEX IF NOT EXISTS idx_download_count ON file_info(download_count);",
            "CREATE INDEX IF NOT EXISTS idx_file_author ON file_info(file_author);",
            "CREATE INDEX IF NOT EXISTS idx_file_isbn ON file_info(file_isbn);",
            "CREATE INDEX IF NOT EXISTS idx_file_price_type ON file_info(file_price_type);",
            "CREATE INDEX IF NOT EXISTS idx_standard_name ON file_info(standard_name);",
            "CREATE INDEX IF NOT EXISTS idx_alipay_trade_no ON alipay_wap_pay_records(trade_no);",
            "CREATE INDEX IF NOT EXISTS idx_alipay_out_trade_no ON alipay_wap_pay_records(out_trade_no);",
            "CREATE INDEX IF NOT EXISTS idx_payment_config_status ON payment_config(status);"
        ]
        
        for index_sql in create_indexes:
            cursor.execute(index_sql)
        print("索引创建成功")
        
        # 启用外键约束和WAL模式
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA journal_mode = WAL;")
        
        conn.commit()
        print("表结构创建和更新完成")
        
    except Exception as e:
        print(f"创建表结构时出错: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# 检查表结构
def check_table_structure():
    print("\n检查表结构...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查file_info表结构
        cursor.execute("PRAGMA table_info(file_info);")
        file_info_columns = cursor.fetchall()
        print("file_info表字段:")
        for column in file_info_columns:
            print(f"  {column[1]} ({column[2]})")
        
        # 检查alipay_wap_pay_records表结构
        cursor.execute("PRAGMA table_info(alipay_wap_pay_records);")
        alipay_columns = cursor.fetchall()
        print("\nalipay_wap_pay_records表字段:")
        for column in alipay_columns:
            print(f"  {column[1]} ({column[2]})")
        
        # 检查payment_config表结构
        cursor.execute("PRAGMA table_info(payment_config);")
        payment_columns = cursor.fetchall()
        print("\npayment_config表字段:")
        for column in payment_columns:
            print(f"  {column[1]} ({column[2]})")
        
    except Exception as e:
        print(f"检查表结构时出错: {str(e)}")
    finally:
        conn.close()

# 主函数
def main():
    print("开始创建和更新表结构...")
    create_tables()
    check_table_structure()
    print("\n操作完成！")

if __name__ == '__main__':
    main()
