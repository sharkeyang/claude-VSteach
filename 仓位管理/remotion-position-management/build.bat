@echo off
chcp 65001 >nul
echo Rendering Video...
echo.
echo Rendering 1080p...
call npx remotion render entry.tsx PositionManagement out/position-management-1080p.mp4 --codec h264
echo.
echo Done! Output: out\position-management-1080p.mp4
echo.
pause