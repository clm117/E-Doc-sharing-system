-- 向alipay_wap_pay_records表添加session_id字段，用于关联支付记录和页面

ALTER TABLE alipay_wap_pay_records 
ADD session_id VARCHAR2(20) NULL;

-- 添加索引，提高查询效率
CREATE INDEX idx_alipay_session_id ON alipay_wap_pay_records(session_id);

-- 提交事务
COMMIT;

-- 输出修改成功信息
SELECT 'alipay_wap_pay_records表已添加session_id字段' AS message FROM DUAL;