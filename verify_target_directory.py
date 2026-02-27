import os
from PyPDF2 import PdfReader

# 目标目录
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def verify_target_directory():
    try:
        print("验证目标目录的PDF文件加密状态...")
        print("=" * 80)
        
        # 遍历目标目录下的所有PDF文件
        pdf_files = []
        for filename in os.listdir(TARGET_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        
        print(f"找到{len(pdf_files)}个PDF文件\n")
        
        encrypted_count = 0
        not_encrypted_count = 0
        error_count = 0
        
        # 检查所有文件的加密状态
        for filename in pdf_files:
            filepath = os.path.join(TARGET_DIR, filename)
            
            try:
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f, strict=False)
                    if reader.is_encrypted:
                        encrypted_count += 1
                    else:
                        not_encrypted_count += 1
                        if not_encrypted_count <= 20:
                            print(f"❌ 未加密：{filename}")
            except Exception as e:
                error_count += 1
                if error_count <= 10:
                    print(f"⚠️  错误：{filename}, {str(e)[:60]}")
        
        # 统计结果
        print("\n" + "=" * 80)
        print("验证统计：")
        print(f"  - 总PDF文件数：{len(pdf_files)}")
        print(f"  - 已加密：{encrypted_count}个")
        print(f"  - 未加密：{not_encrypted_count}个")
        print(f"  - 检查失败：{error_count}个")
        print("=" * 80)
        
        if not_encrypted_count == 0 and error_count == 0:
            print("\n" + "=" * 80)
            print("✅✅✅ 所有PDF文件都已成功加密！✅✅✅")
            print("=" * 80)
        else:
            print(f"\n⚠️  还有{not_encrypted_count}个文件未加密，{error_count}个文件检查失败")
        
        print("验证完成！")
        
    except Exception as e:
        print(f"❌ 验证失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("验证目标目录的PDF文件加密状态")
    print("=" * 80)
    verify_target_directory()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
