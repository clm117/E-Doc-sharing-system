-- 创建支付宝WAP支付记录表
CREATE TABLE alipay_wap_pay_records (
    -- 自增1的数据唯一标识，不能为空
    record_id         NUMBER(18) NOT NULL,
    
    -- 支付宝交易号
    trade_no          VARCHAR2(64) NOT NULL,
    
    -- 商户订单号
    out_trade_no      VARCHAR2(64) NOT NULL,
    
    -- 应用ID
    app_id            VARCHAR2(32) NOT NULL,
    
    -- 交易金额
    total_amount      NUMBER(11,2) NOT NULL,
    
    -- 卖家支付宝用户ID
    seller_id         VARCHAR2(32) NOT NULL,
    
    -- 卖家支付宝账号
    seller_email      VARCHAR2(100),
    
    -- 买家支付宝用户ID
    buyer_id          VARCHAR2(32) NOT NULL,
    
    -- 买家支付宝账号
    buyer_logon_id    VARCHAR2(100) NOT NULL,
    
    -- 交易状态
    trade_status      VARCHAR2(32) NOT NULL,
    
    -- 交易创建时间
    gmt_create        DATE NOT NULL,
    
    -- 交易付款时间
    gmt_payment       DATE,
    
    -- 交易退款时间
    gmt_refund        DATE,
    
    -- 交易结束时间
    gmt_close         DATE,
    
    -- 订单标题
    subject           VARCHAR2(256) NOT NULL,
    
    -- 订单描述
    body              VARCHAR2(4000),
    
    -- 编码格式
    charset           VARCHAR2(16) NOT NULL,
    
    -- 接口版本
    version           VARCHAR2(8) NOT NULL,
    
    -- 签名类型
    sign_type         VARCHAR2(10) NOT NULL,
    
    -- 签名
    sign              VARCHAR2(2048) NOT NULL,
    
    -- 授权方APPID
    auth_app_id       VARCHAR2(32),
    
    -- 积分支付金额
    point_amount      NUMBER(11,2),
    
    -- 开票金额
    invoice_amount    NUMBER(11,2),
    
    -- 支付金额信息（JSON格式）
    fund_bill_list    VARCHAR2(2048),
    
    -- 回传参数
    passback_params   VARCHAR2(512),
    
    -- 长度为600的字符串，用于存储文件名
    file_name         VARCHAR2(600),
    
    -- 手机支付页面URL
    mobile_pay_url    VARCHAR2(1024) NOT NULL,
    
    -- 动态金额（用于生成二维码）
    dynamic_amount    NUMBER(11,2) NOT NULL,
    
    -- 二维码URL，用于生成index.html页面中的二维码，扫描后跳转到mobile_payment_simple.html
    qr_code_url       VARCHAR2(2048) NOT NULL,
    
    -- 记录创建时间
    create_time       DATE DEFAULT SYSDATE,
    
    -- 记录更新时间
    update_time       DATE DEFAULT SYSDATE,
    
    -- 设置主键约束
    CONSTRAINT pk_alipay_wap_pay_records PRIMARY KEY (record_id),
    
    -- 设置唯一约束
    CONSTRAINT uk_alipay_wap_pay_records UNIQUE (trade_no, out_trade_no)
);

-- 为自增字段创建序列
CREATE SEQUENCE seq_alipay_wap_pay_records
    START WITH 1          -- 起始值
    INCREMENT BY 1        -- 步长为1
    NOMAXVALUE           -- 无最大值
    NOCYCLE              -- 不循环
    NOCACHE;             -- 不缓存

-- 创建触发器，实现自增字段
CREATE OR REPLACE TRIGGER trg_alipay_wap_pay_records
BEFORE INSERT ON alipay_wap_pay_records
FOR EACH ROW
BEGIN
    -- 当record_id为NULL时，使用序列生成值
    IF :NEW.record_id IS NULL THEN
        SELECT seq_alipay_wap_pay_records.NEXTVAL INTO :NEW.record_id FROM DUAL;
    END IF;
    
    -- 更新记录创建时间和更新时间
    :NEW.create_time := SYSDATE;
    :NEW.update_time := SYSDATE;
END;
/

-- 创建索引，提高查询性能
CREATE INDEX idx_alipay_wap_pay_trade_status ON alipay_wap_pay_records(trade_status);
CREATE INDEX idx_alipay_wap_pay_out_trade_no ON alipay_wap_pay_records(out_trade_no);
CREATE INDEX idx_alipay_wap_pay_gmt_create ON alipay_wap_pay_records(gmt_create);
CREATE INDEX idx_alipay_wap_pay_total_amount ON alipay_wap_pay_records(total_amount);

-- 提交事务
COMMIT;

-- 输出创建成功信息
SELECT '支付宝WAP支付记录表创建成功' AS message FROM DUAL;
