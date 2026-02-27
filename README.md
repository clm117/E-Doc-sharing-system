# 二维码与数据库更新系统

这是一个使用Python Flask框架开发的Web应用，包含二维码生成和Oracle数据库联动功能，兼容IE和Chrome浏览器。

## 功能特性

- 生成可扫描的二维码，扫描后跳转到手机页面
- 提供更新按钮，可联动到本地Oracle数据库
- 兼容IE和Chrome浏览器
- 响应式设计，适配不同屏幕尺寸

## 环境要求

- Python 3.6+
- Oracle数据库
- Oracle Instant Client（用于cx_Oracle连接）

## 安装步骤

1. 安装依赖包：
```bash
pip install -r requirements.txt
```

2. 配置Oracle数据库：
   - 确保Oracle Instant Client已安装并配置环境变量
   - 修改`app.py`中的数据库连接配置：
     ```python
     DB_CONFIG = {
         'user': 'your_username',  # 替换为实际用户名
         'password': 'your_password',  # 替换为实际密码
         'dsn': 'your_oracle_dsn',  # 替换为实际DSN（如：localhost:1521/orcl）
         'encoding': 'UTF-8'
     }
     ```

3. 配置手机页面URL：
   - 修改`app.py`中的`MOBILE_PAGE_URL`变量为实际的手机页面地址

## 运行应用

```bash
python app.py
```

应用将在`http://localhost:5000`启动

## 使用说明

1. 打开浏览器访问`http://localhost:5000`
2. 页面将显示一个二维码，扫描可跳转到配置的手机页面
3. 点击"更新数据库"按钮，系统将连接Oracle数据库执行更新操作
4. 操作结果将显示在页面上

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML5, CSS3, JavaScript (兼容IE)
- **二维码生成**：qrcode库
- **数据库连接**：cx_Oracle

## 浏览器兼容性

- Chrome 60+
- IE 10+
- Firefox 55+
- Safari 11+

## 注意事项

1. 确保Oracle数据库服务正常运行
2. 确保数据库用户有足够的权限执行更新操作
3. 首次运行可能需要安装Oracle Instant Client
4. 在生产环境中，建议关闭调试模式(debug=False)