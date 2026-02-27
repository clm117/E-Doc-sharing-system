import cx_Oracle
import os
import shutil

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',
    'password': 'oracle123',
    'dsn': 'localhost:1521/ORCLM',
    'encoding': 'UTF-8'
}

# 源目录和目标目录
SOURCE_DIR = r"D:\2.enjoy\2.学习资料"
TARGET_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

def find_all_pdfs(directory):
    """递归查找目录下所有PDF文件"""
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(root, filename)
                pdf_files.append(full_path)
    return pdf_files

def copy_pdf_files_recursive():
    try:
        print("正在连接数据库...")
        connection = cx_Oracle.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("开始递归复制PDF文件...")
        print("=" * 80)
        
        # 1. 查询file_info表中的所有文件名
        print("\n1. 查询file_info表中的所有文件名...")
        cursor.execute("""
            SELECT file_name
            FROM file_info
            WHERE file_name IS NOT NULL
        """)
        file_names = set()
        for row in cursor.fetchall():
            file_names.add(row[0])
        print(f"✅ 查询到{len(file_names)}个文件名")
        
        # 2. 递归查找源目录下的所有PDF文件
        print(f"\n2. 递归查找源目录下的所有PDF文件...")
        source_files = find_all_pdfs(SOURCE_DIR)
        print(f"✅ 找到{len(source_files)}个PDF文件")
        
        # 3. 检查源目录是否存在
        print(f"\n3. 检查源目录：{SOURCE_DIR}")
        if not os.path.exists(SOURCE_DIR):
            print(f"❌ 源目录不存在：{SOURCE_DIR}")
            cursor.close()
            connection.close()
            return
        print(f"✅ 源目录存在")
        
        # 4. 检查目标目录是否存在
        print(f"\n4. 检查目标目录：{TARGET_DIR}")
        if not os.path.exists(TARGET_DIR):
            print(f"❌ 目标目录不存在：{TARGET_DIR}")
            cursor.close()
            connection.close()
            return
        print(f"✅ 目标目录存在")
        
        # 5. 复制符合条件的PDF文件
        print(f"\n5. 开始复制符合条件的PDF文件...")
        success_count = 0
        skipped_count = 0
        not_in_db_count = 0
        failed_count = 0
        
        for i, source_path in enumerate(source_files):
            filename = os.path.basename(source_path)
            target_path = os.path.join(TARGET_DIR, filename)
            
            # 检查文件名是否在file_info表中
            if filename not in file_names:
                not_in_db_count += 1
                if not_in_db_count <= 10:
                    print(f"⏭️  [{i+1}/{len(source_files)}] 不在数据库中，跳过：{filename}")
                continue
            
            try:
                # 检查目标文件是否已存在
                if os.path.exists(target_path):
                    # 比较文件大小，如果相同则跳过
                    source_size = os.path.getsize(source_path)
                    target_size = os.path.getsize(target_path)
                    
                    if source_size == target_size:
                        skipped_count += 1
                        if (i + 1) % 100 == 0:
                            print(f"⏭️  已处理{i+1}/{len(source_files)}个文件...")
                        continue
                    else:
                        # 删除旧文件
                        os.remove(target_path)
                        print(f"🗑️  [{i+1}/{len(source_files)}] 删除旧文件：{filename}")
                
                # 复制文件
                shutil.copy2(source_path, target_path)
                success_count += 1
                if (i + 1) % 100 == 0:
                    print(f"✅ 已处理{i+1}/{len(source_files)}个文件...")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ [{i+1}/{len(source_files)}] 复制失败：{filename}, 错误：{str(e)[:100]}")
        
        # 6. 统计结果
        print("\n" + "=" * 80)
        print("复制统计：")
        print(f"  - 源PDF文件数：{len(source_files)}")
        print(f"  - 成功复制：{success_count}个")
        print(f"  - 跳过（已存在）：{skipped_count}个")
        print(f"  - 不在数据库中：{not_in_db_count}个")
        print(f"  - 复制失败：{failed_count}个")
        print("=" * 80)
        
        # 7. 验证目标目录
        print("\n7. 验证目标目录...")
        target_files = find_all_pdfs(TARGET_DIR)
        print(f"✅ 目标目录现在有{len(target_files)}个PDF文件")
        
        cursor.close()
        connection.close()
        print("\n数据库连接已关闭")
        print("复制完成！")
        
    except Exception as e:
        print(f"❌ 复制失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 80)
    print("开始递归复制PDF文件")
    print("=" * 80)
    copy_pdf_files_recursive()
    print("=" * 80)
    print("执行完成！")
    print("=" * 80)
