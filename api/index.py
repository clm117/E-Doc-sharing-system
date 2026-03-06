import os

def handler(event, context=None):
    """Vercel Serverless函数入口"""
    # 获取请求路径
    path = event.get('path', '/').strip('/')
    
    # 根据路径返回不同的HTML文件
    if not path or path == 'index':
        # 返回首页
        return get_html_response('templates/index.html')
    elif path == 'payment_success':
        # 返回支付成功页面
        return get_html_response('templates/payment_success.html')
    elif path == 'mobile_payment_simple':
        # 返回移动端支付页面
        return get_html_response('templates/mobile_payment_simple.html')
    else:
        # 返回404页面
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<html><body><h1>404 Not Found</h1></body></html>'
        }

def get_html_response(file_path):
    """读取并返回HTML文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': html_content
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': f'<html><body><h1>Error</h1><p>{str(e)}</p></body></html>'
        }
