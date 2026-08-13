"""
Data loader pour l'application Streamlit
Charge et prépare les données depuis le notebook
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import os
from pathlib import Path

# Configuration des chemins
BASE_PATH = Path(__file__).parent.parent
DATA_SOURCE_PATH = Path("c:/Users/DELL Precision/Downloads/Eau-Defi1")

@st.cache_resource
def load_all_data():
    """Charge toutes les données nécessaires"""
    data = {}
    
    try:
        # Données FRI (Flood Risk Index)
        data['fri_cantons'] = gpd.read_file(
            DATA_SOURCE_PATH / "data" / "fri-cantons.gpkg"
        )
        
        # Données TdE (Châteaux d'eau)
        data['tde'] = pd.read_csv(
            DATA_SOURCE_PATH / "data" / "chateaux-deau-forages-tde.csv"
        )
        
        # Données COSO (Projets)
        data['coso'] = pd.read_json(
            DATA_SOURCE_PATH / "data" / "projet-coso-eau.geojson"
        )
        
        # KPI réseau
        data['kpi_reseau'] = pd.read_csv(
            DATA_SOURCE_PATH / "kpi_reseau_louvain.csv"
        )
        
        # Communautés Louvain
        data['communes_cantons'] = pd.read_csv(
            DATA_SOURCE_PATH / "communautes_louvain_cantons.csv"
        )
        
        data['communes_profil'] = pd.read_csv(
            DATA_SOURCE_PATH / "communautes_louvain_profil.csv"
        )
        
        # Secteur eau hydraulique
        data['secteur_eau'] = pd.read_csv(
            DATA_SOURCE_PATH / "data" / "subprojects-sector-eau-hydraulique.csv"
        )
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        
    return data

@st.cache_data
def get_kpi_summary(data):
    """Calcule les KPI principaux"""
    kpis = {}
    
    try:
        # Nombre de cantons
        kpis['total_cantons'] = len(data['fri_cantons'])
        
        # Nombre d'infrastructures TdE
        kpis['total_tde'] = len(data['tde'])
        
        # Nombre de projets COSO
        if isinstance(data['coso'], dict):
            kpis['total_projects'] = len(data['coso'].get('features', []))
        else:
            kpis['total_projects'] = len(data['coso'])
            
        # FRI moyen
        if 'FRI_class' in data['fri_cantons'].columns:
            kpis['fri_moyen'] = data['fri_cantons']['FRI_class'].mean()
        else:
            kpis['fri_moyen'] = 0
            
    except Exception as e:
        st.warning(f"Erreur lors du calcul des KPI : {str(e)}")
        
    return kpis

@st.cache_data
def get_regional_stats(data):
    """Calcule les statistiques par région"""
    try:
        if 'region' in data['fri_cantons'].columns:
            return data['fri_cantons'].groupby('region').size()
    except:
        pass
    return pd.Series()
