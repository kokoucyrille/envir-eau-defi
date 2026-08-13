#!/usr/bin/env python3
"""
Script de vérification de l'installation Streamlit
À exécuter après installation pour vérifier que tout fonctionne
"""

import sys
import importlib
from pathlib import Path

def check_python_version():
    """Vérifie la version Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠ Attention: Python 3.8+ est recommandé")
        return False
    return True

def check_dependencies():
    """Vérifie les dépendances installées"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'geopandas',
        'openpyxl'
    ]
    
    all_ok = True
    print("\nVérification des dépendances:")
    
    for package in required_packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'N/A')
            print(f"  ✓ {package:<15} {version}")
        except ImportError:
            print(f"  ✗ {package:<15} MANQUANT")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Vérifie la structure du projet"""
    base_path = Path(__file__).parent
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.streamlit/config.toml',
        'pages/home.py',
        'components/visualization.py',
        'utils/data_loader.py',
        'assets/logo.png'
    ]
    
    required_dirs = [
        'pages',
        'components',
        'utils',
        'assets',
        '.streamlit'
    ]
    
    print("\nVérification de la structure:")
    all_ok = True
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ Dossier {dir_name}/")
        else:
            print(f"  ✗ Dossier {dir_name}/ MANQUANT")
            all_ok = False
    
    for file_name in required_files:
        file_path = base_path / file_name
        if file_path.exists() and file_path.is_file():
            size = file_path.stat().st_size
            print(f"  ✓ Fichier {file_name:<40} ({size:,} bytes)")
        else:
            print(f"  ✗ Fichier {file_name} MANQUANT")
            all_ok = False
    
    return all_ok

def check_imports():
    """Vérifie que les imports principaux fonctionnent"""
    print("\nVérification des imports:")
    
    try:
        import streamlit as st
        print("  ✓ import streamlit")
    except ImportError:
        print("  ✗ import streamlit ÉCHOUÉ")
        return False
    
    try:
        import pandas as pd
        print("  ✓ import pandas")
    except ImportError:
        print("  ✗ import pandas ÉCHOUÉ")
        return False
    
    try:
        import plotly.graph_objects as go
        print("  ✓ import plotly")
    except ImportError:
        print("  ✗ import plotly ÉCHOUÉ")
        return False
    
    try:
        import geopandas as gpd
        print("  ✓ import geopandas")
    except ImportError:
        print("  ✗ import geopandas ÉCHOUÉ")
        return False
    
    # Vérifier les modules locaux
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from utils.data_loader import load_all_data
        print("  ✓ import utils.data_loader")
    except ImportError as e:
        print(f"  ✗ import utils.data_loader ÉCHOUÉ: {e}")
        return False
    
    try:
        from components.visualization import display_metric_card
        print("  ✓ import components.visualization")
    except ImportError as e:
        print(f"  ✗ import components.visualization ÉCHOUÉ: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("VÉRIFICATION DE L'INSTALLATION STREAMLIT")
    print("Diagnostic - Accès Eau Potable Togo")
    print("="*60 + "\n")
    
    checks = [
        ("Python", check_python_version),
        ("Dépendances", check_dependencies),
        ("Structure", check_project_structure),
        ("Imports", check_imports)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Erreur lors de {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    
    all_ok = True
    for name, result in results:
        status = "✓ OK" if result else "✗ ÉCHEC"
        print(f"{name:<20} {status}")
        if not result:
            all_ok = False
    
    print("="*60 + "\n")
    
    if all_ok:
        print("✓ TOUS LES VÉRIFICATIONS PASSÉES")
        print("\nPour lancer l'application:")
        print("  streamlit run app.py")
        print("\nL'application s'ouvrira à: http://localhost:8501\n")
        return 0
    else:
        print("✗ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ")
        print("\nPour corriger:")
        print("  pip install -r requirements.txt\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
