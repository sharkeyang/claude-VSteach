@echo off
cd /d "d:\@VSwork\VSteach"
python md2pdf.py "_CHRIS/Chris-2026-07-07-每日计划.md"
if exist "_CHRIS/Chris-20260707-每日计划.pdf" (
  echo PDF generated successfully
) else (
  echo PDF generation failed - check if the .md file exists
)
pause