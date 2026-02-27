import cx_Oracle
import os
from PyPDF2 import PdfReader, PdfWriter
import traceback as tb

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# 加密文件目录
ENCRYPT_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def encrypt_all_files_final():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始加密所有PDF文件（最终版）...")
        print("=" * 80)
        
        # 1. 查询file_info表中的所有文件信息
        print("\n1. 查询file_info表中的所有文件信息...")
        cursor.execute("""
            SELECT file_name, file_password
            FROM file_info
            WHERE file_name IS NOT NULL
        """)
        file_info_map = {}
        for row in cursor.fetchall():
            file_name, file_password = row
            file_info_map[file_name] = file_password
        print(f"✅ 查询到{len(file_info_map)}个文件信息")
        
        # 2. 遍历目标目录下的所有PDF文件
        print("\n2. 遍历目标目录下的所有PDF文件...")
        pdf_files = []
        for filename in os.listdir(ENCRYPT_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        print(f"✅ 找到{len(pdf_files)}个PDF文件")
        
        # 3. 加密每个PDF文件（最终版）
        print("\n3. 开始加密每个PDF文件...")
        success_count = 0
        skipped_count = 0
        failed_count = 0
        no_password_count = 0
        corrupt_files = []
        
        for i, filename in enumerate(pdf_files):
            filepath = os.path.join(ENCRYPT_DIR, filename)
            
            # 从file_info_map中获取密码
            password = file_info_map.get(filename)
            
            if not password:
                no_password_count += 1
                print(f"⚠️  [{i+1}/{len(pdf_files)}] 未找到密码：{filename}")
                continue
            
            try:
                # 读取PDF文件（使用最宽松的参数）
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    
                    # 检查是否已经加密
                    if reader.is_encrypted:
                        skipped_count += 1
                        if (i + 1) % 100 == 0:
                            print(f"⏭️  已处理{i+1}/{len(pdf_files)}个文件...")
                        continue
                    
                    # 创建PDF写入器
                    writer = PdfWriter()
                    
                    # 复制所有页面
                    page_count = len(reader.pages)
                    for page_num in range(page_count):
                        try:
                            page = reader.pages[page_num]
                            writer.add_page(page)
                        except Exception as e:
                            print(f"⚠️  [{i+1}/{len(pdf_files)}] 页面{page_num}读取失败，跳过：{filename}")
                            break
                    
                    # 加密PDF
                    writer.encrypt(password)
                    
                    # 写入加密后的文件
                    with open(filepath, 'wb') as output_file:
                        writer.write(output_file)
                    
                    success_count += 1
                    print(f"✅ [{i+1}/{len(pdf_files)}] 加密成功：{filename}")
                
            except Exception as e:
                error_msg = str(e)
                failed_count += 1
                
                # 记录损坏的文件（所有可能的错误）
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
                    print(f"⚠️  [{i+1}/{len(pdf_files)}] 文件损坏，跳过：{filename}")
                else:
                    print(f"❌ [{i+1}/{len(pdf_files)}] 加密失败：{filename}, 错误：{error_msg[:80]}")
        
        # 4. 统计结果
        print("\n" + "=" * 80)
        print("加密统计：")
        print(f"  - 总PDF文件数：{len(pdf_files)}")
        print(f"  - 成功加密：{success_count}个")
        print(f"  - 已加密跳过：{skipped_count}个")
        print(f"  - 加密失败：{failed_count}个")
        print(f"  - 未找到密码：{no_password_count}个")
        print(f"  - 损坏文件：{len(corrupt_files)}个")
        print("=" * 80)
        
        if corrupt_files:
            print("\n损坏的PDF文件列表：")
            for i, filename in enumerate(corrupt_files[:30]):
                print(f"  {i+1}. {filename}")
            if len(corrupt_files) > 30:
                print(f"  ... 还有{len(corrupt_files)-30}个文件")
        
        # 5. 验证最终结果
        print("\n5. 验证最终结果...")
        final_encrypted = 0
        final_not_encrypted = 0
        final_error = 0
        
        for filename in pdf_files:
            filepath = os.path.join(ENCRYPT_DIR, filename)
            
            try:
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    if reader.is_encrypted:
                        final_encrypted += 1
                    else:
                        final_not_encrypted += 1
                        if final_not_encrypted <= 30:
                            print(f"❌ 未加密：{filename}")
            except:
                final_error += 1
        
        print("最终验证统计：")
        print(f"  - 总PDF文件数：{len(pdf_files)}")
        print(f"  - 已加密：{final_encrypted}个")
        print(f"  - 未加密：{final_not_encrypted}个")
        print(f"  - 检查失败：{final_error}个")
        
        if final_not_encrypted == 0 and final_error == 0:
            print("\n" + "=" * 80)
            print("✅✅✅ 所有PDF文件都已成功加密！✅✅✅")
            print("=" * 80)
        else:
            print(f"\n⚠️  还有{final_not_encrypted}个文件未加密，{final_error}个文件检查失败")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("加密完成！")
        
    except Exception as e:
        print(f"❌ 加密失败：{str(e)}")
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始加密所有PDF文件（最终版）")
    print("=" * 80)
    encrypt_all_files_final()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
