-- SQLite建表脚本
-- 1. 文件信息表
CREATE TABLE IF NOT EXISTS file_info (
    file_id TEXT NOT NULL PRIMARY KEY,
    file_name TEXT NOT NULL UNIQUE,
    file_password TEXT NOT NULL,
    file_major_class TEXT NOT NULL,
    file_mid_class TEXT NOT NULL,
    file_minor_class TEXT NOT NULL,
    download_count INTEGER DEFAULT 0 NOT NULL,
    create_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_file_major_class ON file_info(file_major_class);
CREATE INDEX IF NOT EXISTS idx_file_mid_class ON file_info(file_mid_class);
CREATE INDEX IF NOT EXISTS idx_file_minor_class ON file_info(file_minor_class);
CREATE INDEX IF NOT EXISTS idx_download_count ON file_info(download_count);

-- 2. 支付宝WAP支付记录表
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

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_alipay_trade_no ON alipay_wap_pay_records(trade_no);
CREATE INDEX IF NOT EXISTS idx_alipay_out_trade_no ON alipay_wap_pay_records(out_trade_no);

-- 3. 支付配置表
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

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_payment_config_status ON payment_config(status);

-- 初始化支付配置数据
INSERT OR IGNORE INTO payment_config (price_type, amount, payment_url, description, status)
VALUES ('1', 3.00, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买默认支付配置', 'Y');

-- 4. 支付宝WAP支付记录表（oracle_create_table.sql版本）
CREATE TABLE IF NOT EXISTS alipay_wap_pay_records_extended (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_no TEXT NOT NULL,
    out_trade_no TEXT NOT NULL,
    app_id TEXT NOT NULL,
    total_amount REAL NOT NULL,
    seller_id TEXT NOT NULL,
    seller_email TEXT,
    buyer_id TEXT NOT NULL,
    buyer_logon_id TEXT NOT NULL,
    trade_status TEXT NOT NULL,
    gmt_create TEXT NOT NULL,
    gmt_payment TEXT,
    gmt_refund TEXT,
    gmt_close TEXT,
    subject TEXT NOT NULL,
    body TEXT,
    charset TEXT NOT NULL,
    version TEXT NOT NULL,
    sign_type TEXT NOT NULL,
    sign TEXT NOT NULL,
    auth_app_id TEXT,
    point_amount REAL,
    invoice_amount REAL,
    fund_bill_list TEXT,
    passback_params TEXT,
    file_name TEXT,
    mobile_pay_url TEXT NOT NULL,
    dynamic_amount REAL NOT NULL,
    qr_code_url TEXT NOT NULL,
    create_time TEXT DEFAULT CURRENT_TIMESTAMP,
    update_time TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_alipay_extended_trade_status ON alipay_wap_pay_records_extended(trade_status);
CREATE INDEX IF NOT EXISTS idx_alipay_extended_out_trade_no ON alipay_wap_pay_records_extended(out_trade_no);
CREATE INDEX IF NOT EXISTS idx_alipay_extended_gmt_create ON alipay_wap_pay_records_extended(gmt_create);
CREATE INDEX IF NOT EXISTS idx_alipay_extended_total_amount ON alipay_wap_pay_records_extended(total_amount);

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- 启用WAL模式提高性能
PRAGMA journal_mode = WAL;