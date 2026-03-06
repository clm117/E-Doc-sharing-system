def handler(event, context=None):
    """测试函数"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello from Vercel!'
    }
