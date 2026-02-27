-- 为alipay_wap_pay_records表添加文件加密密码字段

-- 查看当前表结构，确认没有同名字段
DESCRIBE alipay_wap_pay_records;

-- 添加文件加密密码字段
ALTER TABLE alipay_wap_pay_records
ADD (
    -- 文件加密密码，长度为6位
    file_encrypt_password VARCHAR2(6) NOT NULL
    -- 添加注释
    CONSTRAINT ck_file_encrypt_password CHECK (LENGTH(file_encrypt_password) = 6)
);

-- 添加字段注释
COMMENT ON COLUMN alipay_wap_pay_records.file_encrypt_password IS '文件加密密码，长度为6位';

-- 查看修改后的表结构
DESCRIBE alipay_wap_pay_records;

-- 为现有记录设置默认值（如果需要）
-- UPDATE alipay_wap_pay_records SET file_encrypt_password = '123456';
-- COMMIT;
