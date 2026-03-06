-- 更新SQLite的file_info表，添加Oracle中存在的缺失字段
-- 所有新增字段允许为空，确保不影响现有代码

-- 添加作者信息
ALTER TABLE file_info ADD COLUMN file_author TEXT DEFAULT NULL;

-- 添加标准化文件名
ALTER TABLE file_info ADD COLUMN standard_name TEXT DEFAULT NULL;

-- 添加核心搜索关键字
ALTER TABLE file_info ADD COLUMN search_keywords TEXT DEFAULT NULL;

-- 添加标签
ALTER TABLE file_info ADD COLUMN file_tags TEXT DEFAULT NULL;

-- 添加ISBN号
ALTER TABLE file_info ADD COLUMN file_isbn TEXT DEFAULT NULL;

-- 添加价格类型
ALTER TABLE file_info ADD COLUMN file_price_type TEXT DEFAULT '1';

-- 添加文件路径
ALTER TABLE file_info ADD COLUMN file_path TEXT DEFAULT NULL;

-- 添加备注字段
ALTER TABLE file_info ADD COLUMN remark1 TEXT DEFAULT NULL;
ALTER TABLE file_info ADD COLUMN remark2 TEXT DEFAULT NULL;
ALTER TABLE file_info ADD COLUMN remark3 TEXT DEFAULT NULL;

-- 为新增字段创建索引，提高查询性能
CREATE INDEX IF NOT EXISTS idx_file_author ON file_info(file_author);
CREATE INDEX IF NOT EXISTS idx_file_isbn ON file_info(file_isbn);
CREATE INDEX IF NOT EXISTS idx_file_price_type ON file_info(file_price_type);
CREATE INDEX IF NOT EXISTS idx_standard_name ON file_info(standard_name);
