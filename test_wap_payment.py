# WAP支付接口测试脚本

import requests
import json

def test_alipay_wap_pay():
    """测试支付宝WAP支付接口"""
    url = "http://127.0.0.1:5000/alipay_wap_pay"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "session_id": "test123456",
        "file_price_type": "1"
    }
    
    print("测试WAP支付接口...")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"\n✅ 支付接口调用成功！")
                print(f"支付URL: {result.get('pay_url')}")
                print(f"订单号: {result.get('out_trade_no')}")
            else:
                print(f"\n❌ 支付接口调用失败: {result.get('message')}")
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
    except Exception as e:
        print(f"\n❌ 未知异常: {str(e)}")

def test_alipay_notify():
    """测试支付宝异步通知接口"""
    url = "http://127.0.0.1:5000/alipay_notify"
    
    data = {
        "trade_status": "TRADE_SUCCESS",
        "out_trade_no": "ORD202601181230451234",
        "trade_no": "2026011200000000000123456",
        "total_amount": "3.00",
        "gmt_payment": "2026-01-18 14:30:45",
        "buyer_id": "2088102146225135",
        "buyer_logon_id": "test@alipay.com"
    }
    
    print("\n测试支付宝异步通知接口...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.text.strip() == "success":
            print(f"\n✅ 异步通知处理成功！")
        else:
            print(f"\n❌ 异步通知处理失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
    except Exception as e:
        print(f"\n❌ 未知异常: {str(e)}")

def test_alipay_return():
    """测试支付宝同步返回接口"""
    url = "http://127.0.0.1:5000/alipay_return"
    
    params = {
        "trade_status": "TRADE_SUCCESS",
        "out_trade_no": "ORD202601181230451234"
    }
    
    print("\n测试支付宝同步返回接口...")
    print(f"URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text[:500] if len(response.text) > 500 else response.text}")
        
        if response.status_code == 200:
            print(f"\n✅ 同步返回处理成功！")
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
    except Exception as e:
        print(f"\n❌ 未知异常: {str(e)}")

def test_payment_cancel():
    """测试支付取消接口"""
    url = "http://127.0.0.1:5000/payment_cancel"
    
    params = {
        "out_trade_no": "ORD202601181230451234"
    }
    
    print("\n测试支付取消接口...")
    print(f"URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500] if len(response.text) > 500 else response.text}")
        
        if response.status_code == 200:
            print(f"\n✅ 取消接口处理成功！")
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
    except Exception as e:
        print(f"\n❌ 未知异常: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("WAP支付接口测试脚本")
    print("=" * 60)
    print()
    
    while True:
        print("\n请选择测试项目：")
        print("1. 测试WAP支付接口 (/alipay_wap_pay)")
        print("2. 测试异步通知接口 (/alipay_notify)")
        print("3. 测试同步返回接口 (/alipay_return)")
        print("4. 测试支付取消接口 (/payment_cancel)")
        print("0. 退出")
        print()
        
        choice = input("请输入选项 (0-4): ")
        
        if choice == "1":
            test_alipay_wap_pay()
        elif choice == "2":
            test_alipay_notify()
        elif choice == "3":
            test_alipay_return()
        elif choice == "4":
            test_alipay_return()
        elif choice == "0":
            print("\n退出测试...")
            break
        else:
            print("\n无效选项，请重新选择")
        
        print("\n" + "=" * 60)
        print()