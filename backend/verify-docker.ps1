# 三问学习机后端 Docker 一键验证脚本
# 用法（在本目录下，已安装 Docker Desktop 并启动后）：
#   powershell -ExecutionPolicy Bypass -File .\verify-docker.ps1
$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[X] 未检测到 docker，请先安装并启动 Docker Desktop：https://www.docker.com/products/docker-desktop/" -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] 构建并启动容器..." -ForegroundColor Cyan
docker compose up -d --build

Write-Host "[2/4] 等待服务就绪..." -ForegroundColor Cyan
$ok = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 2
    try {
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/health" -TimeoutSec 5
        if ($r.status -eq "healthy") { $ok = $true; break }
    } catch {}
}

if (-not $ok) {
    Write-Host "[X] 健康检查未通过，查看日志：docker compose logs" -ForegroundColor Red
    docker compose logs
    exit 1
}

Write-Host "[3/4] 健康检查通过：" -ForegroundColor Green
$r | ConvertTo-Json -Compress

Write-Host "[4/4] 容器状态：" -ForegroundColor Cyan
docker compose ps

Write-Host "`n[OK] Docker 链路验证通过。停止容器：docker compose down" -ForegroundColor Green
