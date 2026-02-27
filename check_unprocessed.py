import cx_Oracle
import os

DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def check_files():
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
        
        print("\n查找未处理的文件...")
        unprocessed_files = []
        for filename in file_map.keys():
            if filename not in target_files:
                password = file_info_map.get(filename)
                unprocessed_files.append((filename, password))
        
        print(f"未处理的文件数：{len(unprocessed_files)}")
        
        if unprocessed_files:
            print("\n未处理的文件列表：")
            for i, (filename, password) in enumerate(unprocessed_files):
                print(f"  {i+1}. {filename} (密码: {password})")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"[ERROR] 检查失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("检查未处理的PDF文件")
    print("=" * 80)
    check_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
