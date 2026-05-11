@echo off
chcp 65001
echo.
echo ========================================
echo   PriceScout 一键推送脚本
echo ========================================
echo.
echo 正在推送到 GitHub...
echo.

"C:\Program Files\Git\cmd\git.exe" push -u origin main

if %ERRORLEVEL% == 0 (
    echo.
    echo ========================================
    echo   ✅ 推送成功！
    echo ========================================
    echo.
    echo 请访问以下链接启用 GitHub Pages:
    echo https://github.com/309000545-byte/pricescout/settings/pages
    echo.
    pause
    start https://github.com/309000545-byte/pricescout/settings/pages
) else (
    echo.
    echo ========================================
    echo   ❌ 推送失败
    echo ========================================
    echo.
    echo 请检查网络连接后重试
    echo.
    pause
)
