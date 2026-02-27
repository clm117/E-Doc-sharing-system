import os
from PyPDF2 import PdfReader

# 加密文件目录
ENCRYPT_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def quick_verify():
    try:
        print("快速验证PDF文件加密状态...")
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
        
        # 检查所有文件的加密状态
        for filename in pdf_files:
            filepath = os.path.join(ENCRYPT_DIR, filename)
            
            try:
                # 尝试不使用密码打开PDF
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f)
                    
                    # 检查是否加密
                    if reader.is_encrypted:
                        encrypted_count += 1
                    else:
                        not_encrypted_count += 1
            
            except Exception as e:
                error_count += 1
        
        # 统计结果
        print("验证统计：")
        print(f"  - 总PDF文件数：{len(pdf_files)}")
        print(f"  - 已加密：{encrypted_count}个")
        print(f"  - 未加密：{not_encrypted_count}个")
        print(f"  - 检查失败：{error_count}个")
        print("=" * 80)
        
        if not_encrypted_count == 0 and error_count == 0:
            print("\n✅ 所有PDF文件都已成功加密！")
        else:
            print(f"\n⚠️  还有{not_encrypted_count}个文件未加密，{error_count}个文件检查失败")
        
        print("验证完成！")
        
    except Exception as e:
        print(f"❌ 验证失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    quick_verify()
