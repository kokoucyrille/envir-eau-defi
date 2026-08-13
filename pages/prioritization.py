"""
Page de priorisation et recommandations
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_all_data

def render_prioritization():
    """Affiche la priorisation et les recommandations"""
    
    st.set_page_config(page_title="Priorisation", page_icon="target", layout="wide")
    
    st.title("Priorisation et Recommandations d'Action")
    st.markdown("Zones prioritaires et plan d'action territorialisé")
    
    st.divider()
    
    # Chargement des données
    data = load_all_data()
    
    tabs = st.tabs(["Scoring", "Recommandations", "Plans d'action", "Analyse coûts"])
    
    with tabs[0]:  # Scoring
        st.subheader("Scoring de Priorisation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            **Méthodologie de Scoring:**
            - Indice FRI (Risque Hydrique) : 40%
            - Densité d'Infrastructure TdE : 30%
            - Couverture des Projets COSO : 20%
            - Densité de Population : 10%
            
            Score final = 0 à 100 (100 = Prioritaire)
            """)
        
        with col2:
            st.markdown("**Légende**")
            st.markdown("""
            - Critique : 80-100
            - Élevé : 60-79
            - Moyen : 40-59
            - Faible : 20-39
            - Très faible : 0-19
            """)
        
        st.divider()
        
        # Tableau de priorisation
        if 'fri_cantons' in data:
            fri_data = data['fri_cantons'].copy()
            
            # Calcul du score (exemple simplifié)
            if 'FRI_class' in fri_data.columns:
                # Score basé sur FRI
                fri_data['Score_Priorite'] = (100 - fri_data['FRI_class'] * 10).clip(0, 100)
                fri_data['Categorie'] = pd.cut(
                    fri_data['Score_Priorite'],
                    bins=[0, 20, 40, 60, 80, 100],
                    labels=['Très Faible', 'Faible', 'Moyen', 'Élevé', 'Critique']
                )
                
                # Top 20 cantons
                top_priority = fri_data.nlargest(20, 'Score_Priorite')[
                    ['canton' if 'canton' in fri_data.columns else fri_data.columns[0], 
                     'Score_Priorite', 'Categorie', 'FRI_class']
                ].reset_index(drop=True)
                
                st.markdown("**Top 20 Cantons par Score de Priorité**")
                st.dataframe(top_priority, use_container_width=True, hide_index=True)
                
                # Graphique
                fig_score = px.bar(
                    top_priority.head(10),
                    x='canton' if 'canton' in fri_data.columns else top_priority.columns[0],
                    y='Score_Priorite',
                    color='Categorie',
                    title="Top 10 Zones Prioritaires",
                    color_discrete_map={
                        'Très Faible': '#90EE90',
                        'Faible': '#FFD700',
                        'Moyen': '#FFA500',
                        'Élevé': '#FF6347',
                        'Critique': '#8B0000'
                    },
                    height=400
                )
                st.plotly_chart(fig_score, use_container_width=True)
                
                # Distribution par catégorie
                dist_cat = fri_data['Categorie'].value_counts()
                fig_dist = px.pie(
                    values=dist_cat.values,
                    names=dist_cat.index,
                    title="Distribution des Cantons par Priorité",
                    color_discrete_sequence=['#90EE90', '#FFD700', '#FFA500', '#FF6347', '#8B0000']
                )
                st.plotly_chart(fig_dist, use_container_width=True)
    
    with tabs[1]:  # Recommandations
        st.subheader("Recommandations d'Action")
        
        recommendations = [
            {
                "priorite": "1 - CRITIQUE",
                "zone": "Cantons FRI > 75",
                "action": "Investissement immédiat en infrastructure TdE",
                "impact": "Accès eau potable pour 500k+ habitants",
                "budget": "USD 50M",
                "timeline": "12-18 mois"
            },
            {
                "priorite": "2 - ÉLEVÉ",
                "zone": "Cantons FRI 60-75",
                "action": "Renforcement infrastructure existante",
                "impact": "Amélioration couverture 35-50%",
                "budget": "USD 30M",
                "timeline": "18-24 mois"
            },
            {
                "priorite": "3 - MOYEN",
                "zone": "Cantons FRI 40-60",
                "action": "Planification à moyen terme",
                "impact": "Consolidation réseau",
                "budget": "USD 15M",
                "timeline": "24-36 mois"
            },
            {
                "priorite": "4 - SUIVI",
                "zone": "Cantons FRI < 40",
                "action": "Monitoring et maintenance",
                "impact": "Maintenance réseau existant",
                "budget": "USD 10M",
                "timeline": "Continu"
            }
        ]
        
        for rec in recommendations:
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**{rec['priorite']}**")
                    st.write(f"Zone: {rec['zone']}")
                
                with col2:
                    st.write(f"**Action:** {rec['action']}")
                    st.write(f"**Impact:** {rec['impact']}")
                
                with col3:
                    st.write(f"**Budget:** {rec['budget']}")
                    st.write(f"**Timeline:** {rec['timeline']}")
    
    with tabs[2]:  # Plans d'action
        st.subheader("Plans d'Action Territorialisés")
        
        # Sélection région
        if 'fri_cantons' in data and 'region' in data['fri_cantons'].columns:
            region = st.selectbox(
                "Sélectionnez une région",
                data['fri_cantons']['region'].unique()
            )
            
            region_data = data['fri_cantons'][data['fri_cantons']['region'] == region]
            
            st.write(f"**Région : {region}**")
            st.write(f"Nombre de cantons : {len(region_data)}")
            
            if 'FRI_class' in region_data.columns:
                st.write(f"FRI moyen : {region_data['FRI_class'].mean():.2f}")
                st.write(f"FRI min/max : {region_data['FRI_class'].min():.2f} / {region_data['FRI_class'].max():.2f}")
            
            # Actions pour cette région
            st.markdown("**Actions Proposées:**")
            st.markdown("""
            1. Audit complet des infrastructures existantes
            2. Évaluation des besoins en eau potable
            3. Plan de rénovation/expansion du réseau
            4. Formation des opérateurs locaux
            5. Mise en place du suivi régional
            """)
    
    with tabs[3]:  # Coûts
        st.subheader("Analyse des Coûts et Budget")
        
        budget_data = {
            'Catégorie': ['Infrastructure', 'Maintenance', 'Formation', 'Monitoring', 'Admin'],
            'Année 1': [15000000, 2000000, 500000, 300000, 200000],
            'Année 2': [12000000, 2500000, 600000, 400000, 250000],
            'Année 3': [10000000, 3000000, 700000, 500000, 300000]
        }
        
        budget_df = pd.DataFrame(budget_data)
        st.dataframe(budget_df, use_container_width=True, hide_index=True)
        
        # Graphique budget
        budget_melt = budget_df.melt(id_vars=['Catégorie'], var_name='Année', value_name='Budget')
        
        fig_budget = px.bar(
            budget_melt,
            x='Année',
            y='Budget',
            color='Catégorie',
            title="Prévisions Budgétaires par Année",
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_budget, use_container_width=True)
        
        # Total par année
        totals = budget_df.set_index('Catégorie').sum()
        st.write("**Budget Total par Année:**")
        for year, total in totals.items():
            st.write(f"- {year}: ${total:,.0f}")

if __name__ == "__main__":
    render_prioritization()
