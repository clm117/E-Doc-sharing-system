-- 修改file_info表结构，将文件分类字段改为允许为空

-- 修改文件大类字段为允许为空
ALTER TABLE file_info MODIFY file_major_class VARCHAR2(20) NULL;

-- 修改文件中类字段为允许为空
ALTER TABLE file_info MODIFY file_mid_class VARCHAR2(20) NULL;

-- 修改文件小类字段为允许为空
ALTER TABLE file_info MODIFY file_minor_class VARCHAR2(20) NULL;

-- 删除之前的检查约束
ALTER TABLE file_info DROP CONSTRAINT ck_file_major_class;
ALTER TABLE file_info DROP CONSTRAINT ck_file_mid_class;
ALTER TABLE file_info DROP CONSTRAINT ck_file_minor_class;

-- 提交事务
COMMIT;

-- 输出修改成功信息
SELECT 'file_info表结构修改成功，文件分类字段已改为允许为空' AS message FROM DUAL;
