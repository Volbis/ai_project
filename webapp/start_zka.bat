@echo off
cd /d "%~dp0backend"
echo ================================================
echo    🚀 DEMARRAGE DE ZKA - DETECTION IA 🚀
echo ================================================
echo.
echo 📍 Repertoire: %CD%
echo 🎯 Application: ZKA Vision AI
echo 🤖 Technologie: YOLOv5 + Intelligence Artificielle
echo.
echo ⏳ Chargement du modele IA en cours...
echo.
python main.py
echo.
echo ================================================
echo    ❌ SERVEUR ZKA ARRETE
echo ================================================
pause
