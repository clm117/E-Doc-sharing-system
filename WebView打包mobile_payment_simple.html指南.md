# 使用WebView将mobile_payment_simple.html打包成安卓应用

## 一、方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 原生Android + WebView | 性能好，功能强大 | 需要Android开发经验 | 有Android开发基础 |
| Cordova + WebView | 简单快速，跨平台 | 依赖Web服务，性能略低 | Web开发者，快速原型 |

## 二、方案一：使用Cordova打包（推荐）

### 步骤1：创建Cordova项目
打开**命令提示符**，执行：
```bash
cordova create PaymentApp com.example.payment PaymentApp
cd PaymentApp
```

### 步骤2：添加Android平台
```bash
cordova platform add android
```

### 步骤3：配置项目文件

1. **删除默认文件**：
   - 进入`www`目录
   - 删除`index.html`, `css/`, `js/`等默认文件

2. **创建新的index.html**：
   在`www`目录下创建`index.html`，内容如下：
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
       <meta name="format-detection" content="telephone=no">
       <title>支付页面</title>
       <style>
           body {
               margin: 0;
               padding: 0;
               font-family: Arial, sans-serif;
               background-color: #f5f5f5;
           }
           .loading {
               display: flex;
               justify-content: center;
               align-items: center;
               height: 100vh;
               flex-direction: column;
           }
           .spinner {
               width: 50px;
               height: 50px;
               border: 5px solid #f3f3f3;
               border-top: 5px solid #007bff;
               border-radius: 50%;
               animation: spin 1s linear infinite;
           }
           @keyframes spin {
               0% { transform: rotate(0deg); }
               100% { transform: rotate(360deg); }
           }
       </style>
       <script>
           // 页面加载后重定向到目标URL
           window.onload = function() {
               // 延迟1秒后跳转，让用户看到加载动画
               setTimeout(function() {
                   window.location.href = "http://192.168.100.174:5000/mobile_payment_simple";
               }, 1000);
           };
       </script>
   </head>
   <body>
       <div class="loading">
           <div class="spinner"></div>
           <p style="margin-top: 20px; color: #666;">正在加载支付页面...</p>
       </div>
   </body>
   </html>
   ```

### 步骤4：安装必要插件
```bash
# 安装网络状态检测插件
cordova plugin add cordova-plugin-network-information

# 安装设备信息插件
cordova plugin add cordova-plugin-device

# 安装启动页插件
cordova plugin add cordova-plugin-splashscreen

# 安装状态栏插件
cordova plugin add cordova-plugin-statusbar
```

### 步骤5：配置config.xml
编辑`config.xml`文件，添加以下配置：

```xml
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.example.payment" version="1.0.0" xmlns="http://www.w3.org/ns/widgets">
    <name>支付应用</name>
    <description>移动支付应用</description>
    <author email="dev@example.com">开发者</author>
    <content src="index.html" />
    
    <!-- 允许所有网络请求 -->
    <access origin="*" />
    
    <!-- 配置启动页 -->
    <preference name="SplashScreen" value="screen" />
    <preference name="SplashScreenDelay" value="3000" />
    <preference name="AutoHideSplashScreen" value="true" />
    
    <!-- 配置全屏 -->
    <preference name="Fullscreen" value="false" />
    
    <!-- 配置状态栏 -->
    <preference name="StatusBarOverlaysWebView" value="true" />
    <preference name="StatusBarBackgroundColor" value="#000000" />
    
    <!-- 配置WebView设置 -->
    <preference name="Orientation" value="portrait" />
    <preference name="KeepRunning" value="false" />
    
    <platform name="android">
        <!-- 允许HTTP流量（Android 9+需要） -->
        <edit-config file="app/src/main/AndroidManifest.xml" mode="merge" target="/manifest/application">
            <application android:usesCleartextTraffic="true" />
        </edit-config>
        
        <!-- 配置应用图标 -->
        <icon density="ldpi" src="res/icon/android/ldpi.png" />
        <icon density="mdpi" src="res/icon/android/mdpi.png" />
        <icon density="hdpi" src="res/icon/android/hdpi.png" />
        <icon density="xhdpi" src="res/icon/android/xhdpi.png" />
        <icon density="xxhdpi" src="res/icon/android/xxhdpi.png" />
        <icon density="xxxhdpi" src="res/icon/android/xxxhdpi.png" />
        
        <!-- 配置启动页 -->
        <splash density="land-hdpi" src="res/screen/android/splash-land-hdpi.png" />
        <splash density="land-ldpi" src="res/screen/android/splash-land-ldpi.png" />
        <splash density="land-mdpi" src="res/screen/android/splash-land-mdpi.png" />
        <splash density="land-xhdpi" src="res/screen/android/splash-land-xhdpi.png" />
        <splash density="port-hdpi" src="res/screen/android/splash-port-hdpi.png" />
        <splash density="port-ldpi" src="res/screen/android/splash-port-ldpi.png" />
        <splash density="port-mdpi" src="res/screen/android/splash-port-mdpi.png" />
        <splash density="port-xhdpi" src="res/screen/android/splash-port-xhdpi.png" />
    </platform>
</widget>
```

### 步骤6：构建APK
```bash
# 构建调试版APK
cordova build android

# 构建发布版APK
cordova build android --release
```

### 步骤7：签名APK
1. 生成签名密钥库：
   ```bash
   keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
   ```

2. 创建`build.json`文件：
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

3. 重新构建发布版APK：
   ```bash
   cordova build android --release
   ```


## 三、方案二：使用原生Android开发

### 步骤1：创建Android项目
1. 打开Android Studio
2. 创建新项目（Empty Activity）
3. 设置项目名称、包名等

### 步骤2：配置WebView
1. 在`activity_main.xml`中添加WebView：
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <androidx.constraintlayout.widget.ConstraintLayout
       xmlns:android="http://schemas.android.com/apk/res/android"
       xmlns:app="http://schemas.android.com/apk/res-auto"
       xmlns:tools="http://schemas.android.com/tools"
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       tools:context=".MainActivity">

       <WebView
           android:id="@+id/webview"
           android:layout_width="match_parent"
           android:layout_height="match_parent" />

       <ProgressBar
           android:id="@+id/progress_bar"
           android:layout_width="wrap_content"
           android:layout_height="wrap_content"
           android:visibility="gone"
           app:layout_constraintBottom_toBottomOf="parent"
           app:layout_constraintLeft_toLeftOf="parent"
           app:layout_constraintRight_toRightOf="parent"
           app:layout_constraintTop_toTopOf="parent" />

   </androidx.constraintlayout.widget.ConstraintLayout>
   ```

2. 在`MainActivity.java`中配置WebView：
   ```java
   package com.example.payment;

   import android.annotation.SuppressLint;
   import android.graphics.Bitmap;
   import android.os.Bundle;
   import android.view.View;
   import android.webkit.WebChromeClient;
   import android.webkit.WebSettings;
   import android.webkit.WebView;
   import android.webkit.WebViewClient;
   import android.widget.ProgressBar;

   import androidx.appcompat.app.AppCompatActivity;

   public class MainActivity extends AppCompatActivity {

       private WebView webView;
       private ProgressBar progressBar;

       @SuppressLint("SetJavaScriptEnabled")
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_main);

           webView = findViewById(R.id.webview);
           progressBar = findViewById(R.id.progress_bar);

           // 配置WebView设置
           WebSettings webSettings = webView.getSettings();
           webSettings.setJavaScriptEnabled(true);
           webSettings.setDomStorageEnabled(true);
           webSettings.setDatabaseEnabled(true);
           webSettings.setCacheMode(WebSettings.LOAD_NO_CACHE);
           webSettings.setAppCacheEnabled(false);
           
           // 启用混合内容（HTTP和HTTPS混合）
           if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
               webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
           }

           // 设置WebViewClient
           webView.setWebViewClient(new WebViewClient() {
               @Override
               public void onPageStarted(WebView view, String url, Bitmap favicon) {
                   super.onPageStarted(view, url, favicon);
                   progressBar.setVisibility(View.VISIBLE);
               }

               @Override
               public void onPageFinished(WebView view, String url) {
                   super.onPageFinished(view, url);
                   progressBar.setVisibility(View.GONE);
               }
           });

           // 设置WebChromeClient（处理进度条）
           webView.setWebChromeClient(new WebChromeClient() {
               @Override
               public void onProgressChanged(WebView view, int newProgress) {
                   progressBar.setProgress(newProgress);
               }
           });

           // 加载目标URL
           webView.loadUrl("http://192.168.100.174:5000/mobile_payment_simple");
       }

       // 处理返回键
       @Override
       public void onBackPressed() {
           if (webView.canGoBack()) {
               webView.goBack();
           } else {
               super.onBackPressed();
           }
       }
   }
   ```

3. 添加网络权限到`AndroidManifest.xml`：
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
   <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
   ```

4. 配置允许HTTP流量（Android 9+）：
   ```xml
   <application
       android:allowBackup="true"
       android:icon="@mipmap/ic_launcher"
       android:label="@string/app_name"
       android:roundIcon="@mipmap/ic_launcher_round"
       android:supportsRtl="true"
       android:theme="@style/AppTheme"
       android:usesCleartextTraffic="true"
       android:networkSecurityConfig="@xml/network_security_config"
       ...>
   ```

5. 创建`res/xml/network_security_config.xml`：
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <network-security-config>
       <base-config cleartextTrafficPermitted="true">
           <trust-anchors>
               <certificates src="system" />
           </trust-anchors>
       </base-config>
   </network-security-config>
   ```

### 步骤3：构建和签名APK
1. 点击**Build** → **Generate Signed Bundle / APK**
2. 选择**APK**
3. 选择或创建签名密钥库
4. 构建发布版APK


## 四、优化建议

### 1. 添加加载动画
- 使用ProgressBar显示加载进度
- 添加启动页（Splash Screen）
- 优化页面加载速度

### 2. 处理离线情况
- 检测网络状态
- 显示离线提示页面
- 缓存必要资源

### 3. 优化用户体验
- 隐藏浏览器地址栏
- 禁用不必要的缩放
- 处理页面跳转
- 添加返回按钮处理

### 4. 安全性考虑
- 使用HTTPS（如果可能）
- 配置网络安全配置
- 验证SSL证书
- 防止XSS攻击


## 五、测试建议

### 1. 功能测试
- 测试支付流程完整性
- 测试页面加载速度
- 测试网络异常情况
- 测试不同设备兼容性

### 2. 性能测试
- 测试内存使用
- 测试CPU占用
- 测试电池消耗
- 测试页面渲染速度

### 3. 兼容性测试
- 测试不同Android版本
- 测试不同屏幕尺寸
- 测试不同设备厂商
- 测试不同网络环境


## 六、部署建议

### 1. 应用商店发布
- 准备应用图标和截图
- 编写应用描述
- 设置应用分类
- 提交审核

### 2. 直接分发
- 通过网站提供APK下载
- 使用二维码分发
- 通过社交媒体分享
- 企业内部分发


## 七、常见问题及解决方案

### 问题1：页面加载慢
- **解决**：优化后端服务，使用CDN，启用缓存

### 问题2：支付成功后跳转失败
- **解决**：配置正确的URL scheme，处理WebView内跳转

### 问题3：键盘弹出时布局错乱
- **解决**：配置WebView的输入模式，调整布局

### 问题4：HTTPS页面无法加载
- **解决**：配置网络安全配置，允许HTTP流量


## 八、推荐方案

对于Web开发者，**强烈推荐使用Cordova方案**，因为：
1. 学习曲线平缓
2. 开发效率高
3. 跨平台支持
4. 维护成本低

对于有Android开发经验的开发者，可以使用**原生Android方案**，获得更好的性能和更丰富的功能。