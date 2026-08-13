"""
Composants visuels réutilisables
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def display_metric_card(col, label, value, delta=None, color="primary"):
    """Affiche une carte KPI"""
    with col:
        if color == "primary":
            border_color = "#0066cc"
            bg_color = "#f0f6ff"
        elif color == "success":
            border_color = "#22c55e"
            bg_color = "#f0fdf4"
        elif color == "warning":
            border_color = "#f59e0b"
            bg_color = "#fffbeb"
        else:
            border_color = "#ef4444"
            bg_color = "#fef2f2"
            
        metric_html = f"""
        <div style="
            border-left: 4px solid {border_color};
            background-color: {bg_color};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
                {label}
            </p>
            <h3 style="margin: 8px 0 0 0; color: {border_color}; font-size: 32px; font-weight: bold;">
                {value}
            </h3>
            {f'<p style="margin: 8px 0 0 0; color: #22c55e; font-size: 12px;">{delta}</p>' if delta else ''}
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

def display_kpi_section(data):
    """Affiche les KPI principaux"""
    from utils.data_loader import get_kpi_summary
    
    kpis = get_kpi_summary(data)
    
    st.subheader("Indicateurs Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    display_metric_card(col1, "Cantons Analysés", f"{kpis.get('total_cantons', 0)}", color="primary")
    display_metric_card(col2, "Infrastructures TdE", f"{kpis.get('total_tde', 0)}", color="success")
    display_metric_card(col3, "Projets COSO", f"{kpis.get('total_projects', 0)}", color="warning")
    display_metric_card(col4, "Risque Moyen FRI", f"{kpis.get('fri_moyen', 0):.2f}", color="info")

def create_distribution_chart(data, column, title, color="viridis"):
    """Crée un graphique de distribution"""
    if column not in data.columns:
        return None
        
    dist_data = data[column].value_counts().head(10)
    
    fig = px.bar(
        x=dist_data.index,
        y=dist_data.values,
        title=title,
        labels={'x': column, 'y': 'Nombre'},
        color=dist_data.values,
        color_continuous_scale=color
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_regional_comparison(data):
    """Crée un graphique de comparaison régionale"""
    try:
        if 'region' not in data.columns:
            return None
            
        regional = data.groupby('region').agg({
            'population': 'sum' if 'population' in data.columns else 'count'
        }).reset_index()
        
        fig = px.bar(
            regional,
            x='region',
            y='population' if 'population' in data.columns else regional.columns[1],
            title='Comparaison par Région',
            color='region',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            hovermode='x unified',
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
    except:
        return None

def create_heatmap(data_matrix, title="Heatmap"):
    """Crée une heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data_matrix.values,
        x=data_matrix.columns,
        y=data_matrix.index,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def display_info_box(title, content, info_type="info"):
    """Affiche une boîte d'information"""
    icon_map = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✕"
    }
    
    color_map = {
        "info": "#0066cc",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
    
    bg_map = {
        "info": "#f0f6ff",
        "success": "#f0fdf4",
        "warning": "#fffbeb",
        "error": "#fef2f2"
    }
    
    box_html = f"""
    <div style="
        background-color: {bg_map[info_type]};
        border-left: 4px solid {color_map[info_type]};
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    ">
        <p style="margin: 0; color: {color_map[info_type]}; font-weight: bold; font-size: 14px;">
            {icon_map[info_type]} {title}
        </p>
        <p style="margin: 8px 0 0 0; color: #333; font-size: 13px;">
            {content}
        </p>
    </div>
    """
    
    st.markdown(box_html, unsafe_allow_html=True)
