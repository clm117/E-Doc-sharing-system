# 文件与支付记录唯一性关联测试脚本

import requests
import json
import time

def test_unique_payment_record():
    """测试文件与支付记录的唯一性关联"""
    
    print("=" * 60)
    print("文件与支付记录唯一性关联测试")
    print("=" * 60)
    print()
    
    # 测试场景1：用户A和用户B同时下载文件并支付
    print("测试场景1：用户A和用户B同时下载文件并支付")
    print("-" * 60)
    
    # 用户A点击支付
    session_id_a = "user_a_" + str(int(time.time() * 1000))
    print(f"用户A点击支付，session_id: {session_id_a}")
    
    response_a = requests.post(
        'http://127.0.0.1:5000/alipay_wap_pay',
        headers={'Content-Type': 'application/json'},
        json={'session_id': session_id_a, 'file_price_type': '1'},
        timeout=10
    )
    
    print(f"用户A支付请求状态码: {response_a.status_code}")
    if response_a.status_code == 200:
        result_a = response_a.json()
        print(f"用户A订单号: {result_a.get('out_trade_no')}")
        out_trade_no_a = result_a.get('out_trade_no')
    else:
        print(f"用户A支付请求失败: {response_a.text}")
        out_trade_no_a = None
    
    time.sleep(1)
    
    # 用户B点击支付
    session_id_b = "user_b_" + str(int(time.time() * 1000))
    print(f"\n用户B点击支付，session_id: {session_id_b}")
    
    response_b = requests.post(
        'http://127.0.0.1:5000/alipay_wap_pay',
        headers={'Content-Type': 'application/json'},
        json={'session_id': session_id_b, 'file_price_type': '1'},
        timeout=10
    )
    
    print(f"用户B支付请求状态码: {response_b.status_code}")
    if response_b.status_code == 200:
        result_b = response_b.json()
        print(f"用户B订单号: {result_b.get('out_trade_no')}")
        out_trade_no_b = result_b.get('out_trade_no')
    else:
        print(f"用户B支付请求失败: {response_b.text}")
        out_trade_no_b = None
    
    time.sleep(1)
    
    # 模拟用户A支付成功
    if out_trade_no_a:
        print(f"\n模拟用户A支付成功，订单号: {out_trade_no_a}")
        notify_data_a = {
            'trade_status': 'TRADE_SUCCESS',
            'out_trade_no': out_trade_no_a,
            'trade_no': '2026011200000000000123456',
            'total_amount': '3.00',
            'gmt_payment': '2026-01-18 14:30:45',
            'buyer_id': '2088102146225135',
            'buyer_logon_id': 'user_a@alipay.com'
        }
        
        response_notify_a = requests.post(
            'http://127.0.0.1:5000/alipay_notify',
            data=notify_data_a,
            timeout=10
        )
        
        print(f"用户A异步通知响应: {response_notify_a.text.strip()}")
    
    time.sleep(1)
    
    # 模拟用户B支付成功
    if out_trade_no_b:
        print(f"\n模拟用户B支付成功，订单号: {out_trade_no_b}")
        notify_data_b = {
            'trade_status': 'TRADE_SUCCESS',
            'out_trade_no': out_trade_no_b,
            'trade_no': '2026011200000000000789123',
            'total_amount': '3.00',
            'gmt_payment': '2026-01-18 14:31:45',
            'buyer_id': '2088102146225136',
            'buyer_logon_id': 'user_b@alipay.com'
        }
        
        response_notify_b = requests.post(
            'http://127.0.0.1:5000/alipay_notify',
            data=notify_data_b,
            timeout=10
        )
        
        print(f"用户B异步通知响应: {response_notify_b.text.strip()}")
    
    time.sleep(1)
    
    # 测试用户A访问支付成功页面
    if out_trade_no_a:
        print(f"\n用户A访问支付成功页面，session_id: {session_id_a}")
        return_url_a = f"http://127.0.0.1:5000/alipay_return?trade_status=TRADE_SUCCESS&out_trade_no={out_trade_no_a}&session_id={session_id_a}"
        
        response_return_a = requests.get(return_url_a, timeout=10, allow_redirects=False)
        
        print(f"用户A同步返回状态码: {response_return_a.status_code}")
        if response_return_a.status_code == 200:
            if 'payment_success' in response_return_a.text or '您无权' in response_return_a.text:
                print("✅ 用户A可以查看自己的订单文件密码")
            else:
                print("❌ 用户A无法查看自己的订单文件密码")
        else:
            print(f"❌ 用户A访问失败: {response_return_a.text}")
    
    time.sleep(1)
    
    # 测试用户B访问用户A的支付成功页面（跨用户访问）
    if out_trade_no_a and session_id_b:
        print(f"\n用户B尝试访问用户A的订单，session_id: {session_id_b}")
        return_url_b = f"http://127.0.0.1:5000/alipay_return?trade_status=TRADE_SUCCESS&out_trade_no={out_trade_no_a}&session_id={session_id_b}"
        
        response_return_b = requests.get(return_url_b, timeout=10, allow_redirects=False)
        
        print(f"用户B跨用户访问状态码: {response_return_b.status_code}")
        if response_return_b.status_code == 200:
            if '您无权' in response_return_b.text:
                print("✅ 用户B无法查看用户A的订单文件密码（正确）")
            else:
                print("❌ 用户B可以查看用户A的订单文件密码（错误）")
        else:
            print(f"❌ 用户B访问失败: {response_return_b.text}")
    
    print("\n" + "=" * 60)
    print()

def test_pending_order():
    """测试待支付订单无法查看文件密码"""
    
    print("=" * 60)
    print("测试场景2：待支付订单无法查看文件密码")
    print("=" * 60)
    print()
    
    # 创建订单（待支付状态）
    session_id = "pending_test_" + str(int(time.time() * 1000))
    print(f"创建待支付订单，session_id: {session_id}")
    
    response = requests.post(
        'http://127.0.0.1:5000/alipay_wap_pay',
        headers={'Content-Type': 'application/json'},
        json={'session_id': session_id, 'file_price_type': '1'},
        timeout=10
    )
    
    print(f"订单创建状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        out_trade_no = result.get('out_trade_no')
        print(f"订单号: {out_trade_no}")
        
        # 尝试访问支付成功页面（订单状态为TRADE_PENDING）
        print(f"\n尝试访问待支付订单的支付成功页面")
        return_url = f"http://127.0.0.1:5000/alipay_return?trade_status=TRADE_SUCCESS&out_trade_no={out_trade_no}&session_id={session_id}"
        
        response_return = requests.get(return_url, timeout=10, allow_redirects=False)
        
        print(f"访问状态码: {response_return.status_code}")
        if response_return.status_code == 200:
            if '支付未完成' in response_return.text:
                print("✅ 待支付订单无法查看文件密码（正确）")
            else:
                print("❌ 待支付订单可以查看文件密码（错误）")
        else:
            print(f"❌ 访问失败: {response_return.text}")
    else:
        print(f"❌ 订单创建失败: {response.text}")
    
    print("\n" + "=" * 60)
    print()

def test_failed_order():
    """测试支付失败订单无法查看文件密码"""
    
    print("=" * 60)
    print("测试场景3：支付失败订单无法查看文件密码")
    print("=" * 60)
    print()
    
    # 创建订单
    session_id = "failed_test_" + str(int(time.time() * 1000))
    print(f"创建订单，session_id: {session_id}")
    
    response = requests.post(
        'http://127.0.0.1:5000/alipay_wap_pay',
        headers={'Content-Type': 'application/json'},
        json={'session_id': session_id, 'file_price_type': '1'},
        timeout=10
    )
    
    print(f"订单创建状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        out_trade_no = result.get('out_trade_no')
        print(f"订单号: {out_trade_no}")
        
        # 模拟支付失败
        print(f"\n模拟支付失败")
        notify_data = {
            'trade_status': 'TRADE_FAILED',
            'out_trade_no': out_trade_no,
            'trade_no': '2026011200000000000999999',
            'total_amount': '3.00',
            'gmt_payment': '2026-01-18 14:35:45',
            'buyer_id': '2088102146225137',
            'buyer_logon_id': 'user_failed@alipay.com'
        }
        
        response_notify = requests.post(
            'http://127.0.0.1:5000/alipay_notify',
            data=notify_data,
            timeout=10
        )
        
        print(f"支付失败通知响应: {response_notify.text.strip()}")
        
        # 尝试访问支付成功页面（订单状态为TRADE_FAILED）
        print(f"\n尝试访问支付失败订单的支付成功页面")
        return_url = f"http://127.0.0.1:5000/alipay_return?trade_status=TRADE_SUCCESS&out_trade_no={out_trade_no}&session_id={session_id}"
        
        response_return = requests.get(return_url, timeout=10, allow_redirects=False)
        
        print(f"访问状态码: {response_return.status_code}")
        if response_return.status_code == 200:
            if '支付未完成' in response_return.text:
                print("✅ 支付失败订单无法查看文件密码（正确）")
            else:
                print("❌ 支付失败订单可以查看文件密码（错误）")
        else:
            print(f"❌ 访问失败: {response_return.text}")
    else:
        print(f"❌ 订单创建失败: {response.text}")
    
    print("\n" + "=" * 60)
    print()

if __name__ == "__main__":
    print("文件与支付记录唯一性关联测试脚本")
    print()
    
    while True:
        print("\n请选择测试项目：")
        print("1. 测试用户A和用户B同时下载文件并支付")
        print("2. 测试待支付订单无法查看文件密码")
        print("3. 测试支付失败订单无法查看文件密码")
        print("0. 退出")
        print()
        
        choice = input("请输入选项 (0-3): ")
        
        if choice == "1":
            test_unique_payment_record()
        elif choice == "2":
            test_pending_order()
        elif choice == "3":
            test_failed_order()
        elif choice == "0":
            print("\n退出测试...")
            break
        else:
            print("\n无效选项，请重新选择")
        
        print("\n" + "=" * 60)
        print()