@echo off
chcp 65001 > nul
echo ===== Map zteach =====
echo.
net use Y: \\192.168.1.82\zteach /persistent:yes /user:admin sharke6114
echo.
echo Y: -^> zteach
pause
