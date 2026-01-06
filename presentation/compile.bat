@echo off
REM =================================================================
REM Script de compilation de la présentation LaTeX
REM =================================================================

echo ============================================================
echo Compilation de la presentation LaTeX - Analyse Numerique
echo ============================================================
echo.

REM Vérifier si pdflatex est disponible
where pdflatex >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: pdflatex n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Veuillez installer MiKTeX ou TeX Live:
    echo   - MiKTeX: https://miktex.org/
    echo   - TeX Live: https://tug.org/texlive/
    echo.
    pause
    exit /b 1
)

echo [1/3] Premiere compilation avec pdflatex...
pdflatex -interaction=nonstopmode main.tex
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERREUR lors de la premiere compilation!
    echo Consultez le fichier main.log pour plus de details.
    pause
    exit /b 1
)

echo.
echo [2/3] Seconde compilation (pour les references)...
pdflatex -interaction=nonstopmode main.tex
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERREUR lors de la seconde compilation!
    echo Consultez le fichier main.log pour plus de details.
    pause
    exit /b 1
)

echo.
echo [3/3] Nettoyage des fichiers auxiliaires...
del /Q *.aux *.log *.out *.nav *.snm *.toc *.vrb 2>nul

echo.
echo ============================================================
echo Compilation terminee avec succes!
echo ============================================================
echo.
echo Le fichier PDF a ete genere: main.pdf
echo.

REM Ouvrir le PDF automatiquement
if exist main.pdf (
    echo Ouverture du PDF...
    start main.pdf
) else (
    echo ATTENTION: Le fichier main.pdf n'a pas ete trouve!
)

echo.
pause

