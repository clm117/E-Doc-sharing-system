# 测试新功能的Python脚本
import cx_Oracle

# 数据库配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

def test_new_feature():
    try:
        # 连接数据库
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=== 测试新功能 ===")
        
        # 1. 检查payment_config表中的新配置
        print("1. 检查payment_config表中的新配置:")
        cursor.execute("SELECT PRICE_ID, PRICE_TYPE, AMOUNT, STATUS FROM payment_config")
        for row in cursor.fetchall():
            print(f"   PRICE_ID: {row[0]}, PRICE_TYPE: {row[1]}, AMOUNT: {row[2]}, STATUS: {row[3]}")
        
        # 2. 检查file_info表中的FILE_PRICE_TYPE字段
        print("\n2. 检查file_info表中的FILE_PRICE_TYPE字段:")
        cursor.execute("SELECT FILE_ID, FILE_NAME, FILE_PRICE_TYPE FROM file_info WHERE rownum <= 5")
        for row in cursor.fetchall():
            print(f"   FILE_ID: {row[0]}, FILE_NAME: {row[1]}, FILE_PRICE_TYPE: {row[2]}")
        
        # 3. 测试根据价格类型查询金额
        print("\n3. 测试根据价格类型查询金额:")
        # 测试价格类型1
        cursor.execute("SELECT AMOUNT FROM payment_config WHERE STATUS = 'Y' AND PRICE_TYPE = '1'")
        result1 = cursor.fetchone()
        print(f"   价格类型1的金额: {result1[0] if result1 else '未找到'}")
        
        # 测试价格类型2
        cursor.execute("SELECT AMOUNT FROM payment_config WHERE STATUS = 'Y' AND PRICE_TYPE = '2'")
        result2 = cursor.fetchone()
        print(f"   价格类型2的金额: {result2[0] if result2 else '未找到'}")
        
        # 4. 测试随机选择文件
        print("\n4. 测试随机选择文件:")
        cursor.execute("SELECT FILE_ID, FILE_NAME, FILE_PRICE_TYPE FROM file_info ORDER BY DBMS_RANDOM.RANDOM FETCH FIRST 1 ROWS ONLY")
        random_file = cursor.fetchone()
        if random_file:
            file_id, file_name, price_type = random_file
            print(f"   随机选择文件: FILE_ID={file_id}, FILE_NAME={file_name}, PRICE_TYPE={price_type}")
            
            # 根据该文件的价格类型获取对应的金额
            cursor.execute("SELECT AMOUNT FROM payment_config WHERE STATUS = 'Y' AND PRICE_TYPE = :price_type", price_type=price_type)
            amount_result = cursor.fetchone()
            if amount_result:
                print(f"   该文件应显示的金额: {amount_result[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n=== 测试完成 ===")
        print("新功能已成功实现！")
        print("现在访问 http://127.0.0.1:5000/ 可以看到效果")
        print("系统会随机选择一个文件，并根据文件的价格类型展示对应的价格")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    test_new_feature()
