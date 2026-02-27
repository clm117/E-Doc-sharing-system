-- 1. 在payment_config表中插入新的价格配置
INSERT INTO payment_config (
    PRICE_ID, PRICE_TYPE, AMOUNT, PAYMENT_URL, DESCRIPTION, STATUS, CREATE_TIME, UPDATE_TIME
) VALUES (
    2, '2', 5.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买 高级配置', 'Y', SYSDATE, SYSDATE
);

-- 2. 在file_info表中添加新字段FILE_PRICE_TYPE
ALTER TABLE file_info ADD (FILE_PRICE_TYPE CHAR(1) DEFAULT '1' NOT NULL);

-- 3. 更新现有file_info记录，设置不同的FILE_PRICE_TYPE值
-- 例如，将前5条记录中的第2条和第4条设置为价格类型2
UPDATE file_info SET FILE_PRICE_TYPE = '2' WHERE FILE_ID IN ('20260112000000002', '20260112000000004');

-- 4. 提交事务
COMMIT;

-- 5. 验证修改结果
SELECT * FROM payment_config;
SELECT FILE_ID, FILE_NAME, FILE_PRICE_TYPE FROM file_info WHERE rownum <= 5;
