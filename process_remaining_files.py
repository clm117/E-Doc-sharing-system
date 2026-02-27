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
BASE_URL = "http://192.168.100.174:5000/?file_id="

unprocessed_files = [
    ("[图灵程序设计丛书].C#并发编程经典实例.PDF", "20260113000000955"),
    ("心理学基础(王朝庄).PDF", "20260113000001464"),
    ("心理学无处不在 59个日常生活问题的心理学解释 布鲁克斯.PDF", "20260113000001478"),
    ("心理学研究方法( 第2版，王重鸣.PDF", "20260113000001491"),
    ("心理强大之路.PDF", "20260113000001507"),
    ("现代心理学原理与应用(第二版,朱宝荣等).PDF", "20260113000001728"),
    ("罗兰贝格－消费心理分析.PDF", "20260113000001788"),
    ("钱宾四先生全集 第002册 四书释义 论语文解.PDF", "20260113000001862"),
    ("钱宾四先生全集 第003册 论语新解.PDF", "20260113000001863"),
    ("钱宾四先生全集 第005册 先秦诸子系年.PDF", "20260113000001864"),
    ("钱宾四先生全集 第008册 两汉经学 今古文平议.PDF", "20260113000001865"),
    ("钱宾四先生全集 第016册 中国近三百年学术史（一）.PDF", "20260113000001866"),
    ("钱宾四先生全集 第026册 周公 秦汉史.PDF", "20260113000001867"),
    ("钱宾四先生全集 第029册 中国文化史导论 中国历史精神.PDF", "20260113000001868"),
    ("钱宾四先生全集 第030册 国史新论.PDF", "20260113000001869"),
    ("钱宾四先生全集 第033册 中国史学名着.PDF", "20260113000001871"),
    ("钱宾四先生全集 第042册 历史与文化论丛.PDF", "20260113000001872"),
    ("钱宾四先生全集 第043册 世界局势与中国文化.PDF", "20260113000001873"),
]

def create_txt_and_zip_files():
    try:
        print("开始为未处理的文件创建txt文件和压缩包...")
        print("=" * 80)
        
        success_count = 0
        failed_count = 0
        
        for filename, file_id in unprocessed_files:
            txt_filename = f"密码链接说明{file_id}.txt"
            txt_path = os.path.join(ENCRYPTED_DIR, txt_filename)
            
            url = BASE_URL + file_id
            content = f"""文件资料仅供学习交流，收集不易，请复制以下链接，在浏览器打开并获取解压密码
{url}"""
            
            try:
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_count += 1
                print(f"[{success_count}/18] 创建txt文件：{txt_filename}")
                
            except Exception as e:
                failed_count += 1
                print(f"[失败] {filename}: {str(e)}")
        
        print("\n" + "=" * 80)
        print("txt文件创建统计：")
        print(f"  - 成功创建：{success_count}个")
        print(f"  - 创建失败：{failed_count}个")
        print("=" * 80)
        
        print("\n开始创建压缩包...")
        print("=" * 80)
        
        success_zip_count = 0
        failed_zip_count = 0
        
        for filename, file_id in unprocessed_files:
            pdf_path = os.path.join(ENCRYPTED_DIR, filename)
            txt_filename = f"密码链接说明{file_id}.txt"
            txt_path = os.path.join(ENCRYPTED_DIR, txt_filename)
            zip_filename = filename.replace('.PDF', '.zip')
            zip_path = os.path.join(ENCRYPTED_DIR, zip_filename)
            
            if os.path.exists(zip_path):
                print(f"[跳过] 压缩包已存在：{zip_filename}")
                continue
            
            if not os.path.exists(txt_path):
                print(f"[跳过] txt文件不存在：{txt_filename}")
                continue
            
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(pdf_path, filename)
                    zipf.write(txt_path, txt_filename)
                
                success_zip_count += 1
                print(f"[{success_zip_count}/18] 创建压缩包：{zip_filename}")
                
            except Exception as e:
                failed_zip_count += 1
                print(f"[失败] {filename}: {str(e)}")
        
        print("\n" + "=" * 80)
        print("压缩包创建统计：")
        print(f"  - 成功创建：{success_zip_count}个")
        print(f"  - 创建失败：{failed_zip_count}个")
        print("=" * 80)
        
        print("\n验证最终结果...")
        print("=" * 80)
        
        pdf_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        
        zip_files = []
        for filename in os.listdir(ENCRYPTED_DIR):
            if filename.lower().endswith('.zip'):
                zip_files.append(filename)
        
        print(f"PDF文件总数：{len(pdf_files)}")
        print(f"压缩包总数：{len(zip_files)}")
        print(f"应该相等：{len(pdf_files)} == {len(zip_files)}")
        print("=" * 80)
        
        print("所有任务完成！")
        
    except Exception as e:
        print(f"处理失败：{str(e)}")
        import traceback as tb
        tb.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始为未处理的18个文件创建txt文件和压缩包")
    print("=" * 80)
    create_txt_and_zip_files()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
