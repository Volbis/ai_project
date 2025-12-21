# 🏪 ZKA Marchés - Gestion Intelligente des Flux

## 🇨🇮 Contexte Ivoirien

### Problématique

Les grands marchés d'Abidjan (Adjamé, Treichville, Cocody, Yopougon) font face à des défis majeurs :

- **Surpopulation** : Jusqu'à 50 000+ personnes/jour dans certains marchés
- **Accidents** : Bousculades, chutes, collisions véhicules-piétons
- **Congestion** : Voies d'accès bloquées, évacuation impossible en urgence
- **Gestion** : Manque de données sur les flux pour planification
- **Sécurité incendie** : Impossible d'évacuer rapidement en cas d'urgence

### Solution ZKA Marchés

Système de **détection et d'analyse automatique des flux** pour :

1. **Comptage en temps réel** : Nombre de personnes par zone
2. **Détection d'encombrement** : Alertes quand seuil dépassé
3. **Analyze circulation** : Voies bloquées, points de congestion
4. **Statistiques** : Heures de pointe, zones critiques
5. **Prévention** : Prédiction des encombrements

---

## 📊 Classes à Détecter

### Classes Principales (7)

| Classe           | Description                  | Importance      |
| ---------------- | ---------------------------- | --------------- |
| **personne**     | Piéton, client, commerçant   | ⭐⭐⭐ Critique |
| **vehicle**     | Moto, taxi, camion           | ⭐⭐⭐ Critique |
| **etal**         | Stand de marché, boutique    | ⭐⭐ Important  |
| **chariot**      | Brouette, chariot à bras     | ⭐⭐ Important  |
| **obstacle**     | Marchandises empilées, colis | ⭐ Utile        |
| **voie_bloquee** | Passage obstrué              | ⭐⭐⭐ Critique |
| **zone_dense**   | Concentration >10 pers/m²    | ⭐⭐⭐ Critique |

### Examples de Détections

```
┌────────────────────────────────────┐
│  VUE DE DESSUS - MARCHÉ ADJAMÉ     │
│                                    │
│  🧑🧑🧑  [etal] 🧑🧑              │
│  🧑🧑     [etal] 🧑🧑🧑🧑         │
│  🏍️     [chariot]  🧑🧑🧑        │
│  🧑🧑🧑🧑 [voie_bloquee] ❌       │
│  [zone_dense: 15 pers/m²] 🚨      │
│                                    │
└────────────────────────────────────┘
```

---

## 🎯 Cas d'Usage Concrets

### 1. Comptage de Flux

**Objectif** : Connaître le nombre de personnes en temps réel

**Fonctionnement** :

- Caméras aux entrées/sorties du marché
- Détection et tracking des personnes
- Compteur entrées/sorties
- Dashboard temps réel

**Bénéfices** :

- Respect capacité maximale (sécurité)
- Planification personnel de sécurité
- Données pour agrandissement/rénovation

### 2. Détection d'Encombrement

**Objectif** : Alerter quand zone devient dangereuse

**Fonctionnement** :

- Calcul densité (personnes/m²)
- Seuils :
  - 🟢 Normal : < 5 pers/m²
  - 🟡 Dense : 5-10 pers/m²
  - 🔴 Critique : > 10 pers/m²
- Alerte automatique aux agents

**Bénéfices** :

- Prévention bousculades
- Intervention rapide
- Évacuation facilitée

### 3. Gestion Véhicules

**Objectif** : Réguler circulation motos/camions

**Fonctionnement** :

- Détection véhicules dans zones piétonnes
- Comptage camions de livraison
- Identification voies bloquées

**Bénéfices** :

- Réduction accidents
- Optimization livraisons (heures creuses)
- Fluidité circulation

### 4. Cartographie des Zones Critiques

**Objectif** : Identifier points noirs

**Fonctionnement** :

- Heatmap d'encombrement
- Analyze historique
- Identification patterns (jours, heures)

**Bénéfices** :

- Réaménagement éclairé
- Ajout de voies d'accès
- Optimization emplacement étals

### 5. Prévision d'Affluence

**Objectif** : Anticiper les pics

**Fonctionnement** :

- Analyze données historiques
- Corrélation avec événements (fêtes, marchés spéciaux)
- Prédiction 24-48h à l'avance

**Bénéfices** :

- Reinforcement sécurité préventif
- Information aux commerçants
- Communication grand public

---

## 💡 Impact Social et Économique

### Bénéfices Directs

1. **Sécurité** 🔒
   - Réduction accidents de 40-60%
   - Évacuation d'urgence facilitée
   - Prévention bousculades mortelles

2. **Efficacité** ⚡
   - Temps d'accès réduit de 25%
   - Meilleure circulation marchandises
   - Satisfaction clients améliorée

3. **Données** 📈
   - Base pour modernisation
   - Arguments pour investissements
   - Optimization resources

### Réplicabilité

**Autres marchés Abidjan** :

- Marché de Cocody
- Marché de Yopougon
- Marché de Koumassi
- Forum des marchés de Treichville

**Extension possible** :

- Gares routières (Adjamé, Yopougon)
- Centers commerciaux (Playce Marcory)
- Événements (FEMUA, MASA)
- Stades (Félix Houphouët-Boigny)

---

## 🛠️ Architecture Technique

### Infrastructure Recommandée

```
┌─────────────────────────────────────────┐
│         CAMÉRAS (5-10 par marché)       │
│  • Entrées/sorties (comptage)           │
│  • Allées principales (densité)         │
│  • Points critiques identifiés          │
└────────────────┬────────────────────────┘
                 │ RTSP/HTTP
┌────────────────▼────────────────────────┐
│      SERVEUR DÉTECTION (PC/Jetson)      │
│  • YOLOv5 custom marché CI             │
│  • Tracking (DeepSORT)                  │
│  • Calcul densité                       │
│  • Alertes automatiques                 │
└────────────────┬────────────────────────┘
                 │ WebSocket/API
┌────────────────▼────────────────────────┐
│         DASHBOARD ZKA MARCHÉS           │
│  • Carte en temps réel                  │
│  • Compteurs par zone                   │
│  • Alertes visuelles/sonores            │
│  • Historique et statistiques           │
└─────────────────────────────────────────┘
```

### Spécifications Matérielles

**Caméras** :

- Résolution : 1080p minimum
- Angle : 90-110° (vue large)
- Connection : PoE (alimentation + réseau)
- Protection : IP66 (extérieur)
- Coût : ~100-200€/caméra

**Serveur** :

- **Option 1 - PC** : i5/Ryzen 5, 16GB RAM, SSD
  - Coût : ~500-700€
  - Performance : 5-10 caméras
- **Option 2 - GPU** : NVIDIA GTX 1650+
  - Coût : ~300€ (carte)
  - Performance : 20-30 caméras
- **Option 3 - Edge** : NVIDIA Jetson Nano/Xavier
  - Coût : ~100-400€
  - Performance : 2-8 caméras
  - Avantage : Faible consommation

**Réseau** :

- Bande passante : 2-5 Mbps/caméra
- Switch PoE : 8-16 ports
- Routeur/firewall pour sécurité

---

## 📚 Collecte de Données (Dataset)

### Étape 1 : Prise de Photos/Vidéos

**Où** :

- Marché d'Adjamé (heures de pointe)
- Marché de Treichville
- Différents angles et hauteurs

**Quand** :

- Matin (6h-10h) : Arrivée marchandises
- Midi (12h-14h) : Pic clients
- Soir (17h-19h) : Rush retour

**Comment** :

- Smartphone/caméra vidéo
- Extraire images (1 image/2 secondes)
- Objectif : 1000-5000 images

### Étape 2 : Annotation

**Outil recommandé** : LabelImg ou Roboflow

**Process** :

1. Ouvrir image dans LabelImg
2. Dessiner boîte autour de chaque object
3. Sélectionner classe (personne, vehicle, etc.)
4. Sauvegarder (format YOLO)
5. Répéter pour toutes les images

**Répartition** :

- Train : 70% (700 images)
- Validation : 20% (200 images)
- Test : 10% (100 images)

### Étape 3 : Organization

```
dataset_marches_ci/
├── train/
│   ├── images/
│   │   ├── adjame_001.jpg
│   │   ├── adjame_002.jpg
│   │   └── ...
│   └── labels/
│       ├── adjame_001.txt
│       ├── adjame_002.txt
│       └── ...
├── val/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── marches_ci.yaml
```

**Format Label (YOLO)** :

```
# adjame_001.txt
0 0.5 0.3 0.1 0.2    # personne
0 0.6 0.4 0.12 0.22  # personne
1 0.2 0.7 0.15 0.25  # vehicle
```

---

## 🚀 Entraînement du Modèle

### Configuration

**Fichier : marches_ci.yaml**

```yaml
path: dataset_marches_ci
train: train/images
val: val/images
test: test/images

nc: 7 # Nombre de classes
names: ["personne", "vehicle", "etal", "chariot", "obstacle", "voie_bloquee", "zone_dense"]
```

### Commande d'Entraînement

```bash
# Entraînement depuis YOLOv5s pré-entraîné
python train.py \
  --img 640 \
  --batch 16 \
  --epochs 100 \
  --data marches_ci.yaml \
  --weights yolov5s.pt \
  --name marches_ci_v1 \
  --cache \
  --patience 10

# Résultat : runs/train/marches_ci_v1/weights/best.pt
```

### Paramètres Expliqués

- `--img 640` : Résolution images (640x640)
- `--batch 16` : Images par lot (ajuster selon RAM)
- `--epochs 100` : Nombre d'itérations complètes
- `--data` : Fichier config dataset
- `--weights yolov5s.pt` : Transfer learning (recommandé)
- `--cache` : Mise en cache (plus rapide)
- `--patience 10` : Arrêt si pas d'amélioration après 10 epochs

### Temps d'Entraînement Estimé

- **CPU** : 5-10 heures
- **GPU (GTX 1650)** : 1-2 heures
- **GPU (RTX 3060)** : 30-60 minutes

---

## 📈 Évaluation du Modèle

### Métriques Importantes

1. **mAP@0.5** (mean Average Precision)
   - Cible : > 60% (bon)
   - Cible : > 75% (excellent)

2. **Precision** (Précision)
   - % de détections correctes parmi toutes les détections
   - Cible : > 70%

3. **Recall** (Rappel)
   - % d'objets réels détectés
   - Cible : > 70%

4. **FPS** (Frames Per Second)
   - Vitesse de détection
   - Cible : > 10 FPS (temps réel acceptable)

### Validation sur le Terrain

**Tests à effectuer** :

1. Marché pendant heures creuses (facile)
2. Marché pendant heures de pointe (difficile)
3. Différentes conditions lumière (matin, soir)
4. Différents angles caméra
5. Différentes hauteurs (2m, 5m, 10m)

---

## 🎨 Interface ZKA Marchés

### Dashboard Principal

```
┌────────────────────────────────────────────────┐
│  ZKA MARCHÉS - ADJAMÉ                          │
│  ⏰ 14:23 | 📅 19 Déc 2025                     │
├────────────────────────────────────────────────┤
│                                                │
│  📊 FLUX EN TEMPS RÉEL                         │
│                                                │
│  👥 Personnes : 1,247 / 2,000 (62%) 🟡        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                │
│  🏍️ Véhicules : 23                            │
│  🛒 Chariots : 15                              │
│  ⚠️ Voies bloquées : 2                         │
│                                                │
│  🚨 ALERTES ACTIVES (1)                        │
│  • Zone 3 : Densité critique (12 pers/m²)     │
│    [Voir détails] [Notifier agents]           │
│                                                │
│  📍 CARTE DU MARCHÉ                            │
│  ┌──────────────────────────────┐            │
│  │  🟢 Zone 1: 4 pers/m²        │            │
│  │  🟡 Zone 2: 8 pers/m²        │            │
│  │  🔴 Zone 3: 12 pers/m² ⚠️    │            │
│  │  🟢 Zone 4: 3 pers/m²        │            │
│  └──────────────────────────────┘            │
│                                                │
│  📈 STATISTIQUES 24H                           │
│  • Pic d'affluence : 13h45 (1,856 pers)       │
│  • Durée moyenne séjour : 45 min              │
│  • Incidents évités : 3                        │
│                                                │
└────────────────────────────────────────────────┘
```

### Fonctionnalités Avancées

1. **Alertes Automatiques**
   - SMS aux agents de sécurité
   - Notification sonore center de contrôle
   - Escalade selon gravité

2. **Historique**
   - Export PDF rapports journaliers
   - Graphiques tendances mensuelles
   - Comparison année N vs N-1

3. **Prédiction**
   - Affluence prévue prochaines 4h
   - Recommendations staffing
   - Suggestions réaménagement

---

## 💰 Budget et ROI

### Coût Initial (1 marché)

| Poste        | Détail               | Coût       |
| ------------ | -------------------- | ---------- |
| Caméras      | 8 caméras IP PoE     | 1,200€     |
| Serveur      | PC i5 + GPU          | 1,000€     |
| Réseau       | Switch PoE, câbles   | 300€       |
| Installation | Main d'œuvre         | 500€       |
| Logiciel     | Développement custom | 2,000€     |
| **TOTAL**    |                      | **5,000€** |

### Retour sur Investissement

**Économies Annuelles** :

1. Réduction accidents : -50% → 10,000€ économisés (soins, indemnités)
2. Optimization personnel : -20% agents → 15,000€ économisés
3. Meilleure expérience → +10% fréquentation → 50,000€ revenus sup.

**ROI** : Rentabilisé en 3-6 mois

---

## 🔮 Évolution Future

### Phase 1 (Mois 1-3) : POC

- ✅ Dataset 1000 images
- ✅ Modèle entraîné
- ✅ Test sur 1 marché (Adjamé)
- ✅ Dashboard basique

### Phase 2 (Mois 4-6) : Déploiement

- 🔄 3 marchés supplémentaires
- 🔄 Tracking avancé
- 🔄 Alertes automatiques
- 🔄 Application mobile

### Phase 3 (Mois 7-12) : Scaling

- 📈 Tous marchés d'Abidjan (15+)
- 📈 Prédiction IA
- 📈 Intégration autorités
- 📈 API publique pour chercheurs

### Phase 4 (An 2+) : Innovation

- 🚀 Reconnaissance faciale (recherche personnes)
- 🚀 Analyze comportements suspects
- 🚀 Optimization flux automatique
- 🚀 Extension autres villes (Bouaké, San Pedro)

---

## 📞 Partenaires Potentials

1. **Mairies** : Plateau, Adjamé, Treichville
2. **Ministère du Commerce**
3. **Ministère de la Sécurité**
4. **District d'Abidjan**
5. **BNETD** (Bureau National d'Études Techniques)
6. **Startups Tech CI** : Ecosystem, Ingenosya
7. **Universités** : ESATIC, INP-HB, Université Félix

---

## 📝 Conclusion

ZKA Marchés représente une **solution concrète à un problème réel** qui touche quotidiennement des centaines de milliers d'Ivoiriens.

**Advantages clés** :

- ✅ Sécurité améliorée
- ✅ Gestion data-driven
- ✅ Scalable
- ✅ ROI rapide
- ✅ Impact social fort

**Prochaines étapes** :

1. Collecte photos marchés Abidjan
2. Annotation 1000 images
3. Entraînement modèle
4. Test pilote 1 marché
5. Présentation autorités

---

**Auteurs** : Project ZKA - ESATIC 2025  
**Contact** : [Votre email]  
**License** : À définir avec partenaires
