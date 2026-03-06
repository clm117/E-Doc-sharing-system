import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from flask import request as flask_request
from werkzeug.wrappers import Response


def handler(event, context=None):
    """Vercel Serverless函数入口"""
    # 构建Flask请求对象
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    query_string = event.get('queryStringParameters', {})
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # 处理请求
    with app.test_request_context(
        path=path,
        method=method,
        data=body,
        query_string=query_string,
        headers=headers
    ):
        # 处理请求
        response = app.full_dispatch_request()
        
        # 构建响应
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
