@echo off
cd /d "%~dp0"
quarto render slides.qmd
echo.
echo Done! Output: output\slides.html
pause
