import os

# 目标目录
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def verify_copy_result():
    try:
        print("验证PDF文件复制结果...")
        print("=" * 80)
        
        # 遍历目标目录下的所有PDF文件
        pdf_files = []
        for filename in os.listdir(TARGET_DIR):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(filename)
        
        print(f"目标目录：{TARGET_DIR}")
        print(f"找到{len(pdf_files)}个PDF文件\n")
        
        # 显示前20个文件
        print("前20个PDF文件：")
        for i, filename in enumerate(pdf_files[:20]):
            print(f"  {i+1}. {filename}")
        
        if len(pdf_files) > 20:
            print(f"\n... 还有{len(pdf_files)-20}个文件")
        
        print("\n" + "=" * 80)
        print(f"总计：{len(pdf_files)}个PDF文件")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ 验证失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_copy_result()
