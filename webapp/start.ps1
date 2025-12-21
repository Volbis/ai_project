# YOLOv5 Web Application - Startup Script
# Lancement automatique du serveur FastAPI avec interface web

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   YOLOv5 Web Application Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python detecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python non trouvé! Installez Python d'abord." -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

Write-Host ""
Write-Host "📦 Vérification des dépendances..." -ForegroundColor Yellow

# Check if requirements are installed
$requirementsFile = Join-Path $backendPath "requirements.txt"
if (Test-Path $requirementsFile) {
    Write-Host "Installation/Mise à jour des dépendances..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    Write-Host "✓ Dépendances installées" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Démarrage du serveur YOLOv5..." -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "  Application Web: http://localhost:8000" -ForegroundColor Green
Write-Host "  API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  WebSocket: ws://localhost:8000/ws" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""
Write-Host "💡 Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Start the FastAPI server
python main.py
