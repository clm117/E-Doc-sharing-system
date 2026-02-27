#!/usr/bin/env python3
import os
import PyPDF2
import requests
import re
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_decrypt.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 源目录和目标目录
SOURCE_DIR = r"D:\Program Files (x86)\Trae CN\111code\20260123\原加密文件"
DEST_DIR = r"D:\Program Files (x86)\Trae CN\111code\20260123\压缩加密文件"

# Oracle数据库连接配置
DB_CONFIG = {
    'user': 'system',               # 数据库用户名
    'password': 'oracle123',        # 数据库密码
    'dsn': 'localhost:1521/ORCLM',   # 主机名:端口/服务名
    'encoding': 'UTF-8'             # 字符编码
}

# 检查cx_Oracle模块
ORACLE_AVAILABLE = False
try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    print("警告：未安装cx_Oracle，将无法连接Oracle数据库")

# Flask服务器地址
FLASK_SERVER = "http://127.0.0.1:5000"

# 尝试的密码列表
PASSWORD_LIST = [
    "",  # 空密码
    "123456",
    "password",
    "123",
    "admin",
    "1234",
    "12345",
    "1234567",
    "12345678",
    "123456789",
    "qwerty",
    "abc123",
    "111111",
    "123123",
    "123qwe",
    "1q2w3e",
    "admin123",
    "password123",
    "test",
    "test123"
]

def get_password_from_flask():
    """
    从Flask服务器获取测试模式密码
    :return: 密码字符串
    """
    try:
        # 使用测试模式获取密码
        url = f"{FLASK_SERVER}/?test_mode=success"
        response = requests.get(url, timeout=10)
        
        # 解析HTML获取密码
        if response.status_code == 200:
            # 尝试从HTML中提取密码
            password_match = re.search(r'file_password[\s\S]*?([a-zA-Z0-9]+)', response.text)
            if password_match:
                password = password_match.group(1)
                logger.info(f"从Flask服务器获取密码成功: {password}")
                return password
            else:
                # 如果无法解析，返回默认测试密码
                logger.info("无法解析HTML，使用默认测试密码")
                return "123456"
        else:
            logger.error(f"Flask服务器请求失败: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"从Flask服务器获取密码时出错: {str(e)}")
        return None

def get_password_from_db(file_name):
    """
    从Oracle数据库的file_info表中获取密码
    :param file_name: 文件名
    :return: 密码字符串
    """
    if not ORACLE_AVAILABLE:
        logger.info("Oracle数据库不可用，无法从file_info表获取密码")
        return None
    
    # 重试机制，最多重试3次
    for retry in range(3):
        connection = None
        cursor = None
        
        try:
            # 连接到Oracle数据库
            connection = cx_Oracle.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            # 根据文件名查询密码
            cursor.execute("SELECT file_password FROM file_info WHERE file_name = :file_name", file_name=file_name)
            result = cursor.fetchone()
            
            if result:
                password = result[0]
                return password
            else:
                # 尝试使用LIKE查询，可能文件名有空格或其他差异
                cursor.execute("SELECT file_password FROM file_info WHERE file_name LIKE :file_name", file_name=f"%{file_name}%")
                result = cursor.fetchone()
                if result:
                    password = result[0]
                    logger.info(f"在file_info表中找到类似文件: {file_name}")
                    return password
                else:
                    logger.info(f"在file_info表中未找到文件: {file_name}")
                    return None
        except Exception as e:
            logger.error(f"从数据库获取密码时出错 (尝试 {retry+1}/3): {str(e)}")
            if retry >= 2:
                return None
            import time
            time.sleep(1)  # 等待1秒后重试
        finally:
            # 确保关闭连接
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if connection:
                try:
                    connection.close()
                except:
                    pass

def decrypt_pdf(input_path, output_path):
    """
    尝试解密PDF文件
    :param input_path: 输入PDF文件路径
    :param output_path: 输出PDF文件路径
    :return: 解密是否成功
    """
    # 获取文件名
    file_name = os.path.basename(input_path)
    logger.info(f"开始处理: {file_name}")
    
    try:
        # 检查文件是否存在
        if not os.path.exists(input_path):
            logger.error(f"文件不存在: {input_path}")
            return False
        
        # 检查文件大小
        if os.path.getsize(input_path) == 0:
            logger.error(f"文件为空: {file_name}")
            return False
        
        with open(input_path, 'rb') as file:
            try:
                reader = PyPDF2.PdfReader(file)
            except Exception as e:
                logger.error(f"读取PDF文件时出错: {str(e)}")
                logger.info(f"{file_name} 处理完成")
                return False
            
            try:
                # 检查PDF是否加密
                if not reader.is_encrypted:
                    logger.info(f"{file_name} 未加密，直接复制")
                    # 直接复制未加密的文件
                    writer = PyPDF2.PdfWriter()
                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    logger.info(f"{file_name} 处理完成")
                    return True
                
                # 尝试从file_info表获取密码
                db_password = get_password_from_db(file_name)
                if db_password:
                    try:
                        if reader.decrypt(db_password):
                            logger.info(f"{file_name} 解密成功，使用file_info表密码")
                            # 创建解密后的PDF
                            writer = PyPDF2.PdfWriter()
                            for page_num in range(len(reader.pages)):
                                writer.add_page(reader.pages[page_num])
                            with open(output_path, 'wb') as output_file:
                                writer.write(output_file)
                            logger.info(f"{file_name} 处理完成")
                            return True
                    except Exception as e:
                        logger.error(f"使用file_info表密码解密时出错: {str(e)}")
                
                # 尝试从Flask服务器获取密码
                flask_password = get_password_from_flask()
                if flask_password:
                    try:
                        if reader.decrypt(flask_password):
                            logger.info(f"{file_name} 解密成功，使用Flask服务器密码: {flask_password}")
                            # 创建解密后的PDF
                            writer = PyPDF2.PdfWriter()
                            for page_num in range(len(reader.pages)):
                                writer.add_page(reader.pages[page_num])
                            with open(output_path, 'wb') as output_file:
                                writer.write(output_file)
                            logger.info(f"{file_name} 处理完成")
                            return True
                    except Exception as e:
                        logger.error(f"使用Flask服务器密码解密时出错: {str(e)}")
                
                # 尝试密码列表中的密码
                for password in PASSWORD_LIST:
                    try:
                        if reader.decrypt(password):
                            logger.info(f"{file_name} 解密成功，使用密码: {password}")
                            # 创建解密后的PDF
                            writer = PyPDF2.PdfWriter()
                            for page_num in range(len(reader.pages)):
                                writer.add_page(reader.pages[page_num])
                            with open(output_path, 'wb') as output_file:
                                writer.write(output_file)
                            logger.info(f"{file_name} 处理完成")
                            return True
                    except Exception as e:
                        continue
                
                logger.warning(f"{file_name} 解密失败，尝试了所有密码")
                logger.info(f"{file_name} 处理完成")
                return False
            except Exception as e:
                logger.error(f"处理PDF文件时出错: {str(e)}")
                logger.info(f"{file_name} 处理完成")
                return False
    except Exception as e:
        logger.error(f"处理 {file_name} 时出错: {str(e)}")
        logger.info(f"{file_name} 处理完成")
        return False

def main():
    """
    主函数，遍历源目录中的所有PDF文件并尝试解密
    """
    # 确保目标目录存在
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        logger.info(f"创建目标目录: {DEST_DIR}")
    
    # 遍历源目录中的所有PDF文件
    pdf_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)
    logger.info(f"找到 {total_files} 个PDF文件")
    
    # 测试模式：只处理前20个文件
    test_mode = False
    if test_mode:
        test_files = pdf_files[:20]
        logger.info(f"测试模式：只处理前20个文件")
        
        success_count = 0
        failure_count = 0
        
        for i, pdf_file in enumerate(test_files):
            logger.info(f"\n处理第 {i+1} 个文件:")
            input_path = os.path.join(SOURCE_DIR, pdf_file)
            output_path = os.path.join(DEST_DIR, pdf_file)
            
            if decrypt_pdf(input_path, output_path):
                success_count += 1
            else:
                failure_count += 1
        
        logger.info(f"\n测试完成:")
        logger.info(f"成功: {success_count}")
        logger.info(f"失败: {failure_count}")
        logger.info(f"总计: {len(test_files)}")
    else:
        # 处理所有文件
        logger.info("开始处理所有文件...")
        
        success_count = 0
        failure_count = 0
        
        # 批量处理，每次处理50个文件
        batch_size = 50
        total_batches = (total_files + batch_size - 1) // batch_size
        
        for batch in range(total_batches):
            start_idx = batch * batch_size
            end_idx = min((batch + 1) * batch_size, total_files)
            batch_files = pdf_files[start_idx:end_idx]
            
            logger.info(f"\n处理第 {batch+1}/{total_batches} 批文件，共 {len(batch_files)} 个文件")
            
            batch_success = 0
            batch_failure = 0
            
            for i, pdf_file in enumerate(batch_files):
                file_idx = start_idx + i
                # 每处理10个文件显示一次进度
                if i % 10 == 0:
                    logger.info(f"进度: 已处理 {file_idx} 个文件，成功 {success_count} 个，失败 {failure_count} 个")
                
                input_path = os.path.join(SOURCE_DIR, pdf_file)
                output_path = os.path.join(DEST_DIR, pdf_file)
                
                if decrypt_pdf(input_path, output_path):
                    success_count += 1
                    batch_success += 1
                else:
                    failure_count += 1
                    batch_failure += 1
            
            logger.info(f"第 {batch+1}/{total_batches} 批处理完成: 成功 {batch_success} 个，失败 {batch_failure} 个")
            
            # 每处理完一批文件后休息5秒，避免数据库连接超时
            if batch < total_batches - 1:
                logger.info("休息5秒，避免数据库连接超时...")
                import time
                time.sleep(5)
        
        logger.info(f"\n所有文件处理完成:")
        logger.info(f"成功: {success_count}")
        logger.info(f"失败: {failure_count}")
        logger.info(f"总计: {total_files}")

if __name__ == "__main__":
    main()
