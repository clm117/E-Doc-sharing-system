import cx_Oracle
import os

DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

ENCRYPTED_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"
BASE_URL = "http://192.168.100.174:5000/?file_id="

def generate_txt_files():
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
        
        print("\n开始生成txt文件...")
        success_count = 0
        failed_count = 0
        no_file_id_count = 0
        
        for filename in pdf_files:
            file_id = file_info_map.get(filename)
            
            if not file_id:
                no_file_id_count += 1
                print(f"[跳过] 未找到file_id：{filename}")
                continue
            
            txt_filename = f"密码链接说明{file_id}.txt"
            txt_path = os.path.join(ENCRYPTED_DIR, txt_filename)
            
            url = BASE_URL + str(file_id)
            content = f"""文件资料仅供学习交流，收集不易，请复制以下链接，在浏览器打开并获取解压密码
{url}"""
            
            try:
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_count += 1
                if success_count % 100 == 0:
                    print(f"[进度] 已生成{success_count}/{len(pdf_files)}个txt文件")
            
            except Exception as e:
                failed_count += 1
                print(f"[失败] {filename}: {str(e)}")
        
        print("\n" + "=" * 80)
        print("生成txt文件统计：")
        print(f"  - PDF文件总数：{len(pdf_files)}")
        print(f"  - 成功生成：{success_count}个")
        print(f"  - 生成失败：{failed_count}个")
        print(f"  - 未找到file_id：{no_file_id_count}个")
        print("=" * 80)
        
        print("\n验证生成的txt文件...")
        txt_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.startswith('密码链接说明') and filename.endswith('.txt'):
                txt_files.append(filename)
        
        print(f"目录中共有{len(txt_files)}个txt文件")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("生成txt文件完成！")
        
    except Exception as e:
        print(f"生成txt文件失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始生成txt文件")
    print("=" * 80)
    generate_txt_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
