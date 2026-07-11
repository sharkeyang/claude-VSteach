@echo off
chcp 65001 > nul
echo ===== Map SHARKCLOUD NAS =====
echo.
echo Z: -^> file
net use Z: \\192.168.1.82\zfile /persistent:yes /user:admin sharke6114
echo Y: -^> teach
net use Y: \\192.168.1.82\zteach /persistent:yes /user:admin sharke6114
echo X: -^> vedio
net use X: \\192.168.1.82\zvedio /persistent:yes /user:admin sharke6114
echo W: -^> backup
net use W: \\192.168.1.82\zbackup /persistent:yes /user:admin sharke6114
echo.
echo Finished.
pause
