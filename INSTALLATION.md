# INSTALLATION ET DÉPLOIEMENT

## Installation en Local (Recommandé pour développement)

### Prérequis
- Windows 10/11 ou macOS/Linux
- Python 3.8+ installé
- 2 GB d'espace disque libre
- Accès internet pour télécharger les dépendances

### Étapes d'Installation

#### 1. Vérifier Python
```bash
python --version
pip --version
```

#### 2. Naviguer vers le dossier
```bash
cd "c:\Users\DELL Precision\Downloads\Streamlit_EauTogo"
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Lancer l'application
```bash
streamlit run app.py
```

#### 5. Accéder à l'application
- Automatiquement : http://localhost:8501
- Manuellement : Ouvrir le navigateur et aller à http://localhost:8501

---

## Déploiement sur Streamlit Cloud (Gratuit)

### Avantages
- Gratuit jusqu'à 3 applications
- Accès public via URL
- Auto-déploiement via GitHub
- HTTPS automatique

### Étapes

#### 1. Créer un compte GitHub
- https://github.com/signup
- Créer un repository public nommé `streamlit-eau-togo`

#### 2. Pousser le code vers GitHub
```bash
cd c:\Users\DELL Precision\Downloads\Streamlit_EauTogo
git init
git add .
git commit -m "Application Streamlit Eau Potable Togo"
git branch -M main
git remote add origin https://github.com/votre-username/streamlit-eau-togo.git
git push -u origin main
```

#### 3. Déployer sur Streamlit Cloud
- Aller à https://share.streamlit.io
- S'identifier avec GitHub
- Cliquer "New app"
- Sélectionner le repository et la branche `main`
- Fichier: `app.py`
- Cliquer "Deploy"

#### 4. Accéder à l'application
- URL: https://votre-username-streamlit-eau-togo.streamlit.app
- Partager l'URL publiquement

---

## Déploiement sur Serveur Personnel (Linux/Ubuntu)

### Prérequis
- Serveur Linux/Ubuntu avec accès SSH
- Nom de domaine (optionnel)
- Certificat SSL (optionnel, pour HTTPS)

### Installation sur Serveur

#### 1. Connexion SSH
```bash
ssh utilisateur@adresse_ip
```

#### 2. Installation de Python et dépendances
```bash
sudo apt-get update
sudo apt-get install python3.11 python3-pip git
```

#### 3. Cloner le repository
```bash
git clone https://github.com/votre-username/streamlit-eau-togo.git
cd streamlit-eau-togo
```

#### 4. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

#### 5. Lancer l'application en background (avec tmux)
```bash
tmux new-session -d -s streamlit
tmux send-keys -t streamlit "streamlit run app.py --server.port 8080 --server.address 0.0.0.0" Enter
```

#### 6. Vérifier que l'app fonctionne
```bash
curl http://localhost:8080
```

### Configuration Nginx (Proxy Inverse)

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Configuration SSL (Let's Encrypt)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

---

## Déploiement avec Docker

### Créer Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

### Build et Run
```bash
docker build -t streamlit-eau-togo .
docker run -p 8080:8080 streamlit-eau-togo
```

### Avec Docker Compose

```yaml
version: '3.8'
services:
  streamlit:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8080
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## Dépannage d'Installation

### "Python not found"
```bash
# Ajouter Python au PATH (Windows)
# Réinstaller Python en cochant "Add Python to PATH"
```

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### "GeoPandas import error"
```bash
# GeoPandas nécessite GDAL
# Windows: Utiliser Conda
conda create -n eau-togo python=3.11
conda activate eau-togo
conda install geopandas plotly pandas streamlit
```

### L'app démarre mais les données ne s'affichent pas
1. Vérifier que le dossier source d'Eau-Defi1 est accessible
2. Vérifier les chemins dans `utils/data_loader.py`
3. Vérifier que les fichiers données existent

### Port 8501 déjà utilisé
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

---

## Configuration Avancée

### Variables d'Environnement
```bash
# Pour production
set STREAMLIT_SERVER_PORT=8080
set STREAMLIT_SERVER_ADDRESS=0.0.0.0
set STREAMLIT_SERVER_HEADLESS=true
```

### Configuration personnalisée (.streamlit/config.toml)
```toml
[server]
port = 8080
address = "0.0.0.0"
headless = true
maxUploadSize = 200

[logger]
level = "info"

[client]
toolbarMode = "minimal"
```

### Performance
```toml
[client]
showErrorDetails = false
toolbarMode = "minimal"

[logger]
level = "warning"
```

---

## Mise à Jour de l'Application

### En local
```bash
cd c:\Users\DELL Precision\Downloads\Streamlit_EauTogo
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

### Sur Streamlit Cloud
- Les changements pushés sur GitHub se déploient automatiquement

### Sur serveur personnel
```bash
cd /chemin/streamlit-eau-togo
git pull origin main
pip install -r requirements.txt --upgrade
# Redémarrer le service si utilisé avec systemd
```

---

## Monitoring et Logs

### Logs locaux
```bash
# Affichage détaillé
streamlit run app.py --logger.level=debug
```

### Logs serveur (Linux)
```bash
journalctl -u streamlit -f  # Si utilisation systemd
tail -f ~/.streamlit/logs/*  # Fichiers de log
```

### Monitoring performance
- Dashboard Streamlit : http://localhost:8501
- Monitor CPU/RAM : `streamlit run app.py --logger.level=debug`

---

## Maintenance

### Mise en cache du navigateur
```python
# Forcer le rechargement (Ctrl+Maj+R ou Cmd+Shift+R)
```

### Vider le cache Streamlit
```bash
# Windows
del %appdata%\.streamlit\*

# macOS/Linux
rm -rf ~/.streamlit/*
```

### Sauvegarder les données
```bash
# Copier les fichiers de données importants
cp -r data/ backup_data_$(date +%Y%m%d)/
```

---

## Support

### Problèmes Courants

| Problème | Solution |
|----------|----------|
| App lente | Vérifier RAM disponible, réduire données |
| Erreur données | Vérifier chemins dans data_loader.py |
| Port occupé | Utiliser --server.port 8502 |
| Module manquant | Exécuter pip install -r requirements.txt |
| Pas de mise à jour | Actualiser (Ctrl+R ou Cmd+R) |

### Ressources
- Streamlit Docs: https://docs.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues
- Community: https://discuss.streamlit.io

---

## Checklist Post-Déploiement

- [ ] Application accessible et fonctionnelle
- [ ] Données chargées correctement
- [ ] Cartes interactives affichées
- [ ] Graphiques Plotly visibles
- [ ] Filtres et recherche opérationnels
- [ ] Téléchargements CSV/Excel fonctionnels
- [ ] Logo affiché
- [ ] Pas d'erreurs dans la console
- [ ] URL/domaine accessible publiquement (si déploiement public)
- [ ] HTTPS activé (si déploiement production)

---

**Application prête pour le déploiement !**
