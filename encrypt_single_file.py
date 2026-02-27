import cx_Oracle
import os
from PyPDF2 import PdfReader, PdfWriter

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# 加密文件目录
ENCRYPT_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def encrypt_single_file():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        filename = "Python初学教程：《简明Python教程》.pdf"
        filepath = os.path.join(ENCRYPT_DIR, filename)
        
        print(f"开始加密文件：{filename}")
        print("=" * 80)
        
        # 1. 查询file_info表中的文件信息
        print("\n1. 查询file_info表中的文件信息...")
        cursor.execute("""
            SELECT file_password
            FROM file_info
            WHERE file_name = :filename
        """, filename=filename)
        
        result = cursor.fetchone()
        if not result:
            print(f"❌ 未找到文件信息：{filename}")
            cursor.close()
            connection.close()
            return
        
        password = result[0]
        print(f"✅ 找到密码：{password}")
        
        # 2. 检查文件是否存在
        print(f"\n2. 检查文件是否存在...")
        if not os.path.exists(filepath):
            print(f"❌ 文件不存在：{filepath}")
            cursor.close()
            connection.close()
            return
        print(f"✅ 文件存在")
        
        # 3. 读取并加密PDF文件
        print(f"\n3. 读取并加密PDF文件...")
        try:
            with open(filepath, 'rb') as f:
                reader = PdfReader(f, strict=False)
                
                # 检查是否已经加密
                if reader.is_encrypted:
                    print(f"✅ 文件已经加密")
                else:
                    # 创建PDF写入器
                    writer = PdfWriter()
                    
                    # 复制所有页面
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    # 加密PDF
                    writer.encrypt(password)
                    
                    # 写入加密后的文件
                    with open(filepath, 'wb') as output_file:
                        writer.write(output_file)
                    
                    print(f"✅ 加密成功")
            
            # 4. 验证加密结果
            print(f"\n4. 验证加密结果...")
            with open(filepath, 'rb') as f:
                reader = PdfReader(f, strict=False)
                if reader.is_encrypted:
                    print(f"✅ 文件已成功加密")
                else:
                    print(f"❌ 文件未加密")
            
            print("\n" + "=" * 80)
            print("✅✅✅ 文件加密完成！✅✅✅")
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ 加密失败：{str(e)}")
            import traceback
            traceback.print_exc()
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("加密完成！")
        
    except Exception as e:
        print(f"❌ 加密失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始加密单个文件")
    print("=" * 80)
    encrypt_single_file()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
