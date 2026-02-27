import os
from PyPDF2 import PdfReader, PdfWriter

SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

filename = "C语言趣味编程100例.pdf"
password = "414016"

print(f"测试文件：{filename}")
print(f"密码：{password}")

source_path = None
for root, dirs, files in os.walk(SOURCE_DIR):
    if filename in files:
        source_path = os.path.join(root, filename)
        break

if not source_path:
    print(f"未找到源文件：{filename}")
else:
    print(f"源文件路径：{source_path}")
    
    target_path = os.path.join(TARGET_DIR, filename)
    print(f"目标文件路径：{target_path}")
    
    try:
        print("开始加密...")
        with open(source_path, 'rb') as f:
            reader = PdfReader(f, strict=False)
            print(f"PDF页数：{len(reader.pages)}")
            
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            with open(target_path, 'wb') as output_file:
                writer.write(output_file)
        
        print("加密成功！")
        
        print("验证加密...")
        with open(target_path, 'rb') as f:
            reader = PdfReader(f, strict=False)
            if reader.is_encrypted:
                print("文件已加密")
            else:
                print("文件未加密")
    except Exception as e:
        print(f"加密失败：{str(e)}")
        import traceback as tb
        tb.print_exc()
