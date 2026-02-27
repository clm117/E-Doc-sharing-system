# 使用Cordova打包mobile_payment_simple.html的任务清单

## 一、环境准备

### 任务1：安装Node.js和npm
- **状态**：待完成
- **操作步骤**：
  1. 访问Node.js官网（https://nodejs.org/）
  2. 下载LTS版本的Node.js安装包
  3. 运行安装程序，勾选"Add to PATH"选项
  4. 完成安装
- **验证方法**：
  ```bash
  node -v  # 应显示Node.js版本号
  npm -v   # 应显示npm版本号
  ```

### 任务2：安装Cordova
- **状态**：待完成
- **前置依赖**：Node.js和npm已安装
- **操作步骤**：
  ```bash
  npm install -g cordova
  ```
- **验证方法**：
  ```bash
  cordova -v  # 应显示Cordova版本号
  ```

### 任务3：安装Java JDK
- **状态**：待完成
- **版本要求**：JDK 8或更高版本
- **操作步骤**：
  1. 访问Oracle官网或OpenJDK官网下载JDK
  2. 运行安装程序
  3. 配置环境变量JAVA_HOME
- **验证方法**：
  ```bash
  java -version  # 应显示Java版本号
  javac -version # 应显示Java编译器版本号
  ```

### 任务4：安装Android SDK
- **状态**：待完成
- **操作步骤**：
  1. 下载Android Studio（包含Android SDK）
  2. 安装Android Studio
  3. 启动Android Studio，安装所需的SDK版本
  4. 配置环境变量ANDROID_HOME
- **验证方法**：
  ```bash
  adb version  # 应显示Android Debug Bridge版本号
  ```

## 二、项目创建与配置

### 任务5：创建Cordova项目
- **状态**：待完成
- **前置依赖**：Cordova已安装
- **操作步骤**：
  ```bash
  cordova create PaymentApp com.example.payment PaymentApp
  cd PaymentApp
  ```
- **预期结果**：创建名为PaymentApp的Cordova项目

### 任务6：添加Android平台
- **状态**：待完成
- **前置依赖**：Cordova项目已创建，Java JDK和Android SDK已安装
- **操作步骤**：
  ```bash
  cordova platform add android
  ```
- **预期结果**：在项目中添加Android平台支持

### 任务7：配置项目文件
- **状态**：待完成
- **操作步骤**：
  1. 删除`www`目录下的默认文件（index.html, css/, js/）
  2. 创建新的`index.html`文件，内容为：
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>支付页面</title>
         <script>
             // 页面加载后重定向到目标URL
             window.onload = function() {
                 window.location.href = "http://192.168.100.174:5000/mobile_payment_simple";
             };
         </script>
     </head>
     <body>
         <h1>加载中...</h1>
     </body>
     </html>
     ```

### 任务8：安装必要的插件
- **状态**：待完成
- **操作步骤**：
  ```bash
  # 安装网络相关插件
  cordova plugin add cordova-plugin-network-information
  # 安装设备信息插件（可选）
  cordova plugin add cordova-plugin-device
  ```

## 三、构建与测试

### 任务9：构建调试版APK
- **状态**：待完成
- **操作步骤**：
  ```bash
  cordova build android
  ```
- **预期结果**：生成调试版APK文件

### 任务10：测试APK
- **状态**：待完成
- **操作步骤**：
  1. 将生成的APK文件传输到安卓设备
  2. 安装APK文件
  3. 打开应用，测试是否能正常加载支付页面

### 任务11：生成签名密钥库
- **状态**：待完成
- **操作步骤**：
  ```bash
  keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
  ```
- **注意事项**：
  - 记住密钥库密码和别名密码
  - 妥善保管密钥库文件

### 任务12：构建发布版APK
- **状态**：待完成
- **前置依赖**：签名密钥库已生成
- **操作步骤**：
  1. 创建`build.json`文件，配置签名信息：
     ```json
     {
         "android": {
             "release": {
                 "keystore": "my-release-key.keystore",
                 "alias": "my-key-alias",
                 "storePassword": "你的密钥库密码",
                 "password": "你的别名密码"
             }
         }
     }
     ```
  2. 构建发布版APK：
     ```bash
     cordova build android --release
     ```
- **预期结果**：生成已签名的发布版APK文件

## 四、优化与部署

### 任务13：优化应用性能
- **状态**：待完成
- **操作步骤**：
  1. 添加启动页（Splash Screen）
  2. 添加图标
  3. 优化WebView配置

### 任务14：配置应用图标和启动页
- **状态**：待完成
- **操作步骤**：
  1. 安装图标和启动页插件：
     ```bash
     cordova plugin add cordova-plugin-splashscreen
     cordova plugin add cordova-plugin-icon
     ```
  2. 准备不同尺寸的图标和启动页图片
  3. 配置config.xml文件

### 任务15：部署应用
- **状态**：待完成
- **操作步骤**：
  1. 将发布版APK上传到应用商店
  2. 或通过其他渠道分发

## 三、现有环境检查结果

| 依赖项 | 状态 | 版本 | 备注 |
|-------|------|------|------|
| Node.js | 未安装 | - | 需先安装 |
| npm | 未安装 | - | Node.js安装后自动安装 |
| Cordova | 未安装 | - | 需要npm安装 |
| Java JDK | 未检查 | - | 需安装JDK 8+ |
| Android SDK | 未检查 | - | 需安装Android Studio或SDK |

## 四、注意事项

1. **环境变量配置**：确保所有依赖的环境变量都已正确配置
2. **版本兼容性**：注意Cordova、Node.js、Java JDK和Android SDK之间的版本兼容性
3. **网络连接**：打包过程中需要下载依赖，确保网络连接稳定
4. **密钥库安全**：妥善保管签名密钥库，防止泄露
5. **应用权限**：根据需要在config.xml中配置应用权限

## 五、预计完成时间

| 阶段 | 预计时间 |
|------|----------|
| 环境准备 | 2-3小时 |
| 项目创建与配置 | 1-2小时 |
| 构建与测试 | 1-2小时 |
| 优化与部署 | 2-3小时 |
| 总计 | 6-10小时 |