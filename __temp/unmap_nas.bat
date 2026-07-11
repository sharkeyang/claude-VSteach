@echo off
chcp 65001 > nul
echo ===== Disconnect NAS drives =====
echo.
net use Z: /delete
net use Y: /delete
net use X: /delete
net use W: /delete
echo.
echo Done.
pause
