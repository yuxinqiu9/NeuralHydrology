@echo off
cd /d "%~dp0"

set RSCRIPT=C:\Program Files\R\R-4.4.2\bin\Rscript.exe
set RSTUDIO_PANDOC=C:\Program Files\RStudio\resources\app\bin\quarto\bin\tools

echo Generating packages.bib...
"%RSCRIPT%" -e "knitr::write_bib(c('bookdown','knitr','rmarkdown'), 'packages.bib')"

echo Rendering bookdown gitbook...
"%RSCRIPT%" -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"

echo.
echo Done! Output: _book\index.html
pause
