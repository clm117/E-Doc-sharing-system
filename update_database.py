# 更新数据库结构和数据的Python脚本
import cx_Oracle

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def update_database():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始更新数据库...")
        
        # 1. 在payment_config表中插入新的价格配置
        print("1. 插入新的价格配置...")
        insert_sql = """
        INSERT INTO payment_config (PRICE_ID, PRICE_TYPE, AMOUNT, PAYMENT_URL, DESCRIPTION, STATUS, CREATE_TIME, UPDATE_TIME)
        VALUES (2, '2', 5.0, 'http://192.168.100.174:5000/mobile_payment_simple', '学习资料购买 高级配置', 'Y', SYSDATE, SYSDATE)
        """
        cursor.execute(insert_sql)
        print("   成功插入价格配置")
        
        # 2. 在file_info表中添加新字段FILE_PRICE_TYPE
        print("2. 添加FILE_PRICE_TYPE字段...")
        alter_sql = "ALTER TABLE file_info ADD (FILE_PRICE_TYPE CHAR(1) DEFAULT '1' NOT NULL)"
        cursor.execute(alter_sql)
        print("   成功添加字段")
        
        # 3. 更新现有file_info记录，设置不同的FILE_PRICE_TYPE值
        print("3. 更新现有记录的价格类型...")
        update_sql = "UPDATE file_info SET FILE_PRICE_TYPE = '2' WHERE FILE_ID IN ('20260112000000002', '20260112000000004')"
        cursor.execute(update_sql)
        print(f"   成功更新 {cursor.rowcount} 条记录")
        
        # 4. 提交事务
        connection.commit()
        print("4. 事务提交成功")
        
        # 5. 验证修改结果
        print("5. 验证修改结果...")
        
        # 查看payment_config表数据
        print("   payment_config表数据:")
        cursor.execute("SELECT * FROM payment_config")
        for row in cursor.fetchall():
            print(f"      {row}")
        
        # 查看file_info表数据
        print("   file_info表前5行数据:")
        cursor.execute("SELECT FILE_ID, FILE_NAME, FILE_PRICE_TYPE FROM file_info WHERE rownum <= 5")
        for row in cursor.fetchall():
            print(f"      {row}")
        
        cursor.close()
        connection.close()
        
        print("数据库更新完成！")
        
    except Exception as e:
        print(f"数据库更新失败: {str(e)}")
        # 回滚事务
        if 'connection' in locals():
            connection.rollback()

if __name__ == "__main__":
    update_database()
