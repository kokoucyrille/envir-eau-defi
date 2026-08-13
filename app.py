"""
Application Streamlit principale
Pages de navigation automatiques basées sur le dossier pages/
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Diagnostic - Eau Potable Togo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour l'interface
st.markdown("""
<style>
    /* Styles généraux */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header */
    h1 {
        color: #1a365d;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Cards et containers */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Selectbox et inputs */
    .stSelectbox, .stSlider, .stTextInput {
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## Navigation")
    st.markdown("---")
    
    page_options = {
        "Accueil": "home",
        "Analyse Spatiale": "spatial_analysis",
        "Analyse Statistique": "statistical_analysis",
        "Priorisation": "prioritization",
        "Données Brutes": "raw_data",
        "Méthodologie": "methodology"
    }
    
    selected = st.radio(
        "Sélectionnez une page:",
        list(page_options.keys()),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### A propos")
    st.markdown("""
    **Diagnostic de l'Accès à l'Eau Potable au Togo**
    
    Plateforme interactive pour:
    - Analyser l'accès à l'eau potable
    - Identifier les zones prioritaires
    - Prioriser les investissements publics
    - Formuler des recommandations d'action
    """)
    
    st.markdown("---")
    
    st.markdown("### Ressources")
    st.markdown("""
    - Documentation technique
    - Guide d'utilisation
    - Données sources
    - Méthodologie complète
    """)

# Chargement de la page sélectionnée
if selected == "Accueil":
    from pages.home import render_home
    render_home()
elif selected == "Analyse Spatiale":
    from pages.spatial_analysis import render_spatial_analysis
    render_spatial_analysis()
elif selected == "Analyse Statistique":
    from pages.statistical_analysis import render_statistical_analysis
    render_statistical_analysis()
elif selected == "Priorisation":
    from pages.prioritization import render_prioritization
    render_prioritization()
elif selected == "Données Brutes":
    from pages.raw_data import render_raw_data
    render_raw_data()
elif selected == "Méthodologie":
    from pages.methodology import render_methodology
    render_methodology()
