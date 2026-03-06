# 导入必要的模块
import os  # 导入操作系统相关模块
from io import BytesIO  # 从io模块导入BytesIO，用于处理字节流
import sqlite3  # 导入sqlite3模块，用于连接SQLite数据库

# 检查并导入必要的依赖包
try:  # 尝试导入Flask和qrcode模块
    from flask import Flask, render_template, Response  # 导入Flask核心类、模板渲染函数和响应类
    import qrcode  # 导入qrcode库，用于生成二维码
except ImportError as e:  # 如果导入Flask或qrcode失败
    print(f"错误：缺少必要的依赖包 - {str(e)}")  # 打印错误信息
    print("请先运行以下命令安装依赖：")  # 提示用户安装依赖
    print("pip install flask qrcode[pil]")  # 显示安装命令
    exit(1)  # 退出程序，返回错误码1

# SQLite数据库路径
SQLITE_DB_PATH = 'docshare.db'

# 创建Flask应用实例
app = Flask(__name__)  # 实例化Flask应用，__name__表示当前模块名

# 配置日志
app.debug = True  # 设置调试模式为True，便于开发调试

# 获取数据库连接
def get_db_connection():
    """获取SQLite数据库连接"""
    try:
        return sqlite3.connect(SQLITE_DB_PATH)
    except Exception as e:
        print(f"SQLite连接失败: {str(e)}")
        return None

# 手机页面URL地址(扫描二维码后跳转的支付页面地址)
MOBILE_PAGE_URL = "https://e-doc-sharing-system.vercel.app/mobile_payment_simple"  # 设置二维码指向的简洁版手机支付页面URL，使用Vercel域名

import uuid

# 定义首页路由
@app.route('/')
def index():
    print("访问首页")
    
    from flask import request, redirect, url_for
    
    # 获取file_id参数
    file_id = request.args.get('file_id')
    
    # 获取或生成user_id（通过Cookie或IP识别）
    user_id = request.cookies.get('user_id')
    if not user_id:
        # 如果没有Cookie，生成新的user_id
        user_id = str(uuid.uuid4()).replace('-', '')[:16]
        print(f"生成新user_id: {user_id}")
    
    # 获取session_id参数，如果没有则生成新的
    session_id = request.args.get('session_id')
    
    # 检查测试模式参数
    from flask import request
    test_mode = request.args.get('test_mode')
    
    # 测试模式：如果test_mode=success，直接模拟支付成功
    if test_mode == 'success':
        print(f"测试模式：模拟支付成功，session_id: {session_id}, user_id: {user_id}")
        # 生成模拟订单编号
        import time
        import random
        mock_order_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
        return render_template('payment_success.html',
                             file_name=mock_order_no,
                             file_password='123456',
                             amount=3.00,
                             payment_time='')
    
    # 检查支付状态
    amount = 3.00
    try:
        # 连接到SQLite数据库
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
        else:
            cursor = connection.cursor()
            
            # 关键修改：查询file_id + user_id对应的待支付记录
            if file_id:
                # 查询该file_id和user_id对应的最近一条待支付记录
                query = """
                SELECT a.session_id, a.out_trade_no, a.file_encrypt_password, a.total_amount, a.trade_status, b.file_name
                FROM alipay_wap_pay_records a
                LEFT JOIN file_info b ON a.file_id = b.file_id
                WHERE a.file_id = ?
                AND a.user_id = ?
                AND a.trade_status = 'TRADE_PENDING'
                ORDER BY a.gmt_create DESC
                LIMIT 1
                """
                cursor.execute(query, (file_id, user_id))
                result = cursor.fetchone()
                
                if result:
                    # 找到待支付记录，使用该记录的session_id
                    session_id = result[0]
                    print(f"找到待支付记录，使用session_id: {session_id}, user_id: {user_id}, file_id: {file_id}")
                else:
                    # 没有找到待支付记录，生成新的session_id并创建待支付记录
                    session_id = str(uuid.uuid4()).replace('-', '')[:16]
                    print(f"没有找到待支付记录，生成新session_id: {session_id}, user_id: {user_id}, file_id: {file_id}")
                    
                    # 获取文件信息
                    cursor.execute("SELECT file_name, file_password FROM file_info WHERE file_id = ?", (file_id,))
                    file_result = cursor.fetchone()
                    if file_result:
                        file_name, file_password = file_result
                        
                        # 生成订单号
                        import time
                        import random
                        out_trade_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
                        
                        # 创建待支付记录
                        insert_sql = """
                        INSERT INTO alipay_wap_pay_records (
                            code, msg, sub_code, sub_msg, trade_no, out_trade_no, 
                            buyer_id, buyer_logon_id, seller_id, seller_email, 
                            total_amount, receipt_amount, invoice_amount, buyer_pay_amount, 
                            point_amount, refund_fee, subject, body, gmt_create, 
                            gmt_payment, gmt_refund, gmt_close, file_id, session_id, user_id,
                            file_name, file_encrypt_password, trade_status
                        ) VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """
                        cursor.execute(insert_sql, (
                            '10000', 'Success', None, None, None, out_trade_no, 
                            '2088102146225135', 'test@alipay.com', '2088101122136669', 'test_seller@alipay.com', 
                            amount, amount, amount, amount, 
                            0, None, "学习资料购买", f"购买{file_name}", time.strftime('%Y-%m-%d %H:%M:%S'), 
                            None, None, None, file_id, session_id, user_id,
                            file_name, file_password, 'TRADE_PENDING'
                        ))
                        
                        connection.commit()
                        print(f"创建待支付记录成功: {out_trade_no}, file_id: {file_id}, session_id: {session_id}, user_id: {user_id}")
            else:
                # 没有file_id，生成新的session_id
                if not session_id:
                    session_id = str(uuid.uuid4()).replace('-', '')[:16]
            
            # 查询该session_id对应的支付成功记录
            query = """
            SELECT a.out_trade_no, a.file_encrypt_password, a.total_amount
            FROM alipay_wap_pay_records a
            WHERE a.session_id = ?
            AND a.trade_status = 'TRADE_SUCCESS'
            ORDER BY a.gmt_create DESC
            LIMIT 1
            """
            cursor.execute(query, (session_id,))
            result = cursor.fetchone()
            
            if result:
                order_no, file_password, amount = result
                print(f"检测到支付成功，订单编号: {order_no}, session_id: {session_id}")
                
                # 关闭游标和连接
                cursor.close()
                connection.close()
                
                # 如果支付成功，重定向到payment_success.html
                return render_template('payment_success.html',
                                     file_name=order_no,
                                     file_password=file_password,
                                     amount=amount,
                                     payment_time='')
            
            # 关闭游标和连接
            cursor.close()
            connection.close()
    except Exception as db_e:
        print(f"检查支付状态失败: {str(db_e)}")
    
    # 渲染首页模板，传递session_id、amount、file_id和user_id
    response = app.make_response(render_template('index.html', session_id=session_id, amount=amount, file_id=file_id))
    
    # 设置user_id到Cookie
    response.set_cookie('user_id', user_id, max_age=30*24*60*60)  # 30天过期
    
    return response

# 定义支付页面路由
@app.route('/payment')  # 装饰器，定义/payment路径路由
def payment():
    print("访问支付页面")  # 打印访问日志
    
    from flask import request
    
    # 默认金额
    amount = 99.00  # 默认金额为99.00元
    
    # 获取文件ID或价格类型参数
    file_id = request.args.get('file_id')
    file_price_type = request.args.get('file_price_type', '1')
    
    # 从payment_config表获取金额
    try:
        # 连接到SQLite数据库
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
        else:
            cursor = connection.cursor()
            
            if file_id:  # 如果有file_id参数，先获取文件的价格类型
                cursor.execute("SELECT FILE_PRICE_TYPE FROM file_info WHERE FILE_ID = ?", (file_id,))
                file_type_result = cursor.fetchone()
                if file_type_result:
                    file_price_type = file_type_result[0]
                    print(f"从file_info表获取文件价格类型: {file_price_type}")
            
            # 根据价格类型查询对应的金额
            query = "SELECT amount FROM payment_config WHERE status = 'Y' AND PRICE_TYPE = ?"
            cursor.execute(query, (file_price_type,))
            result = cursor.fetchone()
            
            if result and result[0]:  # 如果查询到了有效的amount
                amount = result[0]  # 使用数据库中的金额
                print(f"从payment_config表获取金额: {amount} (价格类型: {file_price_type})" )  # 打印日志
            
            # 关闭游标和连接
            cursor.close()
            connection.close()
    except Exception as db_e:
        print(f"从payment_config表读取amount失败，使用默认金额: {str(db_e)}")  # 打印数据库错误日志
    
    # 渲染支付页面模板，并传递金额参数
    return render_template('payment.html', amount=amount)  # 返回渲染后的payment.html模板

# 定义手机支付页面路由
@app.route('/mobile_payment')  # 装饰器，定义/mobile_payment路径路由
def mobile_payment():
    print("访问手机支付页面")  # 打印访问日志
    # 渲染手机支付页面模板
    return render_template('mobile_payment.html')  # 返回渲染后的mobile_payment.html模板

# 定义简洁版手机支付页面路由
@app.route('/mobile_payment_simple')  # 装饰器，定义/mobile_payment_simple路径路由
def mobile_payment_simple():
    print("访问简洁版手机支付页面")  # 打印访问日志
    
    from flask import request
    
    # 默认金额
    amount = 3.00
    
    # 获取文件ID或价格类型参数
    file_id = request.args.get('file_id')
    file_price_type = request.args.get('file_price_type', '1')
    
    # 从payment_config表获取金额
    try:
        # 连接到SQLite数据库
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
        else:
            cursor = connection.cursor()
            
            if file_id:  # 如果有file_id参数，先获取文件的价格类型
                cursor.execute("SELECT FILE_PRICE_TYPE FROM file_info WHERE FILE_ID = ?", (file_id,))
                file_type_result = cursor.fetchone()
                if file_type_result:
                    file_price_type = file_type_result[0]
                    print(f"从file_info表获取文件价格类型: {file_price_type}")
            
            # 根据价格类型查询对应的金额
            query = "SELECT amount FROM payment_config WHERE status = 'Y' AND PRICE_TYPE = ?"
            cursor.execute(query, (file_price_type,))
            result = cursor.fetchone()
            
            if result and result[0]:  # 如果查询到了有效的amount
                amount = result[0]  # 使用数据库中的金额
                print(f"从payment_config表获取金额: {amount} (价格类型: {file_price_type})" )  # 打印日志
            
            # 关闭游标和连接
            cursor.close()
            connection.close()
    except Exception as db_e:
        print(f"从payment_config表读取amount失败，使用默认金额: {str(db_e)}")  # 打印数据库错误日志
    
    # 渲染简洁版手机支付页面模板，并传递金额参数
    return render_template('mobile_payment_simple.html', amount=amount)  # 返回渲染后的mobile_payment_simple.html模板

# 定义支付初始化路由
@app.route('/initiate_payment')
def initiate_payment():
    print("初始化支付流程")  # 打印日志
    
    from flask import request
    
    # 获取session_id参数
    session_id = request.args.get('session_id', '')
    
    if not session_id:
        return "缺少必要的session_id参数", 400
    
    # 默认金额
    amount = 3.00
    
    # 获取文件ID或价格类型参数
    file_id = request.args.get('file_id')
    file_price_type = request.args.get('file_price_type', '1')
    
    # 从payment_config表获取金额
    try:
        # 连接到SQLite数据库
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
            return "数据库不可用", 500
        else:
            cursor = connection.cursor()
            
            if file_id:  # 如果有file_id参数，先获取文件的价格类型
                cursor.execute("SELECT FILE_PRICE_TYPE FROM file_info WHERE FILE_ID = ?", (file_id,))
                file_type_result = cursor.fetchone()
                if file_type_result:
                    file_price_type = file_type_result[0]
                    print(f"从file_info表获取文件价格类型: {file_price_type}")
            
            # 根据价格类型查询对应的金额
            query = "SELECT amount FROM payment_config WHERE status = 'Y' AND PRICE_TYPE = ?"
            cursor.execute(query, (file_price_type,))
            result = cursor.fetchone()
            
            if result and result[0]:  # 如果查询到了有效的amount
                amount = result[0]  # 使用数据库中的金额
                print(f"从payment_config表获取金额: {amount} (价格类型: {file_price_type})" )  # 打印日志
            
            # 生成随机订单号
            import random
            import time
            out_trade_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
            
            # 优先使用传递过来的file_id参数，如果没有则随机获取一个
            file_result = None
            if file_id:  # 如果有传递file_id参数
                cursor.execute("SELECT file_id, file_name, file_password FROM file_info WHERE file_id = ?", (file_id,))
                file_result = cursor.fetchone()
                if file_result:
                    file_id, file_name, file_password = file_result
                    print(f"使用传递的文件: {file_id}, 文件名: {file_name}")
            
            # 如果没有传递file_id参数或传递的file_id不存在，则随机获取一个
            if not file_result:
                cursor.execute("SELECT file_id, file_name, file_password FROM file_info ORDER BY RANDOM() LIMIT 1")
                file_result = cursor.fetchone()
                if file_result:
                    file_id, file_name, file_password = file_result
                    print(f"随机选择文件: {file_id}, 文件名: {file_name}")
            
            if file_result:
                # 模拟调用支付宝接口alipay.trade.wap.pay
                # 实际项目中，这里应该调用支付宝SDK的接口
                # 这里我们简化处理，直接写入交易记录
                
                # 插入交易记录到alipay_wap_pay_records表
                insert_sql = """
                INSERT INTO alipay_wap_pay_records (
                    code, msg, sub_code, sub_msg, trade_no, out_trade_no, 
                    buyer_id, buyer_logon_id, seller_id, seller_email, 
                    total_amount, receipt_amount, invoice_amount, buyer_pay_amount, 
                    point_amount, refund_fee, subject, body, gmt_create, 
                    gmt_payment, gmt_refund, gmt_close, file_id, session_id,
                    file_name, file_encrypt_password
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """
                
                # 模拟支付宝交易号
                trade_no = f"20260112{random.randint(1000000000000000000, 9999999999999999999)}"
                
                # 执行插入
                cursor.execute(insert_sql, (
                    '10000', 'Success', None, None, trade_no, out_trade_no, 
                    '2088102146225135', 'test@alipay.com', '2088101122136669', 'test_seller@alipay.com', 
                    amount, amount, amount, amount, 
                    0, None, "学习资料购买", f"购买{file_name}", time.strftime('%Y-%m-%d %H:%M:%S'), 
                    time.strftime('%Y-%m-%d %H:%M:%S'), None, None, file_id, session_id,
                    file_name, file_password
                ))
                
                # 提交事务
                connection.commit()
                
                print(f"交易记录写入成功，trade_no: {trade_no}, out_trade_no: {out_trade_no}, session_id: {session_id}")
                
                # 关闭游标和连接
                cursor.close()
                connection.close()
                
                # 跳转到支付成功页面
                return render_template('payment_success.html',
                                     file_name=out_trade_no,
                                     file_password=file_password,
                                     amount=amount,
                                     payment_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            else:
                cursor.close()
                connection.close()
                return "未找到有效的文件信息", 404
            
    except Exception as db_e:
        print(f"支付初始化失败: {str(db_e)}")  # 打印数据库错误日志
        return f"支付初始化失败: {str(db_e)}", 500

# 定义二维码生成路由
@app.route('/qrcode')  # 装饰器，定义/qrcode路径路由
def generate_qrcode():
    try:  # 尝试生成二维码
        from flask import request
        
        # 获取session_id和file_id参数
        session_id = request.args.get('session_id', '')
        file_id = request.args.get('file_id')
        
        if not session_id:
            print("缺少session_id参数，无法生成支付二维码")
            return Response("缺少session_id参数", status=400)
        
        # 生成带session_id、file_id的支付页面URL
        # 使用中间页面，避免微信直接拦截支付宝链接
        pay_url = f"https://e-doc-sharing-system.vercel.app/mobile_payment_simple?session_id={session_id}"
        if file_id:
            pay_url += f"&file_id={file_id}"
        
        print(f"生成二维码，指向支付页面URL: {pay_url}")  # 打印生成日志
        
        # 创建二维码对象，设置参数
        qr = qrcode.QRCode(
            version=1,                                  # 二维码版本(1-40)，1表示最小版本
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 纠错级别(L:7%)
            box_size=10,                                 # 每个方块的像素大小
            border=4,                                    # 边框的方块数(最小值为4)
        )
        # 向二维码中添加数据(支付页面URL)
        qr.add_data(pay_url)  # 将支付页面URL添加到二维码数据中
        # 调整二维码大小以适应数据
        qr.make(fit=True)  # 调整二维码大小以适应数据量
        
        # 创建二维码图片对象，设置颜色
        img = qr.make_image(fill_color="black", back_color="white")  # 创建图片对象，设置前景色为黑色，背景色为白色
        
        # 创建字节流缓冲区
        buffer = BytesIO()  # 创建BytesIO对象，用于存储图片数据
        # 将二维码图片保存到缓冲区，格式为PNG
        img.save(buffer, format='PNG')  # 将图片保存到缓冲区，格式为PNG
        # 将缓冲区指针移到起始位置
        buffer.seek(0)  # 将缓冲区指针重置到起始位置，以便读取数据
        
        print("二维码生成成功")  # 打印成功日志
        # 返回图片响应，MIME类型为image/png
        return Response(buffer.getvalue(), mimetype='image/png')  # 返回图片响应
    except Exception as e:  # 如果生成过程中出现异常
        print(f"二维码生成失败: {str(e)}")  # 打印失败日志
        # 如果生成失败，返回错误信息
        return Response("二维码生成失败", status=500)  # 返回500错误响应

# 定义支付状态检查路由
@app.route('/check_payment_status')  # 装饰器，定义/check_payment_status路径路由
def check_payment_status():
    from flask import request, jsonify
    
    # 获取session_id参数
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'message': '缺少session_id参数'}), 400
    
    # 获取file_id参数（可选）
    file_id = request.args.get('file_id')
    
    try:  # 尝试连接数据库并查询支付状态
        # 连接到数据库
        connection = get_db_connection()  # 使用配置字典连接数据库
        if not connection:
            print("无法连接数据库")
            return jsonify({'success': False, 'message': '数据库不可用'}), 500
        
        cursor = connection.cursor()  # 创建游标，用于执行SQL语句
        
        # 查询该session_id对应的支付记录
        if file_id:
            query = """
            SELECT a.out_trade_no, a.file_encrypt_password, a.total_amount, b.file_name
            FROM alipay_wap_pay_records a
            LEFT JOIN file_info b ON a.file_id = b.file_id
            WHERE a.session_id = ?
            AND a.file_id = ?
            AND a.trade_status = 'TRADE_SUCCESS'
            ORDER BY a.gmt_create DESC
            LIMIT 1
            """
            cursor.execute(query, (session_id, file_id))
        else:
            query = """
            SELECT a.out_trade_no, a.file_encrypt_password, a.total_amount, b.file_name
            FROM alipay_wap_pay_records a
            LEFT JOIN file_info b ON a.file_id = b.file_id
            WHERE a.session_id = ?
            AND a.trade_status = 'TRADE_SUCCESS'
            ORDER BY a.gmt_create DESC
            LIMIT 1
            """
            cursor.execute(query, (session_id,))
        
        result = cursor.fetchone()
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
        
        if result:  # 如果查询到支付成功记录
            order_no, file_password, amount, file_name = result
            print(f"检测到支付成功，订单编号: {order_no}, session_id: {session_id}")
            
            # 返回JSON响应，指示支付成功并提供文件信息
            return jsonify({'success': True, 'message': '支付成功', 'file_name': file_name or order_no, 'file_password': file_password, 'amount': amount}), 200
        else:  # 如果没有查询到记录
            # 返回JSON响应，指示支付尚未完成
            return jsonify({'success': False, 'message': '支付尚未完成'}), 200
            
    except Exception as e:  # 处理任何异常
        print(f"查询支付状态失败: {str(e)}")  # 打印错误日志
        # 返回JSON响应，指示查询失败
        return jsonify({'success': False, 'message': f'查询支付状态失败: {str(e)}'}), 500

# 定义支付宝WAP支付接口路由
@app.route('/alipay_wap_pay', methods=['POST'])
def alipay_wap_pay():
    """
    支付宝WAP支付接口
    前端调用此接口，返回支付宝支付页面URL
    """
    from flask import request, jsonify
    
    print("收到支付宝WAP支付请求")
    
    # 1. 获取请求参数
    data = request.get_json()
    session_id = data.get('session_id')
    file_id = data.get('file_id')
    file_price_type = data.get('file_price_type', '1')
    
    if not session_id:
        print("缺少session_id参数")
        return jsonify({'success': False, 'message': '缺少session_id参数'}), 400
    
    # 2. 从payment_config表获取金额
    amount = 3.00
    file_name = '学习资料'
    file_password = 'default_password'
    
    # 3. 生成订单号
    import time
    import random
    import json
    out_trade_no = f"ORD{int(time.time() * 1000)}{random.randint(1000, 9999)}"
    trade_no = f"20260112{random.randint(1000000000000000000, 9999999999999999999)}"
    
    try:
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
        else:
            cursor = connection.cursor()
            
            # 查询金额
            query = "SELECT amount FROM payment_config WHERE status = 'Y' AND PRICE_TYPE = ?"
            cursor.execute(query, (file_price_type,))
            result = cursor.fetchone()
            if result and result[0]:
                amount = result[0]
                print(f"从payment_config表获取金额: {amount} (价格类型: {file_price_type})")
            
            # 获取文件信息
            if file_id:
                cursor.execute("SELECT file_name, file_password FROM file_info WHERE file_id = ?", (file_id,))
                file_result = cursor.fetchone()
                if file_result:
                    file_name, file_password = file_result
                    print(f"使用传递的文件: {file_id}, 文件名: {file_name}")
            else:
                # 随机获取一个文件
                cursor.execute("SELECT file_name, file_password FROM file_info ORDER BY RANDOM() LIMIT 1")
                file_result = cursor.fetchone()
                if file_result:
                    file_name, file_password = file_result
                    print(f"随机选择文件: {file_id}, 文件名: {file_name}")
            
            # 写入交易记录（修改：在生成订单时就写入file_id并设置TRADE_PENDING状态）
            insert_sql = """
            INSERT INTO alipay_wap_pay_records (
                code, msg, sub_code, sub_msg, trade_no, out_trade_no, 
                buyer_id, buyer_logon_id, seller_id, seller_email, 
                total_amount, receipt_amount, invoice_amount, buyer_pay_amount, 
                point_amount, refund_fee, subject, body, gmt_create, 
                gmt_payment, gmt_refund, gmt_close, file_id, session_id,
                file_name, file_encrypt_password, trade_status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """
            
            cursor.execute(insert_sql, (
                '10000', 'Success', None, None, trade_no, out_trade_no, 
                '2088102146225135', 'test@alipay.com', '2088101122136669', 'test_seller@alipay.com', 
                amount, amount, amount, amount, 
                0, None, '学习资料购买', '购买学习资料', time.strftime('%Y-%m-%d %H:%M:%S'), 
                None, None, None, file_id, session_id,
                file_name, file_password, 'TRADE_PENDING'
            ))
            
            connection.commit()
            
            print(f"订单生成并写入成功: {out_trade_no}, file_id: {file_id}, session_id: {session_id}, 状态: TRADE_PENDING")
            
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"数据库查询失败: {str(e)}")
    
    # 4. 准备passback_params（关键：将session_id和file_id传递给支付宝，不再上传密码）
    passback_params = {
        'session_id': session_id,
        'file_id': file_id,
        'file_name': file_name
    }
    print(f"准备passback_params: {passback_params}")
    
    # 5. 模拟调用支付宝WAP支付接口
    # 实际项目中，这里应该调用支付宝SDK的alipay.trade.wap.pay接口
    # 示例代码：
    # from alipay import AliPay
    # alipay = AliPay(appid="您的应用ID", ...)
    # order_string = alipay.api_alipay_trade_wap_pay(
    #     out_trade_no=out_trade_no,
    #     total_amount=amount,
    #     subject="学习资料购买",
    #     body=f"购买{file_name}",
    #     product_code="QUICK_WAP_WAY",
    #     passback_params=json.dumps(passback_params)  # 关键：传递passback_params
    # )
    
    print(f"生成订单号: {out_trade_no}, 金额: {amount}, 文件: {file_name}")
    
    # 6. 返回支付URL（模拟）
    # 实际应该调用支付宝SDK获取真实的支付URL
    # 这里为了演示，使用支付宝官方的wap支付接口
    import urllib.parse
    
    # 构建符合支付宝规范的wap支付URL
    # 使用支付宝官方的wap支付接口
    biz_content = {
        'out_trade_no': out_trade_no,
        'total_amount': str(amount),
        'subject': '学习资料购买',
        'product_code': 'QUICK_WAP_WAY',
        'passback_params': json.dumps(passback_params)
    }
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # 构建支付URL
    pay_url = f"https://openapi.alipay.com/gateway.do?method=alipay.trade.wap.pay&app_id=2088101122136669&charset=UTF-8&sign_type=RSA2&timestamp={urllib.parse.quote(timestamp)}&version=1.0&biz_content={urllib.parse.quote(json.dumps(biz_content))}"
    
    return jsonify({
        'success': True,
        'pay_url': pay_url,
        'out_trade_no': out_trade_no,
        'message': '支付初始化成功'
    }), 200

# 定义支付宝异步通知路由
@app.route('/alipay_notify', methods=['POST'])
def alipay_notify():
    """
    支付宝异步通知接口
    支付宝在支付成功后会异步调用此接口
    """
    from flask import request
    
    print("收到支付宝异步通知")
    
    # 1. 获取支付宝POST参数
    params = request.form.to_dict()
    
    # 2. 验证签名（实际项目中需要验证）
    # 这里简化处理，直接返回success
    print(f"收到通知参数: {params}")
    
    # 3. 获取交易参数
    trade_status = params.get('trade_status')
    out_trade_no = params.get('out_trade_no')
    trade_no = params.get('trade_no')
    total_amount = params.get('total_amount')
    gmt_payment = params.get('gmt_payment')
    buyer_id = params.get('buyer_id', '')
    buyer_logon_id = params.get('buyer_logon_id', '')
    
    # 4. 关键：获取自定义业务参数
    passback_params_str = params.get('passback_params')
    passback_params = {}
    
    if passback_params_str:
        try:
            # 解析JSON字符串
            passback_params = json.loads(passback_params_str)
            print(f"获取到自定义参数: {passback_params}")
        except Exception as e:
            print(f"解析passback_params失败: {str(e)}")
            # 尝试修复格式（添加外层花括号）
            try:
                fixed_params = "{" + passback_params_str + "}"
                passback_params = json.loads(fixed_params)
                print(f"修复后获取到自定义参数: {passback_params}")
            except Exception as e2:
                print(f"修复passback_params失败: {str(e2)}")
    
    # 从自定义参数中提取业务信息
    session_id = passback_params.get('session_id')
    file_id = passback_params.get('file_id')
    file_name = passback_params.get('file_name')
    file_password = passback_params.get('file_password')
    
    print(f"交易状态: {trade_status}, 订单号: {out_trade_no}, session_id: {session_id}, file_id: {file_id}")
    
    # 4. 更新交易记录
    try:
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
        else:
            cursor = connection.cursor()
            
            # 检查订单是否存在
            cursor.execute("SELECT COUNT(*), trade_status FROM alipay_wap_pay_records WHERE out_trade_no = ?", (out_trade_no,))
            result = cursor.fetchone()
            count = result[0]
            current_status = result[1] if len(result) > 1 else None
            
            if count == 0:
                print("订单不存在，创建新记录")
                # 创建新记录（使用从passback_params获取的session_id和file_id）
                insert_sql = """
                INSERT INTO alipay_wap_pay_records (
                    code, msg, sub_code, sub_msg, trade_no, out_trade_no, 
                    buyer_id, buyer_logon_id, seller_id, seller_email, 
                    total_amount, receipt_amount, invoice_amount, buyer_pay_amount, 
                    point_amount, refund_fee, subject, body, gmt_create, 
                    gmt_payment, gmt_refund, gmt_close, file_id, session_id,
                    file_name, file_encrypt_password, trade_status
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """
                
                cursor.execute(insert_sql, (
                    '10000', 'Success', None, None, trade_no, out_trade_no, 
                    buyer_id, buyer_logon_id, '2088101122136669', 'test_seller@alipay.com', 
                    total_amount, total_amount, total_amount, total_amount, 
                    0, None, '学习资料购买', '购买学习资料', time.strftime('%Y-%m-%d %H:%M:%S'), 
                    gmt_payment, None, None, file_id, session_id,
                    file_name, file_password, 'TRADE_SUCCESS'
                ))
            else:
                print("订单已存在，检查状态")
                # 关键修改：只更新TRADE_SUCCESS状态的订单
                if trade_status == 'TRADE_SUCCESS':
                    # 验证订单状态是否已经是TRADE_SUCCESS
                    if current_status != 'TRADE_SUCCESS':
                        # 更新为TRADE_SUCCESS
                        update_sql = """
                        UPDATE alipay_wap_pay_records 
                        SET trade_status = ?, 
                            trade_no = ?, 
                            gmt_payment = ?, 
                            buyer_id = ?, 
                            buyer_logon_id = ?, 
                            total_amount = ?, 
                            receipt_amount = ?, 
                            buyer_pay_amount = ? 
                        WHERE out_trade_no = ?
                        """
                        
                        cursor.execute(update_sql, (
                            'TRADE_SUCCESS',
                            trade_no,
                            gmt_payment,
                            buyer_id,
                            buyer_logon_id,
                            total_amount,
                            total_amount,
                            total_amount,
                            out_trade_no
                        ))
                        
                        print(f"订单状态更新为TRADE_SUCCESS: {out_trade_no}")
                    else:
                        print(f"订单状态已经是TRADE_SUCCESS，跳过更新: {out_trade_no}")
                else:
                    print(f"订单状态不是TRADE_SUCCESS，跳过更新: {out_trade_no}, 状态: {trade_status}")
                
            connection.commit()
            
            print(f"交易记录更新成功: {out_trade_no}")
            
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"数据库更新失败: {str(e)}")
        return 'fail'
    
    # 5. 返回success给支付宝
    return 'success'

# 定义支付宝同步返回路由
@app.route('/alipay_return')
def alipay_return():
    """
    支付宝同步返回接口
    用户在支付宝完成支付后，会跳转到此接口
    """
    from flask import request, redirect
    
    print("收到支付宝同步返回")
    
    # 1. 获取支付宝GET参数
    params = request.args.to_dict()
    
    # 2. 验证签名（实际项目中需要验证）
    # 这里简化处理，直接处理
    print(f"收到同步返回参数: {params}")
    
    # 3. 获取交易参数
    trade_status = params.get('trade_status')
    out_trade_no = params.get('out_trade_no')
    
    # 4. 关键：获取自定义业务参数
    passback_params_str = params.get('passback_params')
    passback_params = {}
    
    if passback_params_str:
        try:
            # 解析JSON字符串
            passback_params = json.loads(passback_params_str)
            print(f"获取到自定义参数: {passback_params}")
        except Exception as e:
            print(f"解析passback_params失败: {str(e)}")
    
    # 从自定义参数中提取业务信息
    request_session_id = passback_params.get('session_id')
    
    print(f"交易状态: {trade_status}, 订单号: {out_trade_no}, session_id: {request_session_id}")
    
    # 4. 查询交易记录
    try:
        connection = get_db_connection()
        if not connection:
            print("无法连接数据库")
            return render_template('error.html', message='数据库不可用')
        else:
            cursor = connection.cursor()
            
            query = """
            SELECT file_name, file_encrypt_password, total_amount, trade_status, session_id
            FROM alipay_wap_pay_records
            WHERE out_trade_no = ?
            """
            cursor.execute(query, (out_trade_no,))
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if result:
                file_name, file_password, amount, current_status, current_session_id = result
                
                # 关键修改：只有TRADE_SUCCESS状态的订单才返回文件密码
                if current_status == 'TRADE_SUCCESS':
                    # 验证session_id是否匹配（防止用户A查看用户B的订单）
                    # 使用从passback_params获取的session_id
                    if not request_session_id:
                        # 如果session_id解析失败，跳过验证
                        print("session_id解析失败，跳过验证")
                        return redirect(f'/payment_success?file_name={file_name}&file_password={file_password}&amount={amount}')
                    elif request_session_id == current_session_id:
                        # session_id匹配，返回文件密码
                        print(f"支付成功，session_id匹配: {request_session_id}")
                        return redirect(f'/payment_success?file_name={file_name}&file_password={file_password}&amount={amount}')
                    else:
                        # session_id不匹配，拒绝访问
                        print(f"支付成功，但session_id不匹配: {request_session_id} vs {current_session_id}")
                        return render_template('error.html', message='您无权查看此订单信息')
                else:
                    print(f"订单状态不是TRADE_SUCCESS: {current_status}")
                    return render_template('error.html', message=f'支付未完成: {current_status}')
            else:
                print("未找到交易记录")
                return render_template('error.html', message='未找到交易记录')
                
    except Exception as e:
        print(f"数据库查询失败: {str(e)}")
        return render_template('error.html', message='查询失败')

# 定义支付取消路由
@app.route('/payment_cancel')
def payment_cancel():
    """
    支付取消页面
    用户在支付宝点击取消支付后，会跳转到此接口
    """
    from flask import request
    import time
    
    # 获取取消的订单号
    out_trade_no = request.args.get('out_trade_no')
    
    print(f"支付取消，订单号: {out_trade_no}")
    
    # 更新交易状态
    if out_trade_no:
        try:
            connection = get_db_connection()
            if not connection:
                print("无法连接数据库")
            else:
                cursor = connection.cursor()
                
                update_sql = """
                UPDATE alipay_wap_pay_records 
                SET trade_status = 'TRADE_CLOSED', 
                    gmt_close = ? 
                WHERE out_trade_no = ?
                """
                
                cursor.execute(update_sql, (time.strftime('%Y-%m-%d %H:%M:%S'), out_trade_no))
                
                connection.commit()
                
                cursor.close()
                connection.close()
                
                print("交易状态更新为已关闭")
                
        except Exception as e:
            print(f"数据库更新失败: {str(e)}")
    
    # 返回取消页面
    return render_template('error.html', message='支付已取消')

# 定义支付成功页面路由
@app.route('/payment_success')
def payment_success():
    from flask import request
    
    # 获取URL参数
    file_name = request.args.get('file_name', '未知文件')
    file_password = request.args.get('file_password', '未知密码')
    amount = request.args.get('amount', 0.0)
    
    # 渲染支付成功页面
    return render_template('payment_success.html',
                         file_name=file_name,
                         file_password=file_password,
                         amount=float(amount),
                         payment_time='')

# 判断是否为主程序入口
if __name__ == '__main__':  # 如果当前模块是主程序
    # 启动Flask应用
    app.run(
        debug=True,            # 开启调试模式，便于开发调试
        host='0.0.0.0',        # 允许所有IP访问，便于外部设备访问
        port=5000              # 监听端口号为5000
    )  # 启动Flask应用服务器