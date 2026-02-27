-- 为alipay_wap_pay_records表插入10行测试数据

-- 设置当前会话时间格式
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

-- 插入10行测试数据
DECLARE
    v_i NUMBER;
BEGIN
    FOR v_i IN 1..10 LOOP
        INSERT INTO alipay_wap_pay_records (
            trade_no, out_trade_no, app_id, total_amount, seller_id, 
            buyer_id, buyer_logon_id, trade_status, gmt_create, 
            subject, body, charset, version, sign_type, sign, 
            file_name, mobile_pay_url, dynamic_amount, qr_code_url
        ) VALUES (
            '20260109220011045605' || LPAD(v_i, 6, '0'), -- trade_no
            'TEST20260109' || LPAD(v_i, 4, '0'), -- out_trade_no
            '2021000112345678', -- app_id
            3.00 + (v_i * 0.5), -- total_amount
            '2088123456789012', -- seller_id
            '2088123456789' || LPAD(v_i, 3, '0'), -- buyer_id
            'test' || v_i || '@example.com', -- buyer_logon_id
            CASE WHEN MOD(v_i, 2) = 0 THEN 'WAIT_BUYER_PAY' ELSE 'TRADE_SUCCESS' END, -- trade_status
            SYSDATE, -- gmt_create
            '测试商品' || v_i, -- subject
            '这是第' || v_i || '个测试商品的描述', -- body
            'UTF-8', -- charset
            '1.0', -- version
            'RSA2', -- sign_type
            'test_sign' || v_i, -- sign
            'test_file' || v_i || '.txt', -- file_name
            'http://192.168.100.174:5000/mobile_payment_simple', -- mobile_pay_url
            3.00 + (v_i * 0.5), -- dynamic_amount
            'http://192.168.100.174:5000/mobile_payment_simple' -- qr_code_url
        );
    END LOOP;
    
    -- 提交事务
    COMMIT;
    
    -- 输出成功信息
    DBMS_OUTPUT.PUT_LINE('成功插入10行测试数据到alipay_wap_pay_records表');
    
    -- 显示表中数据行数
    DECLARE
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM alipay_wap_pay_records;
        DBMS_OUTPUT.PUT_LINE('alipay_wap_pay_records表中的数据行数: ' || v_count);
    END;
END;
/

-- 查询插入的数据
SELECT record_id, trade_no, out_trade_no, total_amount, trade_status, subject 
FROM alipay_wap_pay_records 
ORDER BY record_id;
