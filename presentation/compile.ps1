# ============================================================================
# Script de compilation automatique pour présentation LaTeX Beamer
# ============================================================================
# Auteur : BRAHIMA FOFANA
# Date   : 13 janvier 2026
# Usage  : .\compile.ps1
# ============================================================================

# Configuration
$TexFile = "main.tex"
$PdfFile = "main.pdf"
$TempFiles = @("*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm", "*.vrb", "*.synctex.gz")

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

function Write-StepHeader {
    param([string]$Message)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[✗] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[i] $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

function Remove-TempFiles {
    Write-Info "Nettoyage des fichiers temporaires..."
    $removed = 0
    foreach ($pattern in $TempFiles) {
        $files = Get-ChildItem -Path . -Filter $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            try {
                Remove-Item $file.FullName -Force -ErrorAction Stop
                $removed++
            } catch {
                Write-Warning "Impossible de supprimer: $($file.Name)"
            }
        }
    }
    if ($removed -gt 0) {
        Write-Success "Supprimé $removed fichier(s) temporaire(s)"
    }
}

function Close-PdfIfOpen {
    param([string]$PdfPath)

    # Tenter de fermer le PDF s'il est ouvert
    $pdfProcesses = Get-Process | Where-Object {
        $_.MainWindowTitle -like "*$PdfFile*" -or
        $_.ProcessName -eq "AcroRd32" -or
        $_.ProcessName -eq "Acrobat"
    }

    if ($pdfProcesses) {
        Write-Info "Tentative de fermeture du PDF ouvert..."
        foreach ($proc in $pdfProcesses) {
            try {
                $proc.CloseMainWindow() | Out-Null
                Start-Sleep -Milliseconds 500
                if (-not $proc.HasExited) {
                    $proc.Kill()
                }
                Write-Success "PDF fermé"
            } catch {
                Write-Warning "Impossible de fermer le PDF automatiquement"
            }
        }
    }
}

# ============================================================================
# DÉBUT DU SCRIPT
# ============================================================================

Write-StepHeader "COMPILATION LATEX BEAMER"

# Étape 1 : Vérification de pdflatex
Write-Info "Vérification de l'installation de pdfLaTeX..."
try {
    $pdflatexCmd = Get-Command pdflatex -ErrorAction Stop
    Write-Success "pdfLaTeX trouvé: $($pdflatexCmd.Source)"
} catch {
    Write-Error "pdfLaTeX n'est pas installé ou non accessible dans le PATH"
    Write-Info "Installez MiKTeX (https://miktex.org) ou TeX Live (https://www.tug.org/texlive/)"
    exit 1
}

# Étape 2 : Vérification du fichier source
Write-Info "Vérification du fichier source..."
if (-not (Test-Path $TexFile)) {
    Write-Error "Le fichier '$TexFile' est introuvable"
    Write-Info "Répertoire actuel: $(Get-Location)"
    exit 1
}
Write-Success "Fichier source trouvé: $TexFile"

# Étape 3 : Nettoyage initial
Write-StepHeader "ÉTAPE 1/4 : NETTOYAGE INITIAL"
Remove-TempFiles

# Étape 4 : Fermeture et suppression de l'ancien PDF
if (Test-Path $PdfFile) {
    Write-Info "Un fichier PDF existe déjà"
    Close-PdfIfOpen -PdfPath $PdfFile

    try {
        Remove-Item $PdfFile -Force -ErrorAction Stop
        Write-Success "Ancien PDF supprimé"
    } catch {
        Write-Warning "Impossible de supprimer l'ancien PDF (peut-être ouvert)"
        Write-Info "Tentative de compilation malgré tout..."
    }
}

# Étape 5 : Première compilation
Write-StepHeader "ÉTAPE 2/4 : PREMIÈRE COMPILATION"
Write-Info "Génération du PDF et des fichiers auxiliaires..."

$startTime = Get-Date
$compile1 = Start-Process -FilePath "pdflatex" `
    -ArgumentList "-interaction=nonstopmode", "-halt-on-error", $TexFile `
    -NoNewWindow -Wait -PassThru

$duration1 = ((Get-Date) - $startTime).TotalSeconds

if ($compile1.ExitCode -eq 0) {
    Write-Success "Première compilation réussie (${duration1}s)"
} else {
    Write-Error "Échec de la première compilation"
    Write-Info "Consultez le fichier main.log pour les détails"

    if (Test-Path "main.log") {
        $errors = Select-String -Path "main.log" -Pattern "^!" | Select-Object -First 5
        if ($errors) {
            Write-Host ""
            Write-Warning "Premières erreurs détectées:"
            foreach ($err in $errors) {
                Write-Host "  $($err.Line)" -ForegroundColor Yellow
            }
        }
    }
    exit 1
}

# Étape 6 : Deuxième compilation
Write-StepHeader "ÉTAPE 3/4 : DEUXIÈME COMPILATION"
Write-Info "Mise à jour des références et de la table des matières..."

$startTime = Get-Date
$compile2 = Start-Process -FilePath "pdflatex" `
    -ArgumentList "-interaction=nonstopmode", "-halt-on-error", $TexFile `
    -NoNewWindow -Wait -PassThru

$duration2 = ((Get-Date) - $startTime).TotalSeconds

if ($compile2.ExitCode -eq 0) {
    Write-Success "Deuxième compilation réussie (${duration2}s)"
} else {
    Write-Warning "Avertissements lors de la deuxième compilation"
    Write-Info "Le PDF peut contenir des références non résolues"
}

# Étape 7 : Vérification du PDF
Write-StepHeader "ÉTAPE 4/4 : VÉRIFICATION ET FINALISATION"

if (-not (Test-Path $PdfFile)) {
    Write-Error "Le fichier PDF n'a pas été généré"
    Write-Info "Vérifiez le fichier main.log pour les erreurs"
    exit 1
}

$pdfInfo = Get-Item $PdfFile
$totalTime = $duration1 + $duration2

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   COMPILATION RÉUSSIE !                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Success "Fichier généré : $PdfFile"
Write-Success "Taille        : $([math]::Round($pdfInfo.Length / 1MB, 2)) Mo"
Write-Success "Temps total   : $([math]::Round($totalTime, 2))s"
Write-Success "Date          : $($pdfInfo.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Host ""

# Étape 8 : Nettoyage final
Write-Info "Nettoyage des fichiers temporaires..."
Start-Sleep -Milliseconds 500
Remove-TempFiles

# Étape 9 : Ouverture automatique du PDF
Write-Host ""
Write-Info "Ouverture du PDF..."
try {
    Start-Process $PdfFile
    Write-Success "PDF ouvert avec succès"
} catch {
    Write-Warning "Impossible d'ouvrir le PDF automatiquement"
    Write-Info "Ouvrez manuellement le fichier: $PdfFile"
}

Write-Host ""
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Script terminé avec succès" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

exit 0

