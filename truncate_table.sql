-- 清空alipay_wap_pay_records表的所有记录

-- 1. 首先查询表中的当前记录数，确认表中有数据
SELECT COUNT(*) AS current_record_count
FROM alipay_wap_pay_records;

-- 2. 使用TRUNCATE TABLE语句清空表（高效，不记录日志）
-- 注意：TRUNCATE TABLE将直接删除所有记录，无法回滚
TRUNCATE TABLE alipay_wap_pay_records;

-- 3. 提交事务（TRUNCATE是DDL语句，会自动提交）
COMMIT;

-- 4. 验证表已清空
SELECT COUNT(*) AS after_truncate_count
FROM alipay_wap_pay_records;

-- 5. 输出成功信息
SELECT 'alipay_wap_pay_records表已成功清空' AS message FROM DUAL;
