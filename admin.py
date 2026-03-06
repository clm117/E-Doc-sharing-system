# 后台管理系统
import os
import zipfile
import shutil
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import pyAesCrypt
import uuid

# 创建Flask应用
app = Flask(__name__)
app.debug = True

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 配置
UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = r'D:\Program Files (x86)\Trae CN\111code\加密文件路径'
PASSWORD_INFO_FILE = r'D:\Program Files (x86)\Trae CN\111code\待加密文件路径下文件 密码链接说明.txt'
ALLOWED_EXTENSIONS = {'pdf', 'zip', 'rar', '7z', 'txt'}

# 确保上传和加密文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

# 获取数据库连接
def get_db_connection():
    """获取SQLite数据库连接"""
    try:
        return sqlite3.connect(SQLITE_DB_PATH)
    except Exception as e:
        print(f"SQLite连接失败: {str(e)}")
        return None

# ==================== 后台管理界面路由 ====================

@app.route('/admin')
def admin():
    """后台管理界面首页"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 获取文件总数
        cursor.execute("SELECT COUNT(*) FROM file_info")
        file_count = cursor.fetchone()[0]
        
        # 获取支付记录数
        cursor.execute("SELECT COUNT(*) FROM alipay_wap_pay_records")
        payment_count = cursor.fetchone()[0]
        
        # 获取今日收入
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT SUM(total_amount) 
            FROM alipay_wap_pay_records 
            WHERE trade_status = 'TRADE_SUCCESS' 
            AND DATE(gmt_payment) = ?
        """, (today,))
        today_income = cursor.fetchone()[0] or 0
        
        cursor.close()
        connection.close()
        
        return render_template('admin.html', file_count=file_count, payment_count=payment_count, today_income=today_income)
    except Exception as e:
        print(f"错误: {str(e)}")
        return render_template('admin.html', file_count=0, payment_count=0, today_income=0)

@app.route('/admin/add_file', methods=['GET', 'POST'])
def admin_add_file():
    """添加文件到数据库"""
    if request.method == 'GET':
        return render_template('admin_add_file.html')
    
    if request.method == 'POST':
        try:
            # 获取表单数据
            file_name = request.form.get('file_name')
            file_path = request.form.get('file_path')
            file_author = request.form.get('file_author', '')
            standard_name = request.form.get('standard_name', '')
            search_keywords = request.form.get('search_keywords', '')
            file_tags = request.form.get('file_tags', '')
            file_isbn = request.form.get('file_isbn', '')
            file_price_type = request.form.get('file_price_type', '1')
            file_password = request.form.get('file_password', '')
            
            # 连接数据库
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # 生成唯一ID
            file_id = str(uuid.uuid4()).replace('-', '')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 插入file_info表
            insert_sql = """
            INSERT INTO file_info (
                file_id, file_name, file_path, file_author,
                standard_name, search_keywords, file_tags,
                file_isbn, file_price_type, file_password,
                create_time, update_time
            ) VALUES (
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?
            )
            """
            
            cursor.execute(insert_sql, (
                file_id, file_name, file_path, file_author,
                standard_name, search_keywords, file_tags,
                file_isbn, file_price_type, file_password,
                current_time, current_time
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': '文件添加成功'})
            
        except Exception as e:
            print(f"错误: {str(e)}")
            return jsonify({'success': False, 'message': '文件添加失败: ' + str(e)})

@app.route('/admin/encrypt_and_compress', methods=['POST'])
def admin_encrypt_and_compress():
    """加密并压缩文件"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '请选择文件'})
        
        file = request.files['file']
        password = request.form.get('password', '')
        
        if not password:
            return jsonify({'success': False, 'message': '请输入密码'})
        
        # 保存上传的文件
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # 加密文件
        encrypted_path = os.path.join(UPLOAD_FOLDER, 'encrypted_' + filename)
        encrypt_file(file_path, encrypted_path, password)
        
        # 创建压缩包
        package_name = 'encrypted_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.zip'
        package_path = os.path.join(ENCRYPTED_FOLDER, package_name)
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加加密文件
            zipf.write(encrypted_path, os.path.basename(encrypted_path))
            # 添加密码说明文件（如果存在）
            if os.path.exists(PASSWORD_INFO_FILE):
                zipf.write(PASSWORD_INFO_FILE, os.path.basename(PASSWORD_INFO_FILE))
        
        return jsonify({
            'success': True, 
            'message': '加密压缩成功',
            'package_path': package_path,
            'package_name': package_name
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': '加密压缩失败: ' + str(e)})

def encrypt_file(input_path, output_path, password):
    """加密文件"""
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(input_path, output_path, password, bufferSize)

@app.route('/admin/edit_file', methods=['GET', 'POST'])
def admin_edit_file():
    """编辑文件信息"""
    if request.method == 'GET':
        file_id = request.args.get('file_id')
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询文件信息
        cursor.execute("SELECT * FROM file_info WHERE file_id = ?", (file_id,))
        file_info = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if file_info:
            return render_template('admin_edit_file.html', file_info=file_info)
        else:
            return '文件不存在'
    
    if request.method == 'POST':
        try:
            file_id = request.form.get('file_id')
            file_name = request.form.get('file_name')
            file_author = request.form.get('file_author', '')
            standard_name = request.form.get('standard_name', '')
            search_keywords = request.form.get('search_keywords', '')
            file_tags = request.form.get('file_tags', '')
            file_isbn = request.form.get('file_isbn', '')
            file_price_type = request.form.get('file_price_type', '1')
            file_password = request.form.get('file_password', '')
            
            # 连接数据库
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # 更新file_info表
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_sql = """
            UPDATE file_info SET
                file_name = ?,
                file_author = ?,
                standard_name = ?,
                search_keywords = ?,
                file_tags = ?,
                file_isbn = ?,
                file_price_type = ?,
                file_password = ?,
                update_time = ?
            WHERE file_id = ?
            """
            
            cursor.execute(update_sql, (
                file_name,
                file_author,
                standard_name,
                search_keywords,
                file_tags,
                file_isbn,
                file_price_type,
                file_password,
                current_time,
                file_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': '文件更新成功'})
            
        except Exception as e:
            print(f"错误: {str(e)}")
            return jsonify({'success': False, 'message': '文件更新失败: ' + str(e)})

@app.route('/admin/file_list')
def admin_file_list():
    """文件列表"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询文件列表
        cursor.execute("SELECT * FROM file_info ORDER BY create_time DESC")
        files = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('admin_file_list.html', files=files)
    except Exception as e:
        print(f"错误: {str(e)}")
        return render_template('admin_file_list.html', files=[])

@app.route('/admin/generate_package', methods=['POST'])
def admin_generate_package():
    """生成压缩包"""
    try:
        # 获取参数
        file_ids = request.form.getlist('file_ids')
        package_name = request.form.get('package_name', 'package_' + datetime.now().strftime("%Y%m%d%H%M%S"))
        output_path = request.form.get('output_path', ENCRYPTED_FOLDER)
        
        # 查询选中的文件
        connection = get_db_connection()
        cursor = connection.cursor()
        
        placeholders = ','.join(['?' for _ in file_ids])
        query = "SELECT file_name, file_path, file_password FROM file_info WHERE file_id IN (" + placeholders + ")"
        cursor.execute(query, file_ids)
        files = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # 创建压缩包
        package_path = os.path.join(output_path, package_name + '.zip')
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                file_name, file_path, file_password = file
                
                # 添加文件到压缩包
                if os.path.exists(file_path):
                    zipf.write(file_path, file_name)
                    
                    # 创建文件信息文件
                    info_content = "文件名称: " + file_name + "\n"
                    info_content += "文件路径: " + file_path + "\n"
                    info_content += "文件密码: " + file_password + "\n"
                    info_content += "创建时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    zipf.writestr(file_name + '_info.txt', info_content)
        
        return jsonify({
            'success': True, 
            'message': '压缩包生成成功',
            'package_path': package_path,
            'file_count': len(files)
        })
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'message': '压缩包生成失败: ' + str(e)})

@app.route('/admin/payment_records')
def admin_payment_records():
    """支付记录查询"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询支付记录
        cursor.execute("""
            SELECT out_trade_no, file_name, total_amount, trade_status, 
                   gmt_create, gmt_payment, file_encrypt_password
            FROM alipay_wap_pay_records 
            ORDER BY gmt_create DESC
            LIMIT 100
        """)
        records = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('admin_payment_records.html', records=records)
    except Exception as e:
        print(f"错误: {str(e)}")
        return render_template('admin_payment_records.html', records=[])

@app.route('/admin/api/payment_records', methods=['GET'])
def admin_api_payment_records():
    """API: 获取支付记录"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询支付记录
        cursor.execute("""
            SELECT out_trade_no, file_name, total_amount, trade_status, 
                   gmt_create, gmt_payment, file_encrypt_password
            FROM alipay_wap_pay_records 
            ORDER BY gmt_create DESC
            LIMIT 100
        """)
        columns = [col[0] for col in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'records': records})
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'records': [], 'message': str(e)})

@app.route('/admin/payment_config', methods=['GET', 'POST'])
def admin_payment_config():
    """支付配置管理"""
    if request.method == 'GET':
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # 查询支付配置
            cursor.execute("SELECT * FROM payment_config WHERE status = 'Y' ORDER BY price_id")
            configs = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return render_template('admin_payment_config.html', configs=configs)
        except Exception as e:
            print(f"错误: {str(e)}")
            return render_template('admin_payment_config.html', configs=[])
    
    if request.method == 'POST':
        try:
            price_id = request.form.get('price_id')
            price_type = request.form.get('price_type')
            amount = request.form.get('amount')
            payment_url = request.form.get('payment_url')
            description = request.form.get('description', '')
            status = request.form.get('status', 'Y')
            
            # 连接数据库
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # 检查是新增还是修改
            cursor.execute("SELECT price_id FROM payment_config WHERE price_id = ?", (price_id,))
            existing = cursor.fetchone()
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if existing:
                # 更新配置
                update_sql = """
                UPDATE payment_config SET
                    price_type = ?,
                    amount = ?,
                    payment_url = ?,
                    description = ?,
                    status = ?,
                    update_time = ?
                WHERE price_id = ?
                """
                cursor.execute(update_sql, (
                    price_type,
                    amount,
                    payment_url,
                    description,
                    status,
                    current_time,
                    price_id
                ))
            else:
                # 新增配置
                insert_sql = """
                INSERT INTO payment_config (
                    price_id, price_type, amount, payment_url,
                    description, status, create_time, update_time
                ) VALUES (
                    ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
                """
                cursor.execute(insert_sql, (
                    price_id,
                    price_type,
                    amount,
                    payment_url,
                    description,
                    status,
                    current_time,
                    current_time
                ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': '配置保存成功'})
            
        except Exception as e:
            print(f"错误: {str(e)}")
            return jsonify({'success': False, 'message': '配置保存失败: ' + str(e)})

@app.route('/admin/api/payment_config', methods=['GET'])
def admin_api_payment_config():
    """API: 获取支付配置"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查询支付配置
        cursor.execute("SELECT * FROM payment_config ORDER BY price_id")
        columns = [col[0] for col in cursor.description]
        configs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'configs': configs})
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'configs': [], 'message': str(e)})

@app.route('/admin/api/files', methods=['GET'])
def admin_api_files():
    """API: 获取所有文件列表（分页）"""
    try:
        page = int(request.args.get('page', 1))
        per_page = 50
        offset = (page - 1) * per_page
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) FROM file_info")
        total = cursor.fetchone()[0]
        
        # 查询文件列表（分页）
        cursor.execute("""
            SELECT * FROM file_info 
            ORDER BY create_time DESC
            LIMIT ? OFFSET ?
        """, (per_page, offset))
        
        columns = [col[0] for col in cursor.description]
        files = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True, 
            'files': files,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'files': [], 'message': str(e)})

@app.route('/admin/api/search_files', methods=['GET'])
def admin_api_search_files():
    """API: 搜索文件（分页）"""
    keyword = request.args.get('keyword', '')
    file_type = request.args.get('file_type', '')
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # 构建查询条件
    conditions = []
    params = []
    
    if keyword:
        conditions.append("(file_name LIKE ? OR file_author LIKE ? OR search_keywords LIKE ?)")
        params.extend(['%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'])
    
    if file_type:
        conditions.append("file_price_type = ?")
        params.append(file_type)
    
    where_clause = ' AND '.join(conditions) if conditions else '1=1'
    
    # 获取总数
    count_query = "SELECT COUNT(*) FROM file_info WHERE " + where_clause
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # 查询文件列表（分页）
    query = """
        SELECT * FROM file_info 
        WHERE """ + where_clause + """
        ORDER BY create_time DESC
        LIMIT ? OFFSET ?
    """
    params.extend([per_page, offset])
    
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    files = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    
    return jsonify({
        'success': True, 
        'files': files,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/admin/api/delete_file', methods=['POST'])
def admin_api_delete_file():
    """API: 删除文件"""
    file_id = request.json.get('file_id')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # 删除文件记录
        cursor.execute("DELETE FROM file_info WHERE file_id = ?", (file_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': '文件删除成功'})
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'message': '文件删除失败: ' + str(e)})

@app.route('/admin/initialize_data', methods=['POST'])
def admin_initialize_data():
    """初始化数据"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查是否已初始化
        cursor.execute("SELECT COUNT(*) FROM payment_config WHERE price_id = '1'")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 初始化支付配置
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
                INSERT INTO payment_config (
                    price_id, price_type, amount, payment_url,
                    description, status, create_time, update_time
                ) VALUES (
                    '1', '标准版', 3.00, '/payment',
                    '标准版支付配置', 'Y', ?, ?
                )
            """, (current_time, current_time))
            
            cursor.execute("""
                INSERT INTO payment_config (
                    price_id, price_type, amount, payment_url,
                    description, status, create_time, update_time
                ) VALUES (
                    '2', '高级版', 5.00, '/payment',
                    '高级版支付配置', 'Y', ?, ?
                )
            """, (current_time, current_time))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': '数据初始化成功'})
        else:
            return jsonify({'success': False, 'message': '数据已初始化'})
            
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({'success': False, 'message': '数据初始化失败: ' + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
