@echo off
cd /d "%~dp0"
Rscript -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"
echo.
echo Done! Output: _book\index.html
pause
