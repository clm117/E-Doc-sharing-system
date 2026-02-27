-- 为alipay_wap_pay_records表插入2247条测试数据
-- file_encrypt_password字段使用随机6位数字

-- 设置当前会话时间格式
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

-- 声明变量和开始PL/SQL块
DECLARE
    v_count NUMBER := 0;  -- 计数器
    v_batch_size NUMBER := 100;  -- 每100条提交一次
    v_total_records NUMBER := 2247;  -- 总记录数
    v_file_encrypt_password VARCHAR2(6);  -- 随机6位数字密码
BEGIN
    -- 循环插入数据
    FOR i IN 1..v_total_records LOOP
        -- 生成随机6位数字密码
        v_file_encrypt_password := TO_CHAR(TRUNC(DBMS_RANDOM.VALUE(100000, 999999)));
        
        -- 插入数据
        INSERT INTO alipay_wap_pay_records (
            trade_no, out_trade_no, app_id, total_amount, seller_id, 
            buyer_id, buyer_logon_id, trade_status, gmt_create, 
            subject, body, charset, version, sign_type, sign, 
            file_name, mobile_pay_url, dynamic_amount, qr_code_url, 
            file_encrypt_password
        ) VALUES (
            '20260112220011045605' || LPAD(i, 6, '0'), -- trade_no
            'TEST20260112' || LPAD(i, 4, '0'), -- out_trade_no
            '2021000112345678', -- app_id
            3.00 + (i * 0.5), -- total_amount
            '2088123456789012', -- seller_id
            '2088123456789' || LPAD(i, 3, '0'), -- buyer_id
            'test' || i || '@example.com', -- buyer_logon_id
            CASE WHEN MOD(i, 2) = 0 THEN 'WAIT_BUYER_PAY' ELSE 'TRADE_SUCCESS' END, -- trade_status
            SYSDATE, -- gmt_create
            '测试商品' || i, -- subject
            '这是第' || i || '个测试商品的描述', -- body
            'UTF-8', -- charset
            '1.0', -- version
            'RSA2', -- sign_type
            'test_sign' || i, -- sign
            'file' || i || '.pdf', -- file_name
            'http://192.168.100.174:5000/mobile_payment_simple', -- mobile_pay_url
            3.00 + (i * 0.5), -- dynamic_amount
            'http://192.168.100.174:5000/mobile_payment_simple', -- qr_code_url
            v_file_encrypt_password -- 随机6位数字密码
        );
        
        v_count := v_count + 1;
        
        -- 每100条提交一次
        IF MOD(v_count, v_batch_size) = 0 THEN
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('已插入 ' || v_count || ' 条记录');
        END IF;
    END LOOP;
    
    -- 提交剩余的记录
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('已插入所有记录，共 ' || v_count || ' 条');
    
    -- 验证插入结果
    DECLARE
        v_result_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_result_count FROM alipay_wap_pay_records;
        DBMS_OUTPUT.PUT_LINE('表中实际记录数: ' || v_result_count);
        IF v_result_count = v_total_records THEN
            DBMS_OUTPUT.PUT_LINE('测试数据插入成功！');
        ELSE
            DBMS_OUTPUT.PUT_LINE('插入失败：预期插入 ' || v_total_records || ' 条，实际插入 ' || v_result_count || ' 条');
        END IF;
    END;
EXCEPTION
    WHEN OTHERS THEN
        -- 异常处理
        DBMS_OUTPUT.PUT_LINE('插入过程中发生错误: ' || SQLERRM);
        ROLLBACK;
END;
/

-- 查询插入结果的基本统计
SELECT 
    COUNT(*) AS total_records,
    MIN(file_encrypt_password) AS min_password,
    MAX(file_encrypt_password) AS max_password
FROM alipay_wap_pay_records;
