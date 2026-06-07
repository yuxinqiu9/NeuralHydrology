@echo off
cd /d "%~dp0"

echo [1/2] Rendering HTML (revealjs)...
quarto render slides.qmd --to revealjs
if errorlevel 1 (
    echo ERROR: HTML render failed.
    pause
    exit /b 1
)
echo HTML done: output\slides.html

echo.
echo [2/2] Rendering PDF (revealjs print mode via Chrome)...
node pdf.js
if errorlevel 1 (
    echo ERROR: PDF render failed.
    echo Make sure output\slides.pdf is not open in any PDF viewer.
    pause
    exit /b 1
)
echo PDF done: output\slides.pdf

echo.
echo =============================================
echo  All outputs ready:
echo    HTML : output\slides.html
echo    PDF  : output\slides.pdf
echo =============================================
pause
