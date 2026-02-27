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

def encrypt_and_copy_files():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT file_name, file_password
            FROM file_info
            WHERE file_name IS NOT NULL
        """)
        file_info_map = {}
        for row in cursor.fetchall():
            file_name, file_password = row
            file_info_map[file_name] = file_password
        print(f"查询到{len(file_info_map)}个文件信息")
        
        print("\n递归遍历源目录下的所有PDF文件...")
        file_map = {}
        for root, dirs, files in os.walk(SOURCE_DIR):
            for filename in files:
                if filename.lower().endswith('.pdf'):
                    file_map[filename] = os.path.join(root, filename)
        print(f"找到{len(file_map)}个PDF文件")
        
        print("\n获取目标目录中的PDF文件...")
        target_files = set()
        for filename in os.listdir(TARGET_DIR):
            if filename.lower().endswith('.pdf'):
                target_files.add(filename)
        print(f"目标目录中有{len(target_files)}个PDF文件")
        
        print("\n开始加密并复制PDF文件...")
        success_count = 0
        failed_count = 0
        no_password_count = 0
        corrupt_files = []
        
        for filename, source_path in file_map.items():
            if filename in target_files:
                continue
            
            password = file_info_map.get(filename)
            
            if not password:
                no_password_count += 1
                continue
            
            target_path = os.path.join(TARGET_DIR, filename)
            
            try:
                with open(source_path, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    writer = PdfWriter()
                    
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    writer.encrypt(password)
                    
                    with open(target_path, 'wb') as output_file:
                        writer.write(output_file)
                    
                    success_count += 1
                    print(f"[{success_count}] 加密成功：{filename}")
                
            except Exception as e:
                error_msg = str(e)
                failed_count += 1
                
                if any(keyword in error_msg for keyword in [
                    "EOF marker not found", 
                    "endstream", 
                    "Stream has ended", 
                    "PdfReadError", 
                    "PdfStreamError", 
                    "RecursionError", 
                    "maximum recursion depth",
                    "Invalid Elementary Object",
                    "Invalid object"
                ]):
                    corrupt_files.append(filename)
                    print(f"[损坏] {filename}")
                else:
                    print(f"[失败] {filename}: {error_msg[:50]}")
        
        print("\n" + "=" * 80)
        print("加密并复制统计：")
        print(f"  - 源PDF文件数：{len(file_map)}")
        print(f"  - 成功加密并复制：{success_count}个")
        print(f"  - 加密失败：{failed_count}个")
        print(f"  - 未找到密码：{no_password_count}个")
        print(f"  - 损坏文件：{len(corrupt_files)}个")
        print("=" * 80)
        
        if corrupt_files:
            print("\n损坏的PDF文件列表：")
            for i, filename in enumerate(corrupt_files):
                print(f"  {i+1}. {filename}")
        
        print("\n验证目标目录...")
        target_files = []
        for filename in os.listdir(TARGET_DIR):
            if filename.lower().endswith('.pdf'):
                target_files.append(filename)
        
        encrypted_count = 0
        not_encrypted_count = 0
        error_count = 0
        
        for filename in target_files:
            filepath = os.path.join(TARGET_DIR, filename)
            
            try:
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    if reader.is_encrypted:
                        encrypted_count += 1
                    else:
                        not_encrypted_count += 1
            except:
                error_count += 1
        
        print("目标目录验证统计：")
        print(f"  - 总PDF文件数：{len(target_files)}")
        print(f"  - 已加密：{encrypted_count}个")
        print(f"  - 未加密：{not_encrypted_count}个")
        print(f"  - 检查失败：{error_count}个")
        
        if not_encrypted_count == 0 and error_count == 0:
            print("\n" + "=" * 80)
            print("[SUCCESS] 所有PDF文件都已成功加密并复制！")
            print("=" * 80)
        else:
            print(f"\n[WARNING] 还有{not_encrypted_count}个文件未加密，{error_count}个文件检查失败")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("加密并复制完成！")
        
    except Exception as e:
        print(f"[ERROR] 加密并复制失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始加密并复制PDF文件")
    print("=" * 80)
    encrypt_and_copy_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
