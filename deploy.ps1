# PriceScout 自动部署脚本
# 遇到网络问题时，请运行此脚本

Write-Host "🚀 PriceScout 自动部署脚本" -ForegroundColor Cyan
Write-Host ""

$gitPath = "C:\Program Files\Git\cmd\git.exe"

if (!(Test-Path $gitPath)) {
    Write-Host "❌ Git 未安装" -ForegroundColor Red
    Write-Host "请先安装 Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git 已安装" -ForegroundColor Green

# 尝试推送，最多重试5次
$maxRetries = 5
$retryCount = 0

while ($retryCount -lt $maxRetries) {
    Write-Host ""
    Write-Host "📤 正在推送代码到 GitHub (尝试 $($retryCount + 1)/$maxRetries)..." -ForegroundColor Cyan
    
    $retryCount++
    
    try {
        & $gitPath push -u origin main --force
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "🎉 部署成功！" -ForegroundColor Green
            Write-Host ""
            Write-Host "请访问以下链接启用 GitHub Pages:" -ForegroundColor Yellow
            Write-Host "https://github.com/pricescout/pricescout/settings/pages" -ForegroundColor Cyan
            exit 0
        }
    } catch {
        Write-Host "⚠️  推送失败，正在重试..." -ForegroundColor Yellow
    }
    
    if ($retryCount -lt $maxRetries) {
        Write-Host "⏳ 等待 5 秒后重试..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

Write-Host ""
Write-Host "⚠️  无法连接到 GitHub，请检查网络后手动运行:" -ForegroundColor Yellow
Write-Host ""
Write-Host "cd d:\solo项目" -ForegroundColor Cyan
Write-Host "git push -u origin main --force" -ForegroundColor Cyan
Write-Host ""
