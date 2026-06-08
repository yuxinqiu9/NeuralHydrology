@echo off
setlocal
cd /d "%~dp0"

set "QUARTO_CMD=quarto"
set "FALLBACK_QUARTO_1=%LOCALAPPDATA%\Programs\Quarto\bin\quarto.exe"
set "FALLBACK_QUARTO_2=C:\Program Files\Quarto\bin\quarto.cmd"
set "FALLBACK_QUARTO_3=C:\Program Files\Quarto\bin\quarto.exe"
set "FALLBACK_QUARTO=C:\Program Files\RStudio\resources\app\bin\quarto\bin\quarto.cmd"

where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js not found in PATH.
    echo Install Node.js and try again.
    pause
    exit /b 1
)

where quarto >nul 2>nul
if errorlevel 1 (
    if exist "%FALLBACK_QUARTO_1%" (
        set "QUARTO_CMD=%FALLBACK_QUARTO_1%"
        echo INFO: Using Quarto from user install path.
    ) else if exist "%FALLBACK_QUARTO_2%" (
        set "QUARTO_CMD=%FALLBACK_QUARTO_2%"
        echo INFO: Using Quarto from Program Files.
    ) else if exist "%FALLBACK_QUARTO_3%" (
        set "QUARTO_CMD=%FALLBACK_QUARTO_3%"
        echo INFO: Using Quarto from Program Files.
    ) else if exist "%FALLBACK_QUARTO%" (
        set "QUARTO_CMD=%FALLBACK_QUARTO%"
        echo INFO: Using Quarto from RStudio bundle.
    ) else (
        echo ERROR: Quarto not found in PATH.
        echo Install Quarto from https://quarto.org/docs/get-started/
        echo or install RStudio with bundled Quarto.
        pause
        exit /b 1
    )
)

where Rscript >nul 2>nul
if errorlevel 1 (
    for /f %%D in ('dir /b /ad /o-n "%LOCALAPPDATA%\Programs\R\R-*" 2^>nul') do (
        if exist "%LOCALAPPDATA%\Programs\R\%%D\bin\Rscript.exe" (
            set "PATH=%LOCALAPPDATA%\Programs\R\%%D\bin;%PATH%"
            goto :rscript_found
        )
        if exist "%LOCALAPPDATA%\Programs\R\%%D\bin\x64\Rscript.exe" (
            set "PATH=%LOCALAPPDATA%\Programs\R\%%D\bin\x64;%PATH%"
            goto :rscript_found
        )
    )

    for /f %%D in ('dir /b /ad /o-n "C:\Program Files\R\R-*" 2^>nul') do (
        if exist "C:\Program Files\R\%%D\bin\Rscript.exe" (
            set "PATH=C:\Program Files\R\%%D\bin;%PATH%"
            goto :rscript_found
        )
        if exist "C:\Program Files\R\%%D\bin\x64\Rscript.exe" (
            set "PATH=C:\Program Files\R\%%D\bin\x64;%PATH%"
            goto :rscript_found
        )
    )
)

:rscript_found
where Rscript >nul 2>nul
if errorlevel 1 (
    echo WARN: Rscript not found in PATH. Quarto may fail if slides contain R code chunks.
    echo Install R from https://cloud.r-project.org/
) else (
    echo INFO: Rscript detected.
)

if not exist "node_modules\puppeteer-core" (
    echo INFO: Installing Node dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed.
        pause
        exit /b 1
    )
)

echo [1/2] Rendering HTML ^(revealjs^)...
call "%QUARTO_CMD%" render slides.qmd --to revealjs
if errorlevel 1 (
    echo ERROR: HTML render failed.
    pause
    exit /b 1
)
echo HTML done: output\slides.html

echo.
echo [2/2] Rendering PDF ^(Chrome screenshot pipeline^) ...
call node pdf.js
if errorlevel 1 (
    echo ERROR: PDF render failed.
    echo Make sure output\slides.pdf is not open in any PDF viewer.
    echo You can also set CHROME_PATH if Chrome is installed elsewhere.
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
