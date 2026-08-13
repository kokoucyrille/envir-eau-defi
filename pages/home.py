"""
Page d'accueil du dashboard
"""

import streamlit as st
from pathlib import Path
from components.visualization import display_metric_card, display_info_box, display_kpi_section
from utils.data_loader import load_all_data

def render_home():
    """Affiche la page d'accueil"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="Diagnostic - Accès Eau Potable Togo",
        page_icon="📊",
        layout="wide"
    )
    
    # Header avec logo
    col_logo, col_title = st.columns([1, 4])
    
    with col_logo:
        try:
            st.image("assets/logo.png", width=100)
        except:
            st.write("[Logo]")
    
    with col_title:
        st.title("Diagnostic de l'Accès à l'Eau Potable au Togo")
        st.markdown("""
        **Plateforme d'Analyse et de Priorisation pour l'Intervention Publique**
        """)
    
    st.divider()
    
    # Chargement des données
    data = load_all_data()
    
    # Section KPI
    display_kpi_section(data)
    
    st.divider()
    
    # Vue d'ensemble
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Objectifs du Diagnostic")
        st.markdown("""
        1. **Audit exhaustif** - Évaluer l'accès à l'eau potable dans les 388 cantons
        2. **Identification des risques** - Analyser les zones à risque hydrique élevé
        3. **Priorisation** - Identifier les zones d'intervention prioritaire
        4. **Recommandations** - Proposer 5 axes d'action territorialisés
        5. **Visualisation** - Faciliter la prise de décision publique
        """)
    
    with col2:
        st.subheader("Critères d'Évaluation")
        st.markdown("""
        - **Ergonomie** - Navigation intuitive et claire
        - **Analyse** - Conclusions pertinentes basées sur les données
        - **Interaction** - Filtres et visualisations interactives
        - **Méthodologie** - Structure rigoureuse et transparente
        """)
    
    st.divider()
    
    # Résumé exécutif
    st.subheader("Résumé Exécutif")
    
    display_info_box(
        "Diagnostic Complet",
        "Cette plateforme fournit une analyse exhaustive de l'accès à l'eau potable au Togo "
        "avec priorisation des zones d'intervention et recommandations d'action.",
        "info"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_info_box(
            "Données",
            f"388 cantons analysés avec données géographiques, infrastructurelles et de risque",
            "success"
        )
    
    with col2:
        display_info_box(
            "Analyse",
            "Clustering spatial, scoring de priorisation et recommandations territorialisées",
            "success"
        )
    
    with col3:
        display_info_box(
            "Export",
            "11 fichiers de données prêts pour intégration dans des outils tiers",
            "success"
        )
    
    st.divider()
    
    # Guide de navigation
    st.subheader("Guide de Navigation")
    
    navigation_tabs = st.tabs(["Vue d'ensemble", "Comment utiliser", "Sections disponibles"])
    
    with navigation_tabs[0]:
        st.markdown("""
        **Cette plateforme permet de :**
        - Consulter les indicateurs clés (KPI) nationaux et régionaux
        - Explorer les données géographiques et spatiales
        - Analyser les risques hydrologiques par canton
        - Visualiser l'infrastructure existante
        - Consulter les recommandations d'action
        """)
    
    with navigation_tabs[1]:
        st.markdown("""
        1. Utilisez le menu de navigation à gauche pour accéder aux différentes sections
        2. Sélectionnez une région ou un canton pour filtrer les données
        3. Interagissez avec les graphiques (hover, zoom, sélection)
        4. Consultez les recommandations dans la dernière section
        """)
    
    with navigation_tabs[2]:
        st.markdown("""
        - **Accueil** - Vous êtes ici
        - **Diagnostique Spatial** - Analyse géographique et cartes
        - **Analyse Statistique** - Distributions et tendances
        - **Priorisation** - Scoring et recommandations
        - **Données Brutes** - Tables détaillées
        - **Méthodologie** - Documentation technique
        """)
    
    st.divider()
    
    # Pied de page
    st.caption("""
    **Plateforme de Diagnostic - Accès Eau Potable Togo**  
    Données et analyses basées sur FRI, infrastructure TdE et projets COSO.  
    Last updated: 2024
    """)

if __name__ == "__main__":
    render_home()
