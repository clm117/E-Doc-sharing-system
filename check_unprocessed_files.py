import cx_Oracle
import os

DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

ENCRYPTED_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def check_unprocessed_files():
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
        
        print("\n检查已生成的压缩包...")
        zip_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.lower().endswith('.zip'):
                zip_files.append(filename)
        
        print(f"找到{len(zip_files)}个压缩包")
        
        print("\n查找未生成压缩包的PDF文件...")
        unprocessed_files = []
        no_file_id_files = []
        no_txt_files = []
        
        for filename in pdf_files:
            pdf_name = filename.replace('.pdf', '.zip')
            
            if pdf_name in zip_files:
                continue
            
            file_id = file_info_map.get(filename)
            
            if not file_id:
                no_file_id_files.append(filename)
                continue
            
            txt_filename = f"密码链接说明{file_id}.txt"
            txt_path = os.path.join(ENCRYPTED_DIR, txt_filename)
            
            if not os.path.exists(txt_path):
                no_txt_files.append(filename)
                continue
            
            unprocessed_files.append(filename)
        
        print("\n" + "=" * 80)
        print("未生成压缩包的文件统计：")
        print(f"  - 未处理PDF文件总数：{len(unprocessed_files)}")
        print(f"  - 未找到file_id：{len(no_file_id_files)}")
        print(f"  - 未找到txt文件：{len(no_txt_files)}")
        print("=" * 80)
        
        if unprocessed_files:
            print("\n未生成压缩包的文件列表：")
            for i, filename in enumerate(unprocessed_files, 1):
                file_id = file_info_map.get(filename, 'N/A')
                print(f"  {i}. {filename} (file_id: {file_id})")
        
        if no_file_id_files:
            print("\n未找到file_id的文件：")
            for i, filename in enumerate(no_file_id_files[:10], 1):
                print(f"  {i}. {filename}")
            if len(no_file_id_files) > 10:
                print(f"  ... 还有{len(no_file_id_files)-10}个文件")
        
        if no_txt_files:
            print("\n未找到txt文件的文件：")
            for i, filename in enumerate(no_txt_files[:10], 1):
                print(f"  {i}. {filename}")
            if len(no_txt_files) > 10:
                print(f"  ... 还有{len(no_txt_files)-10}个文件")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("检查完成！")
        
    except Exception as e:
        print(f"检查失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始检查未生成压缩包的文件")
    print("=" * 80)
    check_unprocessed_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
