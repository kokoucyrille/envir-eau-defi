#!/bin/bash
# Script de démarrage de l'application Streamlit
# Pour macOS/Linux

echo ""
echo "======================================"
echo "Application Streamlit - Eau Potable Togo"
echo "======================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "Erreur: Python 3 n'est pas installé"
    exit 1
fi

echo "Vérification de l'installation..."
echo ""

# Vérifier et installer les dépendances
python3 -c "import streamlit" 2>/dev/null || { echo "Installation de Streamlit..."; pip install streamlit; }
python3 -c "import pandas" 2>/dev/null || { echo "Installation de Pandas..."; pip install pandas; }
python3 -c "import geopandas" 2>/dev/null || { echo "Installation de GeoPandas..."; pip install geopandas; }
python3 -c "import plotly" 2>/dev/null || { echo "Installation de Plotly..."; pip install plotly; }

echo ""
echo "======================================"
echo "Lancement de l'application..."
echo "======================================"
echo ""
echo "L'application s'ouvre dans votre navigateur à:"
echo "http://localhost:8501"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

# Lancer l'application
streamlit run app.py
