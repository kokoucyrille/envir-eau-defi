"""
Page d'analyse spatiale et cartographie
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_all_data

def render_spatial_analysis():
    """Affiche l'analyse spatiale"""
    
    st.set_page_config(page_title="Analyse Spatiale", page_icon="🗺", layout="wide")
    
    st.title("Analyse Spatiale et Cartographie")
    st.markdown("Visualisation des données géographiques, infrastructures et risques")
    
    st.divider()
    
    # Chargement des données
    data = load_all_data()
    
    if data and 'fri_cantons' in data:
        fri_cantons = data['fri_cantons']
        
        # Contrôles de filtrage
        st.subheader("Filtres et Sélections")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'region' in fri_cantons.columns:
                selected_region = st.multiselect(
                    "Région",
                    options=fri_cantons['region'].unique(),
                    default=fri_cantons['region'].unique()[:1] if len(fri_cantons) > 0 else []
                )
        
        with col2:
            if 'FRI_class' in fri_cantons.columns:
                fri_range = st.slider(
                    "Plage FRI",
                    min_value=float(fri_cantons['FRI_class'].min()) if 'FRI_class' in fri_cantons.columns else 0,
                    max_value=float(fri_cantons['FRI_class'].max()) if 'FRI_class' in fri_cantons.columns else 100,
                    value=(float(fri_cantons['FRI_class'].min()), float(fri_cantons['FRI_class'].max())) if 'FRI_class' in fri_cantons.columns else (0, 100)
                )
        
        with col3:
            view_type = st.selectbox(
                "Type de visualisation",
                ["Risque FRI", "Infrastructure TdE", "Projets COSO", "Clusters"]
            )
        
        st.divider()
        
        # Cartes
        st.subheader("Cartographie Interactive")
        
        # Carte 1 : FRI Choroplèthe
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Indice de Risque Hydrique (FRI) par Canton**")
            try:
                if 'FRI_class' in fri_cantons.columns and len(fri_cantons) > 0:
                    fig_fri = px.choropleth_mapbox(
                        fri_cantons,
                        locations="canton" if "canton" in fri_cantons.columns else fri_cantons.index,
                        color="FRI_class" if "FRI_class" in fri_cantons.columns else None,
                        hover_name="canton" if "canton" in fri_cantons.columns else None,
                        color_continuous_scale="RdYlGn_r",
                        title="FRI par Canton",
                        mapbox_style="open-street-map",
                        height=500,
                        zoom=4,
                        center={"lat": 8, "lon": 1}
                    )
                    st.plotly_chart(fig_fri, use_container_width=True)
                else:
                    st.info("Données FRI non disponibles pour la cartographie")
            except Exception as e:
                st.warning(f"Erreur cartographie FRI : {str(e)}")
        
        with col2:
            st.markdown("**Infrastructure TdE et Projets COSO**")
            try:
                if 'tde' in data and len(data['tde']) > 0:
                    tde_df = data['tde']
                    if 'latitude' in tde_df.columns and 'longitude' in tde_df.columns:
                        fig_tde = px.scatter_mapbox(
                            tde_df,
                            lat="latitude",
                            lon="longitude",
                            hover_name="id" if "id" in tde_df.columns else "Château d'eau",
                            color_discrete_sequence=["#1f77b4"],
                            title="Localisation TdE",
                            mapbox_style="open-street-map",
                            height=500,
                            zoom=4,
                            center={"lat": 8, "lon": 1}
                        )
                        st.plotly_chart(fig_tde, use_container_width=True)
                    else:
                        st.info("Coordonnées TdE non disponibles")
                else:
                    st.info("Données TdE non disponibles")
            except Exception as e:
                st.warning(f"Erreur cartographie TdE : {str(e)}")
        
        st.divider()
        
        # Statistiques spatiales
        st.subheader("Statistiques Spatiales")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            try:
                if 'region' in fri_cantons.columns:
                    nb_regions = fri_cantons['region'].nunique()
                    st.metric("Nombre de Régions", nb_regions)
            except:
                st.metric("Nombre de Régions", "N/A")
        
        with stat_col2:
            try:
                if 'FRI_class' in fri_cantons.columns:
                    fri_mean = fri_cantons['FRI_class'].mean()
                    st.metric("FRI Moyen", f"{fri_mean:.2f}")
            except:
                st.metric("FRI Moyen", "N/A")
        
        with stat_col3:
            try:
                if 'tde' in data:
                    nb_tde = len(data['tde'])
                    st.metric("Infrastructure TdE", nb_tde)
            except:
                st.metric("Infrastructure TdE", "N/A")
        
        st.divider()
        
        # Analyse régionale détaillée
        st.subheader("Distribution Régionale")
        
        try:
            if 'region' in fri_cantons.columns:
                regional_stats = fri_cantons.groupby('region').agg({
                    'canton' if 'canton' in fri_cantons.columns else fri_cantons.columns[0]: 'count',
                    'FRI_class' if 'FRI_class' in fri_cantons.columns else fri_cantons.columns[1]: 'mean'
                }).round(2)
                
                fig_regional = px.bar(
                    regional_stats.reset_index() if hasattr(regional_stats, 'reset_index') else regional_stats,
                    x="region" if 'region' in regional_stats.index.names else 0,
                    y=regional_stats.columns[0],
                    title="Nombre de Cantons par Région",
                    color_discrete_sequence=["#1f77b4"],
                    height=400
                )
                st.plotly_chart(fig_regional, use_container_width=True)
        except Exception as e:
            st.info("Statistiques régionales non disponibles")
    
    else:
        st.error("Données spatiales non disponibles")

if __name__ == "__main__":
    render_spatial_analysis()
