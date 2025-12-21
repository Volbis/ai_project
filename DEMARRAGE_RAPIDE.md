# 🚀 Guide de Démarrage Rapide - ZKA Marchés CI

## ⚡ Mise en Route en 5 Étapes

### 📦 1. Vérifier l'Installation

```bash
# Vérifier Python (3.8+)
python --version

# Installer dépendances YOLOv5
pip install -r requirements.txt

# Installer outils annotation
pip install labelImg opencv-python
```

### 📸 2. Initialiser le Dataset

```bash
# Créer la structure de dossiers
python scripts/setup_dataset.py

# Résultat:
# dataset_marches_ci/
# ├── images/      ← Mettre vos photos ici
# ├── labels/      ← Labels générés par LabelImg
# ├── train/
# ├── val/
# └── test/
```

### 🏷️ 3. Collecter et Annoter

#### a) Collecte de Photos

**Où ?** Marchés d'Abidjan (Adjamé, Treichville, Cocody, Yopougon)

**Quand ?**
- 🌅 Matin: 6h-10h (affluence forte)
- 🌞 Midi: 12h-14h (moyenne)
- 🌆 Soir: 17h-19h (pic)

**Comment ?**
- Hauteur: 2-5 mètres (vue d'ensemble)
- Angle: 45-90° (légèrement plongée)
- Distance: 5-20 mètres des sujets
- **Minimum: 1000 photos | Recommandé: 3000+ photos**

**Conseils:**
```
✅ Variété scènes (calme, dense, circulation)
✅ Différents angles et distances
✅ Différentes heures de la journée
✅ Conditions météo variées
❌ Éviter photos floues
❌ Éviter contre-jour extrême
```

#### b) Annotation avec LabelImg

```bash
# Installer LabelImg
pip install labelImg

# Lancer
labelImg
```

**Configuration:**
1. Open Dir → `dataset_marches_ci/images/`
2. Change Save Dir → `dataset_marches_ci/labels/`
3. **Format: YOLO** (important!)
4. View → Auto Save Mode ✅

**Les 7 Classes:**

| ID | Classe | Quand l'utiliser | Priorité |
|----|--------|------------------|----------|
| 0 | **personne** | Tout piéton, client, commerçant | ⭐⭐⭐ |
| 1 | **vehicule** | Moto, taxi, camion, vélo | ⭐⭐⭐ |
| 2 | **etal** | Stand de marché, boutique | ⭐⭐ |
| 3 | **chariot** | Brouette, chariot à bras | ⭐⭐ |
| 4 | **obstacle** | Marchandise bloquant passage | ⭐ |
| 5 | **voie_bloquee** | Zone de passage obstruée | ⭐⭐⭐ |
| 6 | **zone_dense** | Concentration >10 pers/m² | ⭐⭐ |

**Raccourcis LabelImg:**
- `W` : Créer boîte
- `D` : Image suivante
- `A` : Image précédente
- `Ctrl+S` : Sauvegarder
- `Del` : Supprimer boîte

### 🔀 4. Répartir le Dataset

```bash
# Après avoir annoté toutes vos images
python scripts/split_dataset.py

# Résultat:
# Train: 70% des images
# Val:   20% des images
# Test:  10% des images
```

**Vérifier:**
```bash
# Statistiques détaillées
python scripts/check_dataset.py

# Visualiser annotations
python scripts/visualize_annotations.py
```

### 🏋️ 5. Entraîner le Modèle

#### Option A: CPU (Lent mais gratuit)

```bash
python train.py \
  --img 640 \
  --batch 8 \
  --epochs 100 \
  --data data/marches_ci.yaml \
  --weights yolov5s.pt \
  --name marches_ci_v1 \
  --patience 10
```

**Durée:** 6-12 heures

#### Option B: GPU (Rapide)

```bash
python train.py \
  --img 640 \
  --batch 16 \
  --epochs 100 \
  --data data/marches_ci.yaml \
  --weights yolov5s.pt \
  --name marches_ci_v1 \
  --device 0 \
  --patience 10
```

**Durée:** 1-3 heures

#### Option C: Google Colab (Gratuit + GPU)

1. Ouvrir: https://colab.research.google.com/
2. Nouveau notebook
3. Runtime → Change runtime type → GPU
4. Coller:

```python
# Cloner YOLOv5
!git clone https://github.com/ultralytics/yolov5
%cd yolov5
!pip install -r requirements.txt

# Upload votre dataset (zip)
from google.colab import files
uploaded = files.upload()  # Sélectionner dataset_marches_ci.zip

# Extraire
!unzip dataset_marches_ci.zip

# Upload marches_ci.yaml dans data/
# Upload votre fichier data/marches_ci.yaml

# Entraîner
!python train.py \
  --img 640 \
  --batch 16 \
  --epochs 100 \
  --data data/marches_ci.yaml \
  --weights yolov5s.pt \
  --name marches_ci_v1
```

### 📊 Résultats Attendus

**Métriques Cibles:**
- mAP@0.5: **> 65%**
- mAP@0.5:0.95: **> 45%**
- Precision: **> 70%**
- Recall: **> 70%**

**Fichiers Générés:**
```
runs/train/marches_ci_v1/
├── weights/
│   ├── best.pt       ← Meilleur modèle (utiliser celui-ci!)
│   └── last.pt
├── results.png       ← Courbes d'entraînement
├── confusion_matrix.png
├── PR_curve.png
└── F1_curve.png
```

## 🧪 Tester le Modèle

```bash
# Sur une image
python detect.py \
  --weights runs/train/marches_ci_v1/weights/best.pt \
  --source dataset_marches_ci/test/images/ \
  --conf 0.35

# Sur webcam
python detect.py \
  --weights runs/train/marches_ci_v1/weights/best.pt \
  --source 0 \
  --conf 0.35

# Sur vidéo
python detect.py \
  --weights runs/train/marches_ci_v1/weights/best.pt \
  --source video_marche.mp4 \
  --conf 0.35
```

**Résultats dans:** `runs/detect/exp/`

## 🔗 Intégrer à l'Application ZKA

### 1. Copier le Modèle

```bash
# Copier le meilleur modèle
copy runs\train\marches_ci_v1\weights\best.pt webapp\backend\marches_ci_best.pt
```

### 2. Adapter le Code Backend

Éditer `webapp/backend/main.py`:

```python
# Ajouter les 7 classes en français
CLASS_NAMES_FR = {
    'personne': 'personne',
    'vehicule': 'véhicule',
    'etal': 'étal',
    'chariot': 'chariot',
    'obstacle': 'obstacle',
    'voie_bloquee': 'voie bloquée',
    'zone_dense': 'zone dense'
}

# Charger le modèle personnalisé
model = load_model('marches_ci_best.pt')
```

### 3. Ajouter Comptage

```python
def calculate_density(detections, image_area):
    """Calculer densité personnes/m²"""
    persons = [d for d in detections if d['class'] == 'personne']
    # Estimer 1 pixel = 0.01 m² (à calibrer)
    area_m2 = image_area * 0.01
    density = len(persons) / area_m2
    return density

def check_alerts(detections):
    """Générer alertes"""
    alerts = []
    
    # Voie bloquée
    blocked = [d for d in detections if d['class'] == 'voie_bloquee']
    if len(blocked) > 0:
        alerts.append({
            'level': 'critical',
            'message': f'⚠️ {len(blocked)} voie(s) bloquée(s) détectée(s)'
        })
    
    # Zone dense
    dense_zones = [d for d in detections if d['class'] == 'zone_dense']
    if len(dense_zones) > 0:
        alerts.append({
            'level': 'warning',
            'message': f'⚠️ {len(dense_zones)} zone(s) de forte densité'
        })
    
    return alerts
```

### 4. Lancer l'Application

```bash
cd webapp
.\start.ps1
```

Ouvrir: http://localhost:8001

## 📚 Documentation Complète

- 📄 [CAS_USAGE_MARCHES_CI.md](webapp/CAS_USAGE_MARCHES_CI.md) - Contexte et cas d'usage
- 🏷️ [GUIDE_ANNOTATION_IMAGES.md](GUIDE_ANNOTATION_IMAGES.md) - Guide d'annotation détaillé
- 🏋️ [GUIDE_ENTRAINEMENT.md](GUIDE_ENTRAINEMENT.md) - Guide d'entraînement approfondi
- 🚀 [PLAN_DEPLOIEMENT_MARCHES.md](webapp/PLAN_DEPLOIEMENT_MARCHES.md) - Stratégie de déploiement
- 📖 [README_ZKA_MARCHES.md](README_ZKA_MARCHES.md) - Vue d'ensemble du projet

## 🛠️ Scripts Utiles

```bash
# Vérifier dataset
python scripts/check_dataset.py

# Visualiser annotations
python scripts/visualize_annotations.py --split train

# Statistiques entraînement
python val.py \
  --weights runs/train/marches_ci_v1/weights/best.pt \
  --data data/marches_ci.yaml
```

## ❓ Problèmes Fréquents

### "ModuleNotFoundError: No module named 'torch'"
```bash
pip install torch torchvision
```

### "CUDA out of memory"
```bash
# Réduire batch size
python train.py --batch 4 ...
```

### "mAP très faible (<40%)"
- ✅ Vérifier qualité annotations (boîtes précises ?)
- ✅ Augmenter nombre images (min 1000)
- ✅ Augmenter epochs (150-200)
- ✅ Essayer modèle plus gros (yolov5m.pt)

### "Images sans label"
```bash
# Lister images sans label
python scripts/check_dataset.py
# Annoter les images manquantes avec LabelImg
```

## 📞 Support

- **Documentation:** Voir dossier `docs/`
- **Issues YOLOv5:** https://github.com/ultralytics/yolov5/issues
- **Contact:** Projet ZKA - ESATIC

---

## 🎯 Checklist Complète

- [ ] Python 3.8+ installé
- [ ] Requirements installés (`pip install -r requirements.txt`)
- [ ] LabelImg installé (`pip install labelImg`)
- [ ] Dataset créé (`python scripts/setup_dataset.py`)
- [ ] 1000+ photos collectées (marchés Abidjan)
- [ ] Toutes images annotées (7 classes)
- [ ] Dataset réparti (`python scripts/split_dataset.py`)
- [ ] Dataset vérifié (`python scripts/check_dataset.py`)
- [ ] Modèle entraîné (mAP > 65%)
- [ ] Modèle testé (`python detect.py`)
- [ ] Modèle intégré dans webapp
- [ ] Application testée sur vraies vidéos
- [ ] Documentation à jour
- [ ] Prêt pour déploiement pilote! 🚀

**Temps Total Estimé:** 2-4 semaines
- Semaine 1-2: Collecte + Annotation (1000+ images)
- Semaine 3: Entraînement + Tests
- Semaine 4: Intégration + Déploiement

Bon courage ! 💪🇨🇮
