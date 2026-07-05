@echo off
chcp 65001 >nul
title Claude Code 自动备份

echo ========================================
echo   Claude Code 配置自动备份
echo   %date% %time%
echo ========================================
echo.

:: --- 1. 备份 ~/.claude 全局配置 ---
echo [1/2] 备份全局配置 (~/.claude)...
cd /d "%USERPROFILE%\.claude"
git add -A >nul 2>&1
git commit -m "auto-backup %date%" >nul 2>&1
git push >nul 2>&1
echo       完成 ✅

:: --- 2. 备份 VSteach Claude 配置 ---
echo [2/2] 备份 VSteach Claude 配置...
cd /d "D:\@VSwork\VSteach"
git add -A >nul 2>&1
git commit -m "auto-backup %date%" >nul 2>&1
git push >nul 2>&1
echo       完成 ✅

echo.
echo ========================================
echo   全部备份完成！
echo ========================================
pause