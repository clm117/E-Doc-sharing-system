import os
from PyPDF2 import PdfReader, PdfWriter

SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

unprocessed_files = [
    ("[图灵原创].Go语言编程.pdf", "598313"),
    ("[图灵程序设计丛书].Bootstrap实战.pdf", "296499"),
    ("《Python高性能（第2版）》_杨培文等.pdf", "120627"),
    ("万物简史.pdf", "124515"),
    ("上海交通大学生存手册.pdf", "920590"),
    ("第一次世界大战的起源 （下册）.pdf", "845758"),
    ("第一次世界大战的起源（上）.pdf", "177465"),
]

def encrypt_single_file(filename, password):
    source_path = None
    for root, dirs, files in os.walk(SOURCE_DIR):
        if filename in files:
            source_path = os.path.join(root, filename)
            break
    
    if not source_path:
        return False, "未找到源文件"
    
    target_path = os.path.join(TARGET_DIR, filename)
    
    try:
        reader = PdfReader(source_path, strict=False)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(password)
        
        with open(target_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True, "成功"
    except Exception as e:
        error_msg = str(e)
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
            return False, "文件损坏"
        else:
            return False, f"失败: {error_msg[:50]}"

def encrypt_and_copy_files():
    try:
        print("开始加密并复制PDF文件...")
        print("=" * 80)
        
        success_count = 0
        failed_count = 0
        corrupt_files = []
        
        for i, (filename, password) in enumerate(unprocessed_files):
            print(f"\n[{i+1}/{len(unprocessed_files)}] 处理：{filename}")
            
            success, message = encrypt_single_file(filename, password)
            
            if success:
                success_count += 1
                print(f"  [{success_count}] {message}：{filename}")
            else:
                failed_count += 1
                if message == "文件损坏":
                    corrupt_files.append(filename)
                print(f"  [{failed_count}] {message}：{filename}")
        
        print("\n" + "=" * 80)
        print("加密并复制统计：")
        print(f"  - 总文件数：{len(unprocessed_files)}")
        print(f"  - 成功加密并复制：{success_count}个")
        print(f"  - 加密失败：{failed_count}个")
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
        
        print("\n加密并复制完成！")
        
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
