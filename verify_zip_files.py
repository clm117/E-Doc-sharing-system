import os
import zipfile

ENCRYPTED_DIR = r"D:\Program Files (x86)\Trae CN\111code\加密文件"

test_files = [
    "[图灵程序设计丛书].C#并发编程经典实例.PDF",
    "心理学基础(王朝庄).PDF",
    "心理学无处不在 59个日常生活问题的心理学解释 布鲁克斯.PDF",
    "心理学研究方法( 第2版，王重鸣.PDF",
    "心理强大之路.PDF",
    "现代心理学原理与应用(第二版,朱宝荣等).PDF",
    "罗兰贝格－消费心理分析.PDF",
    "钱宾四先生全集 第002册 四书释义 论语文解.PDF",
    "钱宾四先生全集 第003册 论语新解.PDF",
    "钱宾四先生全集 第005册 先秦诸子系年.PDF",
    "钱宾四先生全集 第008册 两汉经学 今古文平议.PDF",
    "钱宾四先生全集 第016册 中国近三百年学术史（一）.PDF",
    "钱宾四先生全集 第026册 周公 秦汉史.PDF",
    "钱宾四先生全集 第029册 中国文化史导论 中国历史精神.PDF",
    "钱宾四先生全集 第030册 国史新论.PDF",
    "钱宾四先生全集 第033册 中国史学名着.PDF",
    "钱宾四先生全集 第042册 历史与文化论丛.PDF",
    "钱宾四先生全集 第043册 世界局势与中国文化.PDF",
]

print("检查压缩包内容...")
print("=" * 80)

for filename in test_files:
    zip_filename = filename.replace('.pdf', '.zip')
    zip_path = os.path.join(ENCRYPTED_DIR, zip_filename)
    
    print(f"\n检查：{zip_filename}")
    
    if not os.path.exists(zip_path):
        print(f"  [错误] 压缩包不存在")
        continue
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            print(f"  压缩包包含{len(file_list)}个文件：")
            for f in file_list:
                print(f"    - {f}")
    except Exception as e:
        print(f"  [错误] 无法读取压缩包：{str(e)}")

print("\n" + "=" * 80)
print("检查完成！")
print("=" * 80)
