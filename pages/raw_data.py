"""
Page de données brutes
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

def render_raw_data():
    """Affiche les données brutes"""
    
    st.set_page_config(page_title="Données Brutes", page_icon="table", layout="wide")
    
    st.title("Données Brutes")
    st.markdown("Accès aux données détaillées et téléchargement")
    
    st.divider()
    
    # Chargement des données
    data = load_all_data()
    
    # Sélection du dataset
    datasets = {
        "FRI Cantons": "fri_cantons",
        "Infrastructure TdE": "tde",
        "Projets COSO": "coso",
        "KPI Réseau": "kpi_reseau",
        "Communes Louvain": "communes_cantons",
        "Profil Communes": "communes_profil",
        "Secteur Eau": "secteur_eau"
    }
    
    selected_dataset = st.selectbox(
        "Sélectionnez un dataset",
        list(datasets.keys())
    )
    
    dataset_key = datasets[selected_dataset]
    
    if dataset_key in data and data[dataset_key] is not None:
        df = data[dataset_key]
        
        # Info du dataset
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if hasattr(df, 'shape'):
                st.metric("Lignes", df.shape[0])
            else:
                st.metric("Éléments", len(df) if isinstance(df, list) else "N/A")
        
        with col2:
            if hasattr(df, 'shape'):
                st.metric("Colonnes", df.shape[1])
            else:
                st.metric("Type", type(df).__name__)
        
        with col3:
            if hasattr(df, 'memory_usage'):
                mem = df.memory_usage(deep=True).sum() / 1024 / 1024
                st.metric("Taille", f"{mem:.2f} MB")
        
        with col4:
            st.metric("Format", type(df).__name__)
        
        st.divider()
        
        # Affichage des données
        st.subheader(f"Aperçu de {selected_dataset}")
        
        if hasattr(df, 'columns'):
            # Filtrage
            col1, col2 = st.columns(2)
            
            with col1:
                rows_to_show = st.slider("Nombre de lignes", 5, 100, 20)
            
            with col2:
                search_col = st.selectbox("Colonne de recherche", ["Aucune"] + list(df.columns))
            
            # Application des filtres
            display_df = df.head(rows_to_show)
            
            if search_col != "Aucune":
                search_term = st.text_input(f"Recherche dans {search_col}")
                if search_term:
                    display_df = display_df[
                        display_df[search_col].astype(str).str.contains(search_term, case=False)
                    ]
            
            st.dataframe(display_df, use_container_width=True)
            
            # Statistiques
            st.divider()
            st.subheader("Statistiques Descriptives")
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                stats_df = df[numeric_cols].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
            else:
                st.info("Pas de colonnes numériques pour statistiques")
            
            # Téléchargement
            st.divider()
            st.subheader("Téléchargement")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f"{selected_dataset.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                xlsx = df.to_excel(index=False) if hasattr(df, 'to_excel') else None
                if xlsx:
                    st.download_button(
                        label="Télécharger Excel",
                        data=xlsx,
                        file_name=f"{selected_dataset.lower().replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        else:
            st.write("Format de données non compatible pour affichage tabulaire")
            st.write(type(df))
    
    else:
        st.warning(f"Dataset {selected_dataset} non disponible")

if __name__ == "__main__":
    render_raw_data()
