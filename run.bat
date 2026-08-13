@echo off
REM Script de démarrage de l'application Streamlit
REM Pour Windows

echo.
echo ======================================
echo Application Streamlit - Eau Potable Togo
echo ======================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Erreur: Python n'est pas installé ou n'est pas dans PATH
    pause
    exit /b 1
)

REM Vérifier pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo Erreur: pip n'est pas installé
    pause
    exit /b 1
)

echo Vérification de l'installation...
echo.

REM Vérifier les dépendances
python -c "import streamlit; print('OK: Streamlit')" >nul 2>&1
if errorlevel 1 (
    echo Installation de Streamlit...
    pip install streamlit
)

python -c "import pandas; print('OK: Pandas')" >nul 2>&1
if errorlevel 1 (
    echo Installation de Pandas...
    pip install pandas
)

python -c "import geopandas; print('OK: GeoPandas')" >nul 2>&1
if errorlevel 1 (
    echo Installation de GeoPandas...
    pip install geopandas
)

python -c "import plotly; print('OK: Plotly')" >nul 2>&1
if errorlevel 1 (
    echo Installation de Plotly...
    pip install plotly
)

echo.
echo ======================================
echo Lancement de l'application...
echo ======================================
echo.
echo L'application s'ouvre dans votre navigateur à:
echo http://localhost:8501
echo.
echo Appuyez sur Ctrl+C dans la console pour arrêter l'application
echo.

REM Lancer l'application
streamlit run app.py

pause
