import cx_Oracle
import os
from PyPDF2 import PdfReader, PdfWriter

DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def test_single_file():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT file_name, file_password
            FROM file_info
            WHERE file_name IS NOT NULL
            AND ROWNUM <= 1
        """)
        row = cursor.fetchone()
        if not row:
            print("没有找到文件信息")
            return
        
        filename, password = row
        print(f"测试文件：{filename}")
        print(f"密码：{password}")
        
        source_path = None
        for root, dirs, files in os.walk(SOURCE_DIR):
            if filename in files:
                source_path = os.path.join(root, filename)
                break
        
        if not source_path:
            print(f"未找到源文件：{filename}")
            return
        
        print(f"源文件路径：{source_path}")
        
        target_path = os.path.join(TARGET_DIR, filename)
        print(f"目标文件路径：{target_path}")
        
        print("开始加密...")
        with open(source_path, 'rb') as f:
            reader = PdfReader(f, strict=False)
            print(f"PDF页数：{len(reader.pages)}")
            
            writer = PdfWriter()
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)
            
            writer.encrypt(password)
            
            with open(target_path, 'wb') as output_file:
                writer.write(output_file)
        
        print("✅ 加密成功！")
        
        print("验证加密...")
        with open(target_path, 'rb') as f:
            reader = PdfReader(f, strict=False)
            if reader.is_encrypted:
                print("✅ 文件已加密")
            else:
                print("❌ 文件未加密")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("测试单个文件加密")
    print("=" * 80)
    test_single_file()
    print("=" * 80)
