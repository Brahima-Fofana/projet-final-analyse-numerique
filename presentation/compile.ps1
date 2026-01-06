# ==============================================================================
# Script PowerShell de compilation LaTeX avec vérification d'erreurs
# ==============================================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Compilation de la présentation LaTeX - Analyse Numérique" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si pdflatex est disponible
$pdflatexPath = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $pdflatexPath) {
    Write-Host "ERREUR: pdflatex n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer MiKTeX ou TeX Live:" -ForegroundColor Yellow
    Write-Host "  - MiKTeX: https://miktex.org/" -ForegroundColor Yellow
    Write-Host "  - TeX Live: https://tug.org/texlive/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host "pdflatex trouvé: $($pdflatexPath.Source)" -ForegroundColor Green
Write-Host ""

# Étape 1: Première compilation
Write-Host "[1/3] Première compilation avec pdflatex..." -ForegroundColor Yellow
$output1 = pdflatex -interaction=nonstopmode -file-line-error main.tex 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERREUR lors de la première compilation!" -ForegroundColor Red
    Write-Host "Consultez le fichier main.log pour plus de détails." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Dernières lignes du log:" -ForegroundColor Yellow
    Get-Content main.log -Tail 20
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host "Première compilation réussie." -ForegroundColor Green
Write-Host ""

# Étape 2: Seconde compilation (pour les références et la table des matières)
Write-Host "[2/3] Seconde compilation (pour les références)..." -ForegroundColor Yellow
$output2 = pdflatex -interaction=nonstopmode -file-line-error main.tex 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERREUR lors de la seconde compilation!" -ForegroundColor Red
    Write-Host "Consultez le fichier main.log pour plus de détails." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Dernières lignes du log:" -ForegroundColor Yellow
    Get-Content main.log -Tail 20
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host "Seconde compilation réussie." -ForegroundColor Green
Write-Host ""

# Étape 3: Nettoyage des fichiers auxiliaires
Write-Host "[3/3] Nettoyage des fichiers auxiliaires..." -ForegroundColor Yellow
$filesToRemove = @("*.aux", "*.log", "*.out", "*.nav", "*.snm", "*.toc", "*.vrb")
foreach ($pattern in $filesToRemove) {
    Remove-Item $pattern -ErrorAction SilentlyContinue
}
Write-Host "Nettoyage terminé." -ForegroundColor Green
Write-Host ""

# Vérifier que le PDF a été créé
if (Test-Path "main.pdf") {
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "Compilation terminée avec succès!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Le fichier PDF a été généré: main.pdf" -ForegroundColor Green
    Write-Host ""

    # Obtenir la taille du fichier
    $pdfFile = Get-Item "main.pdf"
    $sizeKB = [math]::Round($pdfFile.Length / 1KB, 2)
    Write-Host "Taille du fichier: $sizeKB KB" -ForegroundColor Cyan
    Write-Host ""

    # Ouvrir le PDF automatiquement
    Write-Host "Ouverture du PDF..." -ForegroundColor Cyan
    Start-Process "main.pdf"

} else {
    Write-Host "ATTENTION: Le fichier main.pdf n'a pas été trouvé!" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Read-Host "Appuyez sur Entrée pour quitter"

