@echo off
chcp 65001 >nul
echo Remotion Studio
echo ===============
echo.
echo Step 1: Installing dependencies...
call npm install
echo.
echo Step 2: Starting Remotion Studio...
echo Open browser at: http://localhost:3000
echo.
npx remotion studio entry.tsx
pause