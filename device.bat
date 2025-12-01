@echo off
:: -----------------------------
:: CONFIGURE PATHS AND PORT
:: -----------------------------
set "ADB_PATH=%~dp0platform-tools-latest-windows\adb.exe"
set "SCRCPY_PATH=%~dp0platform-tools-latest-windows\scrcpy.exe"
set ADB_PORT=5555
:: -----------------------------

if not exist "%ADB_PATH%" (
    echo ADB not found - Android features disabled
    echo To enable: Download Android Platform Tools and extract to platform-tools-latest-windows folder
    exit /b 1
)

echo Disconnecting old connections...
"%ADB_PATH%" disconnect

echo Setting up device...
"%ADB_PATH%" tcpip %ADB_PORT%

echo Waiting for device to initialize...
ping 127.0.0.1 -n 4 >nul

:: Auto-detect USB-connected device
set DEVICE_ID=
for /f "skip=1 tokens=1,2" %%a in ('"%ADB_PATH%" devices') do (
    if "%%b"=="device" (
        set DEVICE_ID=%%a
        goto :found
    )
)

:: If no device found
echo No USB device detected! Make sure USB debugging is enabled.
exit /b 1

:found
echo Found device: %DEVICE_ID%

:: Get Wi-Fi IP automatically
set DEVICE_IP=
for /f "tokens=2" %%G in ('"%ADB_PATH%" -s %DEVICE_ID% shell ip addr show wlan0 ^| find "inet "') do set ipfull=%%G
for /f "tokens=1 delims=/" %%G in ("%ipfull%") do set DEVICE_IP=%%G

if "%DEVICE_IP%"=="" (
    echo Could not detect Wi-Fi IP. Make sure the phone is connected to Wi-Fi.
    exit /b 1
)

echo Device Wi-Fi IP: %DEVICE_IP%

:: Connect over Wi-Fi
"%ADB_PATH%" connect %DEVICE_IP%:%ADB_PORT%

:: Launch scrcpy
echo Launching scrcpy...
"%SCRCPY_PATH%"
