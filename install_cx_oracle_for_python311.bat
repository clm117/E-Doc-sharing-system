@echo off

echo =======================================
echo Python 3.11 64bit cx_Oracle 安装脚本
echo =======================================
echo.

REM 1. 检查Python版本
echo 检查Python版本...
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

echo.

REM 2. 创建必要的目录
echo 创建安装目录...
mkdir oracle_instantclient
mkdir cx_oracle_wheels

echo.

REM 3. 下载Oracle Instant Client（64位）
echo 正在下载Oracle Instant Client Basic 21.12.0.0.0...
powershell -Command "Invoke-WebRequest -Uri 'https://download.oracle.com/otn_software/nt/instantclient/2112000/instantclient-basic-windows.x64-21.12.0.0.0dbru.zip' -OutFile 'oracle_instantclient.zip'"

if errorlevel 1 (
    echo 错误：下载Oracle Instant Client失败
    echo 请手动下载：https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
    pause
    exit /b 1
)

echo.

REM 4. 解压Oracle Instant Client
echo 解压Oracle Instant Client...
powershell -Command "Expand-Archive -Path 'oracle_instantclient.zip' -DestinationPath 'oracle_instantclient'"

if errorlevel 1 (
    echo 错误：解压Oracle Instant Client失败
    pause
    exit /b 1
)

echo.

REM 5. 获取Instant Client目录路径
for /d %%i in (oracle_instantclient\instantclient*) do set INSTANT_CLIENT_PATH=%%~fi
echo Oracle Instant Client已解压到：%INSTANT_CLIENT_PATH%

echo.

REM 6. 添加Instant Client到PATH环境变量
echo 添加Oracle Instant Client到系统PATH...
setx PATH "%INSTANT_CLIENT_PATH%;%PATH%" /M

if errorlevel 1 (
    echo 警告：添加环境变量失败，可能需要管理员权限
    echo 请手动将 %INSTANT_CLIENT_PATH% 添加到系统PATH
) else (
    echo Oracle Instant Client已成功添加到系统PATH
)

echo.

REM 7. 下载预编译的cx_Oracle wheel文件
echo 正在下载cx_Oracle 8.3.0 预编译wheel文件...
powershell -Command "Invoke-WebRequest -Uri 'https://files.pythonhosted.org/packages/0c/9e/6b3a8b3644d7f2c591a0d868b104b407c0d2c3d4461b9b2b7c4a5f5f8a3f/cx_Oracle-8.3.0-cp311-cp311-win_amd64.whl' -OutFile 'cx_oracle_wheels/cx_Oracle-8.3.0-cp311-cp311-win_amd64.whl'"

if errorlevel 1 (
    echo 错误：下载cx_Oracle wheel文件失败
    echo 请手动下载对应版本：https://pypi.org/project/cx-Oracle/#files
    pause
    exit /b 1
)

echo.

REM 8. 安装cx_Oracle
echo 正在安装cx_Oracle...
python -m pip install cx_oracle_wheels/cx_Oracle-8.3.0-cp311-cp311-win_amd64.whl

if errorlevel 1 (
    echo 错误：安装cx_Oracle失败
    pause
    exit /b 1
) else (
    echo cx_Oracle安装成功！
)

echo.

REM 9. 验证安装
echo 验证cx_Oracle安装...
python -c "import cx_Oracle; print('cx_Oracle版本:', cx_Oracle.__version__)"

if errorlevel 1 (
    echo 错误：验证cx_Oracle安装失败
    echo 请检查Oracle Instant Client是否正确安装和配置
) else (
    echo cx_Oracle验证成功！
)

echo.
echo =======================================
echo 安装完成！请重启命令提示符使环境变量生效
echo =======================================
pause