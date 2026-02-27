import os

SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\待加密文件"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

print("检查源目录...")
file_map = {}
count = 0
for root, dirs, files in os.walk(SOURCE_DIR):
    for filename in files:
        if filename.lower().endswith('.pdf'):
            file_map[filename] = os.path.join(root, filename)
            count += 1
            if count % 100 == 0:
                print(f"已找到 {count} 个文件")

print(f"总共找到 {len(file_map)} 个PDF文件")

print("\n检查目标目录...")
target_files = []
for filename in os.listdir(TARGET_DIR):
    if filename.lower().endswith('.pdf'):
        target_files.append(filename)

print(f"目标目录中有 {len(target_files)} 个PDF文件")

print("\n需要处理的文件数：")
print(f"  总文件数：{len(file_map)}")
print(f"  已存在：{len(target_files)}")
print(f"  需要处理：{len(file_map) - len(target_files)}")
