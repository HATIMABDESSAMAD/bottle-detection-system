@echo off
REM ========================================
REM Lanceur Rapide - Unified Detection System
REM ========================================

echo.
echo ========================================
echo   SYSTEME UNIFIE DE DETECTION
echo   Bouteilles et Bouchons
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
    echo.
)

REM Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

REM Vérifier si les dépendances sont installées
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances...
    echo.
    pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependances installees
    echo.
)

REM Lancer l'application
echo [INFO] Lancement de l'application...
echo.
echo ========================================
echo.

python main.py

REM Fin
echo.
echo ========================================
echo   Application terminee
echo ========================================
pause
