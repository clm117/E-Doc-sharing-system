# 测试支付成功页面的简单脚本，使用Python标准库
import http.client
import urllib.parse

# 测试配置
HOST = "localhost"
PORT = 5000

# 测试数据
TEST_FILE_NAME = "测试文件.pdf"
TEST_FILE_PASSWORD = "123456"
TEST_AMOUNT = 3.00

def test_payment_success():
    print("=== 测试支付成功页面 ===")
    
    # 构建查询参数
    params = {
        "file_name": TEST_FILE_NAME,
        "file_password": TEST_FILE_PASSWORD,
        "amount": TEST_AMOUNT
    }
    
    # 编码查询参数
    encoded_params = urllib.parse.urlencode(params)
    path = f"/payment_success?{encoded_params}"
    print(f"测试URL: http://{HOST}:{PORT}{path}")
    
    try:
        # 创建HTTP连接
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request("GET", path)
        
        # 获取响应
        response = conn.getresponse()
        print(f"\n响应状态码: {response.status}")
        
        if response.status == 200:
            # 读取响应内容
            content = response.read().decode('utf-8')
            
            # 检查页面内容
            test_results = []
            
            # 检查文件名
            if TEST_FILE_NAME in content:
                test_results.append(f"✅ 页面包含文件名: {TEST_FILE_NAME}")
            else:
                test_results.append(f"❌ 页面不包含文件名: {TEST_FILE_NAME}")
            
            # 检查文件密码
            if TEST_FILE_PASSWORD in content:
                test_results.append(f"✅ 页面包含文件密码: {TEST_FILE_PASSWORD}")
            else:
                test_results.append(f"❌ 页面不包含文件密码: {TEST_FILE_PASSWORD}")
            
            # 检查金额
            amount_strings = [
                str(TEST_AMOUNT),
                f"{TEST_AMOUNT:.2f}",
                f"¥{TEST_AMOUNT}",
                f"¥{TEST_AMOUNT:.2f}"
            ]
            amount_found = any(amount_str in content for amount_str in amount_strings)
            if amount_found:
                test_results.append(f"✅ 页面包含金额: {TEST_AMOUNT}")
            else:
                test_results.append(f"❌ 页面不包含金额: {TEST_AMOUNT}")
            
            # 打印测试结果
            for result in test_results:
                print(result)
            
            # 检查是否所有测试都通过
            if all("✅" in result for result in test_results):
                print("\n✅ 支付成功页面测试全部通过！")
            else:
                print("\n❌ 部分测试未通过，请检查代码！")
                print(f"\n页面内容片段（前200字符）:")
                print(content[:200] + "...")
        else:
            print(f"❌ 页面请求失败，状态码: {response.status}")
            print(f"响应内容: {response.read().decode('utf-8')}")
        
        # 关闭连接
        conn.close()
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_payment_success()
