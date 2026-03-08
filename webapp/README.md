# YOLOv5 Web Application - Installation et Lancement

## 🚀 Installation Rapide

### 1. Installer les dépendances Python pour le backend

```bash
cd webapp/backend
pip install -r requirements.txt
```

### 2. Lancer l'application

**Option 1: Lancer avec le script PowerShell (Recommandé)**

```powershell
.\webapp\start.ps1
```

**Option 2: Lancer manuellement**

```bash
cd webapp/backend
python main.py
```

## 📱 Fonctionnalités

### ✅ Implémentées

- 🎥 **Détection en temps réel depuis la webcam** avec WebSocket
- 📤 **Upload drag-and-drop** d'images multiples
- 🎨 **Visualization interactive** des bounding boxes
- 📊 **Dashboard avec statistiques** en temps réel
- 🎯 **Suivi multi-objets** avec confiance
- 💾 **Historique des détections** persistent
- 🌙 **Mode sombre/clair** avec sauvegarde de préférence
- 📱 **Design responsive** mobile-friendly avec Tailwind CSS

### 🎨 Interface

- Design moderne avec Tailwind CSS
- Animations fluides et transitions
- Charts interactifs avec Chart.js
- Icons avec Font Awesome

## 🌐 Accès

Une fois lancé, l'application est accessible sur :

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## 📋 API Endpoints

### Détection

- `POST /detect` - Détecter objects dans une image
- `POST /detect/batch` - Détecter objects dans plusieurs images
- `GET /statistics` - Obtenir les statistiques
- `GET /history` - Obtenir l'historique
- `DELETE /history` - Effacer l'historique
- `GET /models` - Lister les modèles disponibles
- `WS /ws` - WebSocket pour détection temps réel

## 🛠️ Configuration

### Modèles disponibles:

- `yolov5n` - Nano (le plus rapide)
- `yolov5s` - Small (équilibré)
- `yolov5m` - Medium
- `yolov5l` - Large
- `yolov5x` - Extra Large (le plus précis)

### Paramètres ajustables:

- Seuil de confiance (0.1 - 0.9)
- Modèle YOLOv5
- Résolution vidéo webcam

## 🎯 Utilization

### Webcam en Direct

1. Cliquez sur l'onglet "Webcam en Direct"
2. Cliquez sur "Démarrer"
3. Autorisez l'accès à la webcam
4. Les détections apparaissent en temps réel !

### Upload d'Images

1. Cliquez sur l'onglet "Upload Images"
2. Glissez-déposez des images ou cliquez pour sélectionner
3. Cliquez sur "Analyzer les images"
4. Visualisez les résultats avec bounding boxes

### Dashboard

- Consultez les statistiques globales
- Visualisez les graphiques de performance
- Analysez les objects les plus détectés

### Historique

- Consultez toutes les détections précédentes
- Effacez l'historique si nécessaire

## 🔧 Troubleshooting

### Erreur de connection webcam

- Vérifiez les permissions du navigateur
- Assurez-vous qu'aucune autre application n'utilise la webcam

### Erreur WebSocket

- Vérifiez que le backend est bien lancé
- Vérifiez le pare-feu (port 8000)

### Performance lente

- Utilisez un modèle plus léger (yolov5n ou yolov5s)
- Réduisez le seuil de confiance
- Fermez les autres applications

## 📦 Structure

```
webapp/
├── backend/
│   ├── main.py           # Serveur FastAPI
│   └── requirements.txt  # Dépendances Python
├── static/
│   ├── index.html        # Interface utilisateur
│   └── app.js            # Logique JavaScript
└── start.ps1             # Script de lancement
```

## 🎨 Technologies Utilisées

**Backend:**

- FastAPI - Framework web moderne
- WebSocket - Communication temps réel
- PyTorch - Inférence YOLOv5
- OpenCV - Traitement d'images

**Frontend:**

- HTML5 + JavaScript ES6
- Tailwind CSS - Framework CSS
- Chart.js - Graphiques interactifs
- Font Awesome - Icons

## 📝 Notes

- Les détections sont sauvegardées en mémoire (redémarrage = perte)
- Maximum 100 entrées dans l'historique
- Format supporté: JPEG, PNG
- Résolution recommandée webcam: 1280x720

## 🌟 Améliorations Futures Possibles

- Enregistrement vidéo des détections
- Export des résultats en CSV/JSON
- Support des vidéos uploadées
- Mode multi-caméras
- Notifications en temps réel
- Base de données persistante
- Authentication utilisateur
