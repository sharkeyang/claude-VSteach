@echo off
chcp 65001 > nul
echo ===== Map ztech =====
echo.
net use Y: \\192.168.1.82\ztech /persistent:yes
echo.
echo Y: -^> ztech
pause
