"""
Page d'analyse statistique et distributions
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_all_data
from components.visualization import create_distribution_chart, create_regional_comparison

def render_statistical_analysis():
    """Affiche l'analyse statistique"""
    
    st.set_page_config(page_title="Analyse Statistique", page_icon="📈", layout="wide")
    
    st.title("Analyse Statistique et Distributions")
    st.markdown("Exploration des données : distributions, tendances et corrélations")
    
    st.divider()
    
    # Chargement des données
    data = load_all_data()
    
    # Onglets d'analyse
    tabs = st.tabs(["FRI Analysis", "Infrastructure", "Projets", "Corrélations"])
    
    with tabs[0]:  # FRI Analysis
        st.subheader("Analyse du Risque Hydrique (FRI)")
        
        if 'fri_cantons' in data:
            fri_data = data['fri_cantons']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Distribution FRI**")
                if 'FRI_class' in fri_data.columns:
                    fri_dist = fri_data['FRI_class'].value_counts().sort_index()
                    
                    fig_fri_dist = px.bar(
                        x=fri_dist.index,
                        y=fri_dist.values,
                        title="Distribution des Valeurs FRI",
                        labels={'x': 'Classe FRI', 'y': 'Nombre de Cantons'},
                        color=fri_dist.values,
                        color_continuous_scale="Viridis"
                    )
                    st.plotly_chart(fig_fri_dist, use_container_width=True)
            
            with col2:
                st.markdown("**Statistiques Descriptives**")
                if 'FRI_class' in fri_data.columns:
                    stats_df = pd.DataFrame({
                        'Statistique': ['Minimum', 'Quartile 25%', 'Médiane', 'Quartile 75%', 'Maximum', 'Moyenne'],
                        'Valeur': [
                            fri_data['FRI_class'].min(),
                            fri_data['FRI_class'].quantile(0.25),
                            fri_data['FRI_class'].median(),
                            fri_data['FRI_class'].quantile(0.75),
                            fri_data['FRI_class'].max(),
                            fri_data['FRI_class'].mean()
                        ]
                    })
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            # FRI par région
            if 'region' in fri_data.columns and 'FRI_class' in fri_data.columns:
                st.divider()
                st.markdown("**FRI par Région**")
                
                regional_fri = fri_data.groupby('region')['FRI_class'].agg(['mean', 'min', 'max', 'count']).round(2)
                
                fig_regional = px.bar(
                    regional_fri.reset_index(),
                    x='region',
                    y='mean',
                    error_y='max',
                    title="FRI Moyen par Région (avec min/max)",
                    labels={'mean': 'FRI Moyen', 'region': 'Région'},
                    color='mean',
                    color_continuous_scale="RdYlGn_r",
                    height=400
                )
                st.plotly_chart(fig_regional, use_container_width=True)
                
                st.dataframe(regional_fri, use_container_width=True)
    
    with tabs[1]:  # Infrastructure
        st.subheader("Analyse de l'Infrastructure TdE")
        
        if 'tde' in data and len(data['tde']) > 0:
            tde_data = data['tde']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total d'Infrastructures TdE", len(tde_data))
                
                # Distribution par type si disponible
                if 'type' in tde_data.columns or 'Type' in tde_data.columns:
                    type_col = 'type' if 'type' in tde_data.columns else 'Type'
                    type_dist = tde_data[type_col].value_counts()
                    
                    fig_type = px.pie(
                        values=type_dist.values,
                        names=type_dist.index,
                        title="Distribution par Type d'Infrastructure",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                st.markdown("**Colonnes disponibles**")
                st.write(tde_data.columns.tolist())
                
                # Statistiques de base
                st.markdown("**Aperçu des données**")
                st.dataframe(tde_data.head(5), use_container_width=True)
        
        else:
            st.info("Données TdE non disponibles")
    
    with tabs[2]:  # Projets
        st.subheader("Analyse des Projets COSO")
        
        if 'coso' in data:
            coso_data = data['coso']
            
            if isinstance(coso_data, dict):
                features = coso_data.get('features', [])
                nb_projects = len(features)
            else:
                nb_projects = len(coso_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total de Projets COSO", nb_projects)
            
            with col2:
                st.markdown("**Status des projets**")
                if isinstance(coso_data, dict):
                    # Analyse si structures disponibles
                    st.write("Données COSO chargées avec succès")
                else:
                    st.dataframe(coso_data.head(5), use_container_width=True)
    
    with tabs[3]:  # Corrélations
        st.subheader("Analyse des Corrélations")
        
        if 'fri_cantons' in data:
            fri_data = data['fri_cantons']
            
            # Colonnes numériques
            numeric_cols = fri_data.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) > 1:
                selected_cols = st.multiselect(
                    "Sélectionnez les colonnes pour la matrice de corrélation",
                    numeric_cols,
                    default=numeric_cols[:2]
                )
                
                if len(selected_cols) >= 2:
                    corr_matrix = fri_data[selected_cols].corr()
                    
                    fig_corr = px.imshow(
                        corr_matrix,
                        labels=dict(color="Corrélation"),
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        color_continuous_scale="RdBu",
                        zmin=-1,
                        zmax=1,
                        title="Matrice de Corrélation",
                        height=500
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("Pas assez de colonnes numériques pour l'analyse de corrélation")

if __name__ == "__main__":
    render_statistical_analysis()
