-- 为alipay_wap_pay_records表添加file_id字段
-- 用于关联file_info表的file_id

-- 添加file_id字段
ALTER TABLE alipay_wap_pay_records ADD file_id VARCHAR2(18);

-- 添加外键约束，关联file_info表
ALTER TABLE alipay_wap_pay_records ADD CONSTRAINT fk_alipay_wap_pay_file_id 
FOREIGN KEY (file_id) REFERENCES file_info(file_id) ON DELETE CASCADE;

-- 添加索引，提高查询效率
CREATE INDEX idx_alipay_file_id ON alipay_wap_pay_records(file_id);

-- 提交事务
COMMIT;

-- 输出成功信息
SELECT '成功添加file_id字段到alipay_wap_pay_records表' AS message FROM DUAL;
