@echo off
chcp 65001
echo.
echo ========================================
echo   推送 index.html 到 GitHub
echo ========================================
echo.

cd /d "d:\solo项目"

echo 正在推送...
"C:\Program Files\Git\cmd\git.exe" push origin main

if %ERRORLEVEL% == 0 (
    echo.
    echo ========================================
    echo   ✅ 推送成功！
    echo ========================================
    echo.
    echo 请等待 1-2 分钟后访问：
    echo https://309000545-byte.github.io/pricescout/
    echo.
    pause
    start https://309000545-byte.github.io/pricescout/
) else (
    echo.
    echo ========================================
    echo   ❌ 推送失败，请检查网络
    echo ========================================
    echo.
    pause
)
