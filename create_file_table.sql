-- 创建电子文件销售系统的文件信息表
-- 包含文件名、密码、唯一标识、文件分类和下载次数等字段

-- 创建表
CREATE TABLE file_info (
    -- 18位不重复唯一标识，不为空
    file_id           VARCHAR2(18) NOT NULL,
    
    -- 文件名，600位字符，不为空
    file_name         VARCHAR2(600) NOT NULL,
    
    -- 密码，随机6位数字，不为空
    file_password     VARCHAR2(6) NOT NULL,
    
    -- 文件大类，可选值：科技、心理、医学、法律、数学、英语、历史、会计
    file_major_class  VARCHAR2(20) NOT NULL,
    
    -- 文件中类，可选值：C语言、python、java、前端、数据库
    file_mid_class    VARCHAR2(20) NOT NULL,
    
    -- 文件小类，可选值：爬虫、大数据、人工智能
    file_minor_class  VARCHAR2(20) NOT NULL,
    
    -- 下载次数
    download_count    NUMBER(10) DEFAULT 0 NOT NULL,
    
    -- 记录创建时间
    create_time       DATE DEFAULT SYSDATE NOT NULL,
    
    -- 记录更新时间
    update_time       DATE DEFAULT SYSDATE NOT NULL,
    
    -- 设置主键约束
    CONSTRAINT pk_file_info PRIMARY KEY (file_id),
    
    -- 设置唯一约束，文件名唯一
    CONSTRAINT uk_file_info_file_name UNIQUE (file_name),
    
    -- 文件大类检查约束
    CONSTRAINT ck_file_major_class CHECK (file_major_class IN ('科技', '心理', '医学', '法律', '数学', '英语', '历史', '会计')),
    
    -- 文件中类检查约束
    CONSTRAINT ck_file_mid_class CHECK (file_mid_class IN ('C语言', 'python', 'java', '前端', '数据库')),
    
    -- 文件小类检查约束
    CONSTRAINT ck_file_minor_class CHECK (file_minor_class IN ('爬虫', '大数据', '人工智能')),
    
    -- 密码检查约束：必须是6位数字
    CONSTRAINT ck_file_password CHECK (REGEXP_LIKE(file_password, '^[0-9]{6}$'))
);

-- 创建序列，用于生成18位唯一标识
CREATE SEQUENCE seq_file_id
    START WITH 1          -- 起始值
    INCREMENT BY 1        -- 步长为1
    NOMAXVALUE           -- 无最大值
    NOCYCLE              -- 不循环
    NOCACHE;             -- 不缓存

-- 创建触发器，用于生成18位唯一标识
CREATE OR REPLACE TRIGGER trg_file_id
BEFORE INSERT ON file_info
FOR EACH ROW
BEGIN
    -- 当file_id为NULL时，生成18位唯一标识
    -- 格式：20260112 + 0000000001（日期 + 9位序列）
    IF :NEW.file_id IS NULL THEN
        :NEW.file_id := TO_CHAR(SYSDATE, 'YYYYMMDD') || LPAD(seq_file_id.NEXTVAL, 9, '0');
    END IF;
    
    -- 更新记录更新时间
    :NEW.update_time := SYSDATE;
END;
/

-- 创建索引，提高查询性能
CREATE INDEX idx_file_major_class ON file_info(file_major_class);
CREATE INDEX idx_file_mid_class ON file_info(file_mid_class);
CREATE INDEX idx_file_minor_class ON file_info(file_minor_class);
CREATE INDEX idx_download_count ON file_info(download_count);

-- 提交事务
COMMIT;

-- 输出创建成功信息
SELECT '文件信息表file_info创建成功' AS message FROM DUAL;
