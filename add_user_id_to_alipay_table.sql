-- 为alipay_wap_pay_records表添加user_id字段
-- 用于识别不同的用户，避免并发冲突

-- 添加user_id字段
ALTER TABLE alipay_wap_pay_records ADD user_id VARCHAR2(64);

-- 添加字段注释
COMMENT ON COLUMN alipay_wap_pay_records.user_id IS '用户唯一标识，用于区分不同用户';

-- 添加索引，提高查询效率
CREATE INDEX idx_user_id ON alipay_wap_pay_records(user_id);

-- 添加复合索引，优化file_id + user_id查询
CREATE INDEX idx_file_id_user_id ON alipay_wap_pay_records(file_id, user_id);

-- 提交事务
COMMIT;

-- 输出成功信息
SELECT '成功添加user_id字段到alipay_wap_pay_records表' AS message FROM DUAL;

-- 验证字段是否添加成功
SELECT column_name, data_type, nullable
FROM user_tab_columns
WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
AND column_name = 'USER_ID';
