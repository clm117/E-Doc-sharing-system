# cx-Oracle 安装指南

## 安装环境要求

要在 Windows 系统上成功安装 cx-Oracle，您需要满足以下条件：

### 1. 系统依赖

#### Microsoft Visual C++ Build Tools
cx-Oracle 需要 Microsoft Visual C++ 14.0 或更高版本才能编译安装。

**官方下载地址**：
1. 最新版本官方页面：https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/
2. VS2022 Build Tools 直接下载：https://aka.ms/vs/17/release/vs_BuildTools.exe
3. 旧版本完整安装程序：https://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe

**安装步骤**：
1. 下载并运行安装程序
2. 选择 "C++ 生成工具" 工作负载
3. 至少勾选以下组件：
   - MSVC v143 - VS 2022 C++ x64/x86 生成工具
   - Windows 11 SDK (10.0.22621.0) 或更高版本
4. 点击安装，完成后重启计算机

#### Oracle Instant Client
cx-Oracle 需要 Oracle Instant Client 来连接 Oracle 数据库。

**下载地址**：https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html

**安装步骤**：
1. 下载 "Instant Client Package - Basic" 或 "Instant Client Package - Basic Light"
2. 解压到一个目录（例如：`C:\oracle\instantclient_21_9`）
3. 将该目录添加到系统环境变量 `PATH` 中

### 2. 安装 cx-Oracle

完成上述系统依赖安装后，在命令行中运行：

```bash
py -m pip install cx-Oracle
```

## 环境配置

### 配置 TNS_ADMIN（可选）
如果您使用 TNS 名称连接数据库，需要：

1. 创建 `tnsnames.ora` 文件，内容示例：
```
orcleshow = 
  (DESCRIPTION = 
    (ADDRESS_LIST = 
      (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521)) 
    ) 
    (CONNECT_DATA = 
      (SERVICE_NAME = orcleshow) 
    ) 
  )
```

2. 设置系统环境变量 `TNS_ADMIN` 指向包含 `tnsnames.ora` 的目录

## 验证安装

安装完成后，可以运行以下 Python 代码验证：

```python
import cx_Oracle
print("cx-Oracle 版本:", cx_Oracle.__version__)
```

如果能够正常打印版本信息，则说明安装成功。

## 常见问题解决

### 1. 无法找到 Oracle Instant Client
**错误**：`DPI-1047: Cannot locate a 64-bit Oracle Client library`
**解决**：确保 Oracle Instant Client 目录已正确添加到系统环境变量 `PATH` 中

### 2. 连接数据库失败
**错误**：`ORA-12154: TNS:could not resolve the connect identifier specified`
**解决**：检查 DSN 配置是否正确，或确认 TNS 名称已在 `tnsnames.ora` 中定义

### 3. 权限错误
**错误**：`ORA-1017: invalid username/password; logon denied`
**解决**：检查数据库用户名和密码是否正确

## 替代方案

如果您暂时无法安装 Microsoft Visual C++ Build Tools，可以考虑使用其他方法连接 Oracle 数据库：

1. **使用 Oracle 官方的 python-oracledb**：这是 Oracle 推出的新一代 Python 驱动，无需额外安装 Oracle Instant Client
   ```bash
   py -m pip install oracledb
   ```

2. **使用 JDBC 桥接**：通过 JayDeBeApi 连接 Oracle
   ```bash
   py -m pip install jaydebeapi jpype1
   ```

更多信息请参考：https://oracle.github.io/python-oracledb/