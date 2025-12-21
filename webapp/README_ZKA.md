# 🎯 ZKA - Système de Détection d'Objets par Intelligence Artificielle

## 📋 Description

**ZKA** est une application web de détection d'objets en temps réel utilisant l'intelligence artificielle YOLOv5.

### ✨ Caractéristiques Principales

- 🎥 **Détection en temps réel** via webcam
- 📸 **Upload d'images** pour analyse batch
- 🇫🇷 **Interface 100% en français** avec noms d'objets traduits
- 📊 **Tableau de bord** avec statistiques détaillées
- 🔍 **80 classes d'objets** détectables
- ⚡ **Performances optimisées** avec détection à 2 FPS

## 🚀 Démarrage Rapide

### Windows
```powershell
cd webapp\backend
python main.py
```

Ouvrez ensuite : **http://localhost:8001**

## 🎯 Objets Détectables (en français)

### 👥 Personnes & Animaux
- personne, chat, chien, cheval, mouton, vache, éléphant, ours, zèbre, girafe, oiseau

### 🚗 Véhicules
- voiture, camion, bus, moto, vélo, avion, train, bateau

### 🏠 Objets du Quotidien
- ordinateur portable, clavier, souris, téléphone portable, télévision
- chaise, canapé, table à manger, lit
- bouteille, tasse, bol, fourchette, couteau, cuillère

### 🍕 Nourriture
- pomme, banane, orange, pizza, sandwich, hot-dog, gâteau, donut

### 📚 Autres
- livre, horloge, vase, ciseaux, ours en peluche, parapluie, sac à dos, valise

## ⚙️ Configuration

### Seuil de Confiance
- **Par défaut** : 0.35 (35%)
- **Recommandé** : 0.30-0.40 pour usage général
- **Précision élevée** : 0.50+ (moins de détections mais plus fiables)
- **Sensibilité élevée** : 0.20-0.25 (plus de détections, risque de faux positifs)

### Vitesse de Détection
- **Webcam** : 2 FPS (une frame toutes les 500ms)
- **Traitement** : ~1 seconde par image
- **Optimisé pour** : Utilisation CPU

## 🎨 Interface

### 📹 Webcam en Direct
Détection en temps réel avec affichage des objets détectés

### 📤 Upload d'Images
Analysez plusieurs images simultanément

### 📊 Tableau de Bord
- Nombre total de détections
- Images traitées
- Performance moyenne
- Graphiques des objets détectés

### 📜 Historique
Consultez toutes les détections passées

## 🔧 Conseils d'Utilisation

### Pour de Meilleures Détections

1. **Éclairage** : Utilisez un bon éclairage naturel ou artificiel
2. **Distance** : Placez-vous à 1-2 mètres de la caméra
3. **Cadrage** : Montrez les objets entiers dans le cadre
4. **Netteté** : Évitez les mouvements brusques (caméra ou objets)

### Résolution des Problèmes

**Aucun objet détecté :**
- Baissez le seuil de confiance (0.25-0.30)
- Améliorez l'éclairage
- Rapprochez-vous ou éloignez-vous

**Trop de fausses détections :**
- Augmentez le seuil de confiance (0.40-0.50)
- Améliorez la qualité de l'image

**Performances lentes :**
- L'utilisation CPU est normale
- Fermez les applications lourdes
- Réduisez la résolution de la webcam si possible

## 🛠️ Technologies

- **Backend** : FastAPI (Python)
- **Frontend** : HTML5, TailwindCSS, JavaScript
- **IA** : YOLOv5 (Ultralytics)
- **Deep Learning** : PyTorch
- **Communication** : WebSocket pour temps réel

## 📦 Dépendances Principales

```
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0
fastapi>=0.104.0
uvicorn>=0.24.0
pillow>=10.0.0
numpy>=1.24.0
```

## 📝 API Endpoints

- `GET /` - Interface web
- `POST /detect` - Détection sur une image
- `POST /detect/batch` - Détection sur plusieurs images
- `GET /statistics` - Statistiques globales
- `GET /history` - Historique des détections
- `WS /ws` - WebSocket pour détection temps réel
- `GET /docs` - Documentation interactive de l'API

## 🎓 Développé avec

- YOLOv5 (You Only Look Once v5)
- Modèle YOLOv5s (Small) pour rapidité
- Dataset COCO (80 classes)
- Traduction française des classes

## 📄 Licence

Ce projet utilise YOLOv5 sous licence AGPL-3.0

## 🤝 Support

Pour toute question ou problème :
1. Consultez le fichier TROUBLESHOOTING.md
2. Vérifiez que le serveur est actif
3. Testez avec l'onglet "Upload Images" d'abord
4. Vérifiez les logs du serveur dans le terminal

---

**ZKA - Intelligence Artificielle au Service de la Détection** 🚀
