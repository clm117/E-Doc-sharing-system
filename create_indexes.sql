-- 数据库索引优化脚本
-- 为alipay_wap_pay_records表创建索引，提高查询性能

-- 1. 为out_trade_no字段创建索引
-- 用途：根据商户订单号查询交易记录
-- 使用场景：/alipay_notify和/alipay_return路由
CREATE INDEX idx_out_trade_no ON alipay_wap_pay_records(out_trade_no);

-- 2. 为trade_status字段创建索引
-- 用途：根据交易状态查询交易记录
-- 使用场景：查询已支付、待支付、失败的订单
CREATE INDEX idx_trade_status ON alipay_wap_pay_records(trade_status);

-- 3. 为session_id字段创建索引
-- 用途：根据会话ID查询交易记录
-- 使用场景：验证用户权限，防止跨用户访问
CREATE INDEX idx_session_id ON alipay_wap_pay_records(session_id);

-- 4. 为file_id字段创建索引
-- 用途：根据文件ID查询交易记录
-- 使用场景：查询某个文件的所有交易记录
CREATE INDEX idx_file_id ON alipay_wap_pay_records(file_id);

-- 5. 为gmt_create字段创建索引
-- 用途：根据创建时间查询交易记录
-- 使用场景：后台管理系统查询最近交易
CREATE INDEX idx_gmt_create ON alipay_wap_pay_records(gmt_create);

-- 6. 为gmt_payment字段创建索引
-- 用途：根据支付时间查询交易记录
-- 使用场景：统计今日收入、查询某日支付记录
CREATE INDEX idx_gmt_payment ON alipay_wap_pay_records(gmt_payment);

-- 7. 复合索引：trade_status和gmt_create
-- 用途：查询特定状态下的最近交易
-- 使用场景：查询最近的成功交易
CREATE INDEX idx_trade_status_gmt_create ON alipay_wap_pay_records(trade_status, gmt_create);

-- 查看索引创建结果
SELECT index_name, table_name, column_name 
FROM user_ind_columns 
WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
ORDER BY index_name, column_position;