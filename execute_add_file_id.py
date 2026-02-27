import cx_Oracle

# Oracle数据库连接配置（与app.py保持一致）
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def add_file_id_field():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("检查file_id字段是否已存在...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM user_tab_columns 
            WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS' 
            AND column_name = 'FILE_ID'
        """)
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            print("file_id字段已存在，无需添加")
        else:
            print("开始添加file_id字段...")
            
            # 添加file_id字段
            cursor.execute("ALTER TABLE alipay_wap_pay_records ADD file_id VARCHAR2(18)")
            connection.commit()
            print("✅ file_id字段添加成功")
            
            # 添加外键约束
            try:
                cursor.execute("""
                    ALTER TABLE alipay_wap_pay_records 
                    ADD CONSTRAINT fk_alipay_wap_pay_file_id 
                    FOREIGN KEY (file_id) 
                    REFERENCES file_info(file_id) 
                    ON DELETE CASCADE
                """)
                connection.commit()
                print("✅ 外键约束添加成功")
            except Exception as e:
                print(f"⚠️  外键约束添加失败（可能已存在）: {str(e)}")
            
            # 添加索引
            try:
                cursor.execute("CREATE INDEX idx_alipay_file_id ON alipay_wap_pay_records(file_id)")
                connection.commit()
                print("✅ 索引添加成功")
            except Exception as e:
                print(f"⚠️  索引添加失败（可能已存在）: {str(e)}")
            
            # 验证字段是否添加成功
            cursor.execute("""
                SELECT column_name, data_type, nullable
                FROM user_tab_columns
                WHERE table_name = 'ALIPAY_WAP_PAY_RECORDS'
                AND column_name = 'FILE_ID'
            """)
            verify_result = cursor.fetchone()
            
            if verify_result:
                print(f"✅ 验证成功！")
                print(f"   字段名: {verify_result[0]}")
                print(f"   数据类型: {verify_result[1]}")
                print(f"   可为空: {verify_result[2]}")
            else:
                print("❌ 验证失败！")
        
        # 关闭连接
        cursor.close()
        connection.close()
        print("数据库连接已关闭")
        
    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")

if __name__ == '__main__':
    print("=" * 50)
    print("开始添加file_id字段到alipay_wap_pay_records表...")
    print("=" * 50)
    add_file_id_field()
    print("=" * 50)
    print("执行完成！")
    print("=" * 50)
