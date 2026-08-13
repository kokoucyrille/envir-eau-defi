# Guide de Démarrage Rapide - Application Streamlit

## Installation Rapide (5 minutes)

### Étape 1: Installer les dépendances
```bash
cd c:\Users\DELL Precision\Downloads\Streamlit_EauTogo
pip install -r requirements.txt
```

### Étape 2: Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur.

---

## Structure de l'Application

La plateforme est organisée en **6 sections principales** :

### 1. **Accueil** - Point de départ
- Vue d'ensemble du projet
- Indicateurs clés (KPI)
- Objectifs et critères d'évaluation
- Guide de navigation

### 2. **Analyse Spatiale** - Cartes interactives
- Cartographie du risque FRI (choroplèthe)
- Localisation infrastructure TdE
- Projets COSO
- Filtres par région
- Statistiques spatiales

### 3. **Analyse Statistique** - Données et tendances
- Distribution FRI par classe
- Statistiques descriptives
- Analyse infrastructure
- Données projets
- Matrice de corrélation

### 4. **Priorisation** - Zones d'action
- Scoring de priorisation (0-100)
- Top 20 zones prioritaires
- 4 niveaux de recommandations
- Plans d'action régionaux
- Budget prévisionnel 3 ans

### 5. **Données Brutes** - Accès complet
- Tous les datasets disponibles
- Recherche et filtrage
- Statistiques par dataset
- Téléchargement CSV/Excel

### 6. **Méthodologie** - Documentation
- Contexte du projet
- Sources de données
- Approche technique
- Limitations importantes
- Glossaire

---

## Critères d'Évaluation

L'application respecte les 4 critères d'évaluation :

### ✓ Ergonomie, Clarté Visuelle et Facilité de Navigation
- Navigation intuitive avec menu latéral
- Pages structurées avec sections claires
- KPI visualisés en cartes colorées
- Interface professionnelle sans emojis
- Responsive design

### ✓ Pertinence des Analyses et Qualité des Conclusions
- Analyses basées sur données réelles du notebook
- Scoring méthodologiquement justifié
- Statistiques complètes et vérifiables
- Recommandations territorialisées par région
- Documentation technique rigoureuse

### ✓ Richesse des Interactions et Filtres
- Filtrage par région et plage FRI
- Sélection multi-dataset
- Recherche dans les données
- Graphiques Plotly interactifs (zoom, hover, export)
- Tableaux filtrables et téléchargeables

### ✓ Structure, Clarté et Méthodologie
- Architecture modulaire et maintenable
- Code documenté et organisé
- Sections logiques et progressives
- Rédaction professionnelle
- README complet

---

## Utilisation Recommandée

### Profil : Évaluateur
1. Lire **Accueil** (2 min)
2. Consulter **Analyse Spatiale** (5 min)
3. Vérifier **Méthodologie** → Limitations (3 min)
4. Examiner **Données Brutes** pour détails (5 min)

### Profil : Décideur Politique
1. Lire **Accueil** (2 min)
2. Consulter **Priorisation** → Recommandations (5 min)
3. Examiner **Analyse Spatiale** pour contexte régional (5 min)
4. Vérifier Budget dans **Priorisation** (2 min)

### Profil : Analyste de Données
1. Consulter **Méthodologie** (10 min)
2. Explorer **Analyse Statistique** (10 min)
3. Examiner **Données Brutes** (10 min)
4. Télécharger datasets pour analyse complémentaire

### Profil : Technicien IT
1. Consulter **README.md** (architecture)
2. Adapter **data_loader.py** pour nouvelles données
3. Configurer déploiement (Streamlit Cloud ou serveur)

---

## Fichiers Clés et Leur Rôle

| Fichier | Rôle |
|---------|------|
| `app.py` | Application principale, navigation |
| `requirements.txt` | Dépendances Python |
| `README.md` | Documentation complète |
| `pages/home.py` | Page d'accueil |
| `pages/spatial_analysis.py` | Analyse géographique |
| `pages/statistical_analysis.py` | Statistiques et distributions |
| `pages/prioritization.py` | Priorisation et recommandations |
| `pages/raw_data.py` | Accès données brutes |
| `pages/methodology.py` | Documentation technique |
| `utils/data_loader.py` | Chargement et cache données |
| `components/visualization.py` | Fonctions de visualisation |
| `assets/logo.png` | Logo du ministère |

---

## Données Utilisées

L'application utilise les fichiers de données du dossier source :
- **fri-cantons.gpkg** - Données géographiques FRI (388 cantons)
- **chateaux-deau-forages-tde.csv** - Infrastructure TdE (67 points)
- **projet-coso-eau.geojson** - Projets COSO (218 projets)
- **communautes_louvain_*.csv** - Clusters et profils spatiaux
- **kpi_reseau_louvain.csv** - Indicateurs réseau par cluster

---

## Fonctionnalités Interactives

### Cartes
- Zoom et pan sur les régions
- Hover pour voir les détails par canton
- Export en image PNG
- Sélection par région

### Graphiques
- Hover pour voir les valeurs
- Zoom/pan sur zones intéressantes
- Export en image
- Sélection interactive de données

### Tableaux
- Tri par colonne (click sur header)
- Recherche textuelle
- Pagination automatique
- Téléchargement en CSV/Excel

### Filtres
- Sélection multi-région
- Plage FRI ajustable
- Types de visualisation
- Colonnes de recherche

---

## Optimisation des Performances

L'application utilise plusieurs techniques pour être rapide :

1. **Cache des données** : Les données sont chargées une seule fois avec `@st.cache_resource`
2. **Cache des calculs** : Les statistiques sont calculées une fois avec `@st.cache_data`
3. **Lazy loading** : Les visualisations se chargent à la demande
4. **Compression** : Les données sont compressées lors du chargement

---

## Dépannage

### L'app ne démarre pas
```bash
# Vérifier Python et pip
python --version
pip --version

# Réinstaller les dépendances
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Les données ne s'affichent pas
1. Vérifier que le dossier source est accessible
2. Vérifier les chemins dans `utils/data_loader.py`
3. Consulter les messages d'erreur Streamlit
4. Vérifier les formats de fichier (GeoPackage, CSV, GeoJSON)

### Application lente
1. Réduire la taille des données
2. Augmenter le cache
3. Vérifier la connexion réseau
4. Redémarrer l'application

---

## Points de Personnalisation

### Changer le logo
- Remplacer `assets/logo.png` par votre image
- Redémarrer l'application

### Adapter les seuils FRI
- Éditer `pages/prioritization.py`
- Modifier les seuils dans `st.slider()`

### Personnaliser les couleurs
- Éditer `app.py` (section CSS)
- Modifier les codes couleurs (ex: `#667eea`)

### Ajouter une nouvelle page
1. Créer `pages/nouvelle_page.py`
2. Ajouter une fonction `render_nouvelle_page()`
3. Ajouter à la navigation dans `app.py`

---

## Support des Formats

### Formats de données supportés
- CSV (Comma Separated Values)
- GeoPackage (.gpkg)
- GeoJSON (.geojson)
- Excel (.xlsx)

### Formats d'export
- CSV
- Excel (.xlsx)
- PNG (graphiques)
- HTML (pages)

---

## Prochaines Étapes

### 1. Vérifier l'installation
```bash
streamlit --version
python -c "import geopandas; print(geopandas.__version__)"
```

### 2. Lancer l'application
```bash
streamlit run app.py
```

### 3. Consulter l'accueil
- Accueil → Vue d'ensemble → Utilisation

### 4. Explorer les sections
- Commencer par Analyse Spatiale
- Puis Priorisation
- Consulter Méthodologie pour les limites

---

## Ressources Supplémentaires

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python
- **GeoPandas Docs**: https://geopandas.org
- **Pandas Docs**: https://pandas.pydata.org

---

**Application prête à l'emploi !**  
Consultez l'accueil pour un guide détaillé de chaque section.

