import os
from PyPDF2 import PdfReader

# 加密文件目录
ENCRYPT_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def simple_verify():
    try:
        print("简单验证PDF文件加密状态...")
        print("=" * 80)
        
        # 遍历加密文件目录下的所有PDF文件
        pdf_files = []
        for filename in os.listdir(ENCRYPT_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        
        print(f"找到{len(pdf_files)}个PDF文件\n")
        
        encrypted_count = 0
        not_encrypted_count = 0
        error_count = 0
        
        # 只检查前50个文件的状态
        print("检查前50个文件的加密状态：\n")
        for i, filename in enumerate(pdf_files[:50]):
            filepath = os.path.join(ENCRYPT_DIR, filename)
            
            try:
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f)
                    if reader.is_encrypted:
                        encrypted_count += 1
                    else:
                        not_encrypted_count += 1
                        print(f"❌ 未加密：{filename}")
            except Exception as e:
                error_count += 1
                print(f"⚠️  错误：{filename}, {str(e)[:50]}")
        
        # 统计结果
        print("\n" + "=" * 80)
        print("验证统计（前50个文件）：")
        print(f"  - 已加密：{encrypted_count}个")
        print(f"  - 未加密：{not_encrypted_count}个")
        print(f"  - 检查失败：{error_count}个")
        print("=" * 80)
        
        print(f"\n总PDF文件数：{len(pdf_files)}")
        print("验证完成！")
        
    except Exception as e:
        print(f"❌ 验证失败：{str(e)}")

if __name__ == '__main__':
    simple_verify()
