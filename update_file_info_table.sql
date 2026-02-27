-- 优化file_info表，添加新字段
-- 所有新增字段允许为空，确保不影响现有代码

ALTER TABLE file_info ADD (
    -- 作者信息
    FILE_AUTHOR VARCHAR2(100) DEFAULT NULL,
    
    -- 标准化文件名（去除特殊字符、版本号等冗余信息）
    STANDARD_NAME VARCHAR2(200) DEFAULT NULL,
    
    -- 核心搜索关键字，用于爬虫搜索
    SEARCH_KEYWORDS VARCHAR2(200) DEFAULT NULL,
    
    -- 标签，用于分类和过滤
    FILE_TAGS VARCHAR2(300) DEFAULT NULL,
    
    -- ISBN号，唯一标识，提高匹配度
    FILE_ISBN VARCHAR2(20) DEFAULT NULL,
    
    -- 备注字段，用于扩展信息
    REMARK1 VARCHAR2(200) DEFAULT NULL,
    REMARK2 VARCHAR2(200) DEFAULT NULL,
    REMARK3 VARCHAR2(200) DEFAULT NULL
);

-- 提交事务
COMMIT;
