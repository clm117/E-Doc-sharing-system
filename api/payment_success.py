import json

def handler(request):
    # 读取并返回payment_success.html内容
    try:
        with open('templates/payment.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        html_content = f"<html><body><h1>Payment Success</h1><p>Payment processed successfully!</p></body></html>"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }