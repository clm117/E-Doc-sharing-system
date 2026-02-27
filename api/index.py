import json

def handler(request):
    # 读取并返回index.html内容
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        html_content = f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }