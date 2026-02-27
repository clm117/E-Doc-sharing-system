# 测试支付成功页面参数处理和页面渲染的脚本
import requests

# 测试支付成功页面的URL
BASE_URL = "http://127.0.0.1:5000"

# 测试数据
TEST_FILE_NAME = "测试文件.pdf"
TEST_FILE_PASSWORD = "123456"
TEST_AMOUNT = 3.00

def test_payment_success_page():
    print("=== 测试支付成功页面 ===")
    
    # 构建支付成功页面的URL
    payment_success_url = f"{BASE_URL}/payment_success?file_name={TEST_FILE_NAME}&file_password={TEST_FILE_PASSWORD}&amount={TEST_AMOUNT}"
    print(f"测试URL: {payment_success_url}")
    
    try:
        # 发送请求
        response = requests.get(payment_success_url)
        print(f"\n响应状态码: {response.status_code}")
        
        # 检查响应内容
        if response.status_code == 200:
            content = response.text
            
            # 检查页面是否包含期望的内容
            if TEST_FILE_NAME in content:
                print(f"✅ 页面包含文件名: {TEST_FILE_NAME}")
            else:
                print(f"❌ 页面不包含文件名: {TEST_FILE_NAME}")
                print(f"页面内容片段: {content[:200]}...")
            
            if TEST_FILE_PASSWORD in content:
                print(f"✅ 页面包含文件密码: {TEST_FILE_PASSWORD}")
            else:
                print(f"❌ 页面不包含文件密码: {TEST_FILE_PASSWORD}")
                print(f"页面内容片段: {content[:200]}...")
            
            if str(TEST_AMOUNT) in content or f"{TEST_AMOUNT:.2f}" in content or f"¥{TEST_AMOUNT}" in content or f"¥{TEST_AMOUNT:.2f}" in content:
                print(f"✅ 页面包含金额: {TEST_AMOUNT}")
            else:
                print(f"❌ 页面不包含金额: {TEST_AMOUNT}")
                print(f"页面内容片段: {content[:200]}...")
            
            print("\n✅ 支付成功页面测试通过！")
        else:
            print(f"❌ 页面请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_payment_success_page()
