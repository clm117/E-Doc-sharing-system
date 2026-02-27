import cx_Oracle
import os
import zipfile

DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

ENCRYPTED_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def create_zip_files():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("查询file_info表...")
        cursor.execute("""
            SELECT file_id, file_name
            FROM file_info
            WHERE file_name IS NOT NULL
        """)
        
        file_info_map = {}
        for row in cursor.fetchall():
            file_id, file_name = row
            file_info_map[file_name] = file_id
        
        print(f"查询到{len(file_info_map)}个文件信息")
        
        print("\n扫描加密文件目录...")
        pdf_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        
        print(f"找到{len(pdf_files)}个PDF文件")
        
        print("\n开始创建压缩包...")
        success_count = 0
        failed_count = 0
        no_txt_count = 0
        already_exists_count = 0
        
        for filename in pdf_files:
            file_id = file_info_map.get(filename)
            
            if not file_id:
                print(f"[跳过] 未找到file_id：{filename}")
                continue
            
            pdf_path = os.path.join(ENCRYPTED_DIR, filename)
            txt_filename = f"密码链接说明{file_id}.txt"
            txt_path = os.path.join(ENCRYPTED_DIR, txt_filename)
            
            zip_filename = filename.replace('.pdf', '.zip')
            zip_path = os.path.join(ENCRYPTED_DIR, zip_filename)
            
            if os.path.exists(zip_path):
                already_exists_count += 1
                print(f"[跳过] 压缩包已存在：{zip_filename}")
                continue
            
            if not os.path.exists(txt_path):
                no_txt_count += 1
                print(f"[跳过] txt文件不存在：{txt_filename}")
                continue
            
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(pdf_path, filename)
                    zipf.write(txt_path, txt_filename)
                
                success_count += 1
                if success_count % 100 == 0:
                    print(f"[进度] 已创建{success_count}/{len(pdf_files)}个压缩包")
            
            except Exception as e:
                failed_count += 1
                print(f"[失败] {filename}: {str(e)}")
        
        print("\n" + "=" * 80)
        print("创建压缩包统计：")
        print(f"  - PDF文件总数：{len(pdf_files)}")
        print(f"  - 成功创建：{success_count}个")
        print(f"  - 创建失败：{failed_count}个")
        print(f"  - txt文件不存在：{no_txt_count}个")
        print(f"  - 压缩包已存在：{already_exists_count}个")
        print("=" * 80)
        
        print("\n验证生成的压缩包...")
        zip_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.lower().endswith('.zip'):
                zip_files.append(filename)
        
        print(f"目录中共有{len(zip_files)}个压缩包")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("创建压缩包完成！")
        
    except Exception as e:
        print(f"创建压缩包失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始创建压缩包")
    print("=" * 80)
    create_zip_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
