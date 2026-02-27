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

def encrypt_pdf_files():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始加密PDF文件...")
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
        
        # 2. 遍历加密文件目录下的所有PDF文件
        print("\n2. 遍历加密文件目录下的所有PDF文件...")
        pdf_files = []
        for filename in os.listdir(ENCRYPT_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        print(f"✅ 找到{len(pdf_files)}个PDF文件")
        
        # 3. 检查哪些文件没有找到密码
        print("\n3. 检查哪些文件没有找到密码...")
        no_password_files = []
        for filename in pdf_files:
            if filename not in file_info_map:
                no_password_files.append(filename)
        
        if no_password_files:
            print(f"⚠️  有{len(no_password_files)}个文件在file_info表中没有找到密码")
            for i, filename in enumerate(no_password_files[:10]):
                print(f"  {i+1}. {filename}")
            if len(no_password_files) > 10:
                print(f"  ... 还有{len(no_password_files)-10}个文件")
        else:
            print("✅ 所有文件都在file_info表中找到了密码")
        
        # 4. 加密每个PDF文件（跳过已加密的文件）
        print("\n4. 开始加密PDF文件...")
        success_count = 0
        skipped_count = 0
        failed_count = 0
        no_password_count = 0
        
        for i, filename in enumerate(pdf_files):
            filepath = os.path.join(ENCRYPT_DIR, filename)
            
            # 从file_info_map中获取密码
            password = file_info_map.get(filename)
            
            if not password:
                no_password_count += 1
                continue
            
            try:
                # 读取PDF文件
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f)
                    
                    # 检查是否已经加密
                    if reader.is_encrypted:
                        skipped_count += 1
                        if (i + 1) % 100 == 0:
                            print(f"⏭️  已处理{i+1}/{len(pdf_files)}个文件...")
                        continue
                    
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
                    
                    success_count += 1
                    if (i + 1) % 100 == 0:
                        print(f"✅ 已处理{i+1}/{len(pdf_files)}个文件...")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ 加密失败：{filename}, 错误：{str(e)}")
        
        # 5. 统计结果
        print("\n" + "=" * 80)
        print("加密统计：")
        print(f"  - 总PDF文件数：{len(pdf_files)}")
        print(f"  - 成功加密：{success_count}个")
        print(f"  - 已加密跳过：{skipped_count}个")
        print(f"  - 加密失败：{failed_count}个")
        print(f"  - 未找到密码：{no_password_count}个")
        print("=" * 80)
        
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
    print("开始加密PDF文件")
    print("=" * 80)
    encrypt_pdf_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
