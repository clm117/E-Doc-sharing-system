import json

def handler(request):
    # 读取并返回mobile_payment_simple.html内容
    try:
        with open('templates/payment.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        html_content = f"<html><body><h1>Mobile Payment</h1><p>Mobile payment page</p></body></html>"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }