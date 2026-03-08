# 📋 Plan de Déploiement - ZKA Marchés CI

## 🎯 Objectif

Transformer ZKA d'une application générique de détection d'objets en une solution spécialisée pour la **gestion des flux dans les marchés ivoiriens**.

---

## 📦 Livrables du Project

### 1. Documentation ✅

- [x] **CAS_USAGE_MARCHES_CI.md** - Contexte, problématique, impact
- [x] **GUIDE_ANNOTATION_IMAGES.md** - Instructions annotation LabelImg
- [x] **GUIDE_ENTRAINEMENT.md** - Entraînement modèle custom
- [x] **marches_ci.yaml** - Configuration dataset (7 classes)

### 2. Code à Adapter 🔄

#### Backend (webapp/backend/main.py)

**Changements nécessaires** :

```python
# ─────────────────────────────────────────────────────────
# AVANT (80 classes COCO)
# ─────────────────────────────────────────────────────────
MODEL_PATH = YOLOV5_ROOT / "yolov5s.pt"

CLASS_NAMES_FR = {
    "person": "personne",
    "car": "voiture",
    # ... 80 classes COCO
}

# ─────────────────────────────────────────────────────────
# APRÈS (7 classes Marchés CI)
# ─────────────────────────────────────────────────────────
MODEL_PATH = YOLOV5_ROOT / "webapp" / "models" / "marches_ci_best.pt"

CLASS_NAMES_MARCHES = {
    "personne": "personne",
    "vehicle": "véhicule",
    "etal": "étal",
    "chariot": "chariot",
    "obstacle": "obstacle",
    "voie_bloquee": "voie bloquée ⚠️",
    "zone_dense": "zone dense 🚨",
}


# Calcul densité (nouveau)
def calculate_density(detections, image_area_m2=50):
    """Calcule la densité de personnes par m²."""
    person_count = sum(1 for d in detections if d["class"] == "personne")
    density = person_count / image_area_m2
    return density


# Alertes automatiques (nouveau)
def check_alerts(detections, density):
    """Génère alertes selon détections."""
    alerts = []

    # Alerte densité critique
    if density > 10:
        alerts.append(
            {
                "level": "critical",
                "type": "densite",
                "message": f"Densité critique: {density:.1f} pers/m²",
                "action": "Évacuation partielle recommandée",
            }
        )
    elif density > 5:
        alerts.append(
            {
                "level": "warning",
                "type": "densite",
                "message": f"Densité élevée: {density:.1f} pers/m²",
                "action": "Surveillance accrue",
            }
        )

    # Alerte voie bloquée
    blocked = [d for d in detections if d["class"] == "voie_bloquee"]
    if blocked:
        alerts.append(
            {
                "level": "warning",
                "type": "circulation",
                "message": f"{len(blocked)} voie(s) bloquée(s)",
                "action": "Dégager les passages",
            }
        )

    # Alerte zone dense
    dense_zones = [d for d in detections if d["class"] == "zone_dense"]
    if dense_zones:
        alerts.append(
            {
                "level": "warning",
                "type": "concentration",
                "message": f"{len(dense_zones)} zone(s) de concentration",
                "action": "Réguler les flux",
            }
        )

    return alerts
```

#### Frontend (webapp/static/index.html)

**Ajouts nécessaires** :

```html
<!-- Nouveau : Compteurs Spécialisés -->
<div class="grid grid-cols-4 gap-4 mb-6">
  <div class="bg-blue-500 text-white p-4 rounded">
    <div class="text-3xl font-bold" id="count-personnes">0</div>
    <div class="text-sm">👥 Personnes</div>
  </div>
  <div class="bg-green-500 text-white p-4 rounded">
    <div class="text-3xl font-bold" id="count-vehicules">0</div>
    <div class="text-sm">🏍️ Véhicules</div>
  </div>
  <div class="bg-yellow-500 text-white p-4 rounded">
    <div class="text-3xl font-bold" id="densite">0</div>
    <div class="text-sm">📊 Densité (pers/m²)</div>
  </div>
  <div class="bg-red-500 text-white p-4 rounded">
    <div class="text-3xl font-bold" id="count-alertes">0</div>
    <div class="text-sm">🚨 Alertes</div>
  </div>
</div>

<!-- Nouveau : Section Alertes -->
<div id="alertes-container" class="mb-6">
  <!-- Alertes dynamiques ici -->
</div>

<!-- Nouveau : Carte des Zones -->
<div class="bg-white rounded-lg shadow p-4 mb-6">
  <h3 class="text-lg font-bold mb-4">📍 Carte du Marché</h3>
  <div id="market-map" class="h-64 bg-gray-100 rounded">
    <!-- Visualization carte marché -->
  </div>
</div>
```

#### Frontend JavaScript (webapp/static/app.js)

**Nouvelles functions** :

```javascript
// Afficher alertes
function displayAlerts(alerts) {
  const container = document.getElementById("alertes-container");

  if (alerts.length === 0) {
    container.innerHTML = "";
    return;
  }

  const alertHTML = alerts
    .map((alert) => {
      const bgColor = alert.level === "critical" ? "bg-red-100 border-red-500" : "bg-yellow-100 border-yellow-500";
      const icon = alert.level === "critical" ? "🚨" : "⚠️";

      return `
            <div class="${bgColor} border-l-4 p-4 mb-2">
                <div class="flex items-center">
                    <span class="text-2xl mr-3">${icon}</span>
                    <div>
                        <p class="font-bold">${alert.message}</p>
                        <p class="text-sm text-gray-700">${alert.action}</p>
                    </div>
                </div>
            </div>
        `;
    })
    .join("");

  container.innerHTML = alertHTML;
}

// Mettre à jour compteurs
function updateCounters(detections, density, alerts) {
  const personnes = detections.filter((d) => d.class === "personne").length;
  const vehicles = detections.filter((d) => d.class === "vehicle").length;

  document.getElementById("count-personnes").textContent = personnes;
  document.getElementById("count-vehicles").textContent = vehicles;
  document.getElementById("densite").textContent = density.toFixed(1);
  document.getElementById("count-alertes").textContent = alerts.length;
}

// Visualizer carte marché
function updateMarketMap(detections) {
  // TODO: Implémenter visualization carte
  // Peut utiliser Canvas ou bibliothèque comme Konva.js
}
```

### 3. Interface Utilisateur 🎨

**Nouveau Design - Dashboard Marchés** :

```
┌──────────────────────────────────────────────────────────┐
│  🏪 ZKA MARCHÉS - ADJAMÉ                🔴 LIVE          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  👥 247 │  │ 🏍️  12  │  │ 📊 4.9  │  │  🚨 1   │   │
│  │Personnes│  │Véhicules│  │ pers/m² │  │ Alertes │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│                                                          │
│  🚨 ALERTES ACTIVES                                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │ ⚠️  Zone 3 : Densité élevée (8.2 pers/m²)       │  │
│  │     Action : Surveillance accrue                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  📹 FLUX VIDÉO                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │                                                  │  │
│  │         [Image webcam avec détections]          │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  📊 DÉTECTIONS EN TEMPS RÉEL                            │
│  • personne ×247                                        │
│  • véhicule ×12                                         │
│  • étal ×45                                             │
│  • chariot ×8                                           │
│                                                          │
│  📍 CARTE DU MARCHÉ                                     │
│  [Visualization zones + densités]                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🗓️ Roadmap de Mise en Œuvre

### Phase 0 : Préparation (Maintenant) ✅

- [x] Documentation complète créée
- [x] Configuration dataset (marches_ci.yaml)
- [x] Guides d'annotation et d'entraînement
- [ ] Définir site pilote (ex: Marché d'Adjamé)
- [ ] Obtenir autorisations filmage

### Phase 1 : Collecte de Données (Semaine 1-2)

**Objectif** : 1000+ images annotées

- [ ] Jour 1-3 : Prise de photos/vidéos
  - Marché d'Adjamé : 400 images
  - Marché de Treichville : 300 images
  - Autres marchés : 300 images
- [ ] Jour 4-7 : Annotation avec LabelImg
  - 150-200 images/jour
  - Vérification qualité annotations
- [ ] Jour 8-10 : Organization dataset
  - Split 70/20/10
  - Vérification avec scripts Python
  - Backup sur cloud

### Phase 2 : Entraînement (Semaine 3)

**Objectif** : Modèle avec mAP > 65%

- [ ] Jour 1 : Setup environment
  - Installer dépendances
  - Vérifier GPU (ou Google Colab)
- [ ] Jour 2-4 : Premier entraînement
  - 100 epochs
  - Analyzer résultats
  - Identifier faiblesses
- [ ] Jour 5-6 : Optimization
  - Corriger annotations problématiques
  - Réentraîner avec hyperparamètres ajustés
- [ ] Jour 7 : Validation
  - Tests sur vidéos réelles
  - Mesurer performances (FPS, précision)

### Phase 3 : Intégration ZKA (Semaine 4)

**Objectif** : Application fonctionnelle

- [ ] Jour 1-2 : Backend
  - Adapter main.py pour 7 classes
  - Implémenter calcul densité
  - Implémenter système d'alertes
- [ ] Jour 3-4 : Frontend
  - Nouveau design dashboard
  - Compteurs spécialisés
  - Section alertes
- [ ] Jour 5-6 : Tests
  - Tests unitaires
  - Tests d'intégration
  - Tests de charge
- [ ] Jour 7 : Documentation
  - Guide utilisateur
  - Guide installation
  - Vidéo démo

### Phase 4 : Test Pilote (Semaine 5-8)

**Objectif** : Validation terrain

- [ ] Semaine 5 : Installation
  - Caméra(s) au marché pilote
  - Configuration serveur
  - Formation personnel
- [ ] Semaine 6-7 : Collecte données
  - Monitoring 24/7
  - Collecte feedback
  - Ajustements
- [ ] Semaine 8 : Analyze
  - Rapport statistiques
  - ROI estimé
  - Plan d'extension

### Phase 5 : Scale-up (Mois 3-6)

**Objectif** : Extension à 3-5 marchés

- [ ] Installation équipements
- [ ] Entraînement personnel
- [ ] Dashboard centralisé
- [ ] Intégration autorités

---

## 💰 Budget Estimatif

### Project Pilote (1 Marché)

| Poste                          | Quantité | Prix Unitaire | Total      |
| ------------------------------ | -------- | ------------- | ---------- |
| **Matériel**                   |          |               |            |
| Caméras IP PoE 1080p           | 4        | 150€          | 600€       |
| PC Serveur (i5, 16GB, SSD)     | 1        | 600€          | 600€       |
| Switch PoE 8 ports             | 1        | 100€          | 100€       |
| Câbles réseau                  | 50m      | 1€/m          | 50€        |
| Protection (boîtiers étanches) | 4        | 30€           | 120€       |
| **Installation**               |          |               |            |
| Main d'œuvre                   | 3 jours  | 100€/j        | 300€       |
| Support/fixations              |          |               | 100€       |
| **Logiciel**                   |          |               |            |
| Développement custom           | 20h      | 50€/h         | 1000€      |
| **Formation**                  |          |               |            |
| Personnel marché               | 1 jour   | 200€          | 200€       |
| **Divers**                     |          |               |            |
| Imprévus (10%)                 |          |               | 300€       |
| **TOTAL**                      |          |               | **3,370€** |

### Scaling (5 Marchés)

- Coût/marché réduit : ~2,500€ (économie d'échelle)
- Total 5 marchés : **12,500€**
- Budget marketing : 2,000€
- **TOTAL PROJECT** : **~15,000€**

---

## 📊 KPIs de Succès

### Métriques Techniques

- ✅ **Précision modèle** : mAP@0.5 > 65%
- ✅ **Performance** : >10 FPS sur CPU
- ✅ **Disponibilité** : >99% uptime
- ✅ **Latence** : <2 secondes détection

### Métriques Business

- ✅ **Satisfaction utilisateurs** : >80%
- ✅ **Réduction incidents** : -40% sur 6 mois
- ✅ **ROI** : <12 mois
- ✅ **Adoption** : 5+ marchés en 1 an

### Métriques Impact Social

- ✅ **Accidents évités** : -50%
- ✅ **Temps d'intervention** : -60%
- ✅ **Satisfaction usagers** : +30%
- ✅ **Couverture médiatique** : 10+ articles

---

## 🤝 Partenaires et Soutiens

### Institutions Publiques

- **Mairies** : Plateau, Adjamé, Treichville
- **District d'Abidjan**
- **Ministère du Commerce**
- **Ministère de la Sécurité**
- **BNETD** (Bureau National d'Études Techniques)

### Secteur Privé

- **Orange CI / MTN CI** : Connectivité
- **Startups Tech CI** : Ecosystem, Ingenosya, Coliba
- **Banques** : Financement (Ecobank, BOA)

### Académique

- **ESATIC** : R&D, étudiants stagiaires
- **INP-HB** : Partenariat technique
- **Université Félix** : Études d'impact

---

## 📢 Communication et Valorisation

### Événements de Lancement

1. **Démo Presse** (Semaine 4)
   - Présentation au marché pilote
   - Conférence de presse
   - Communiqué de presse

2. **Journée Portes Ouvertes** (Mois 2)
   - Visite guidée pour autorités
   - Démonstrations live
   - Témoignages commerçants

3. **Publication Scientifique** (Mois 6)
   - Article conférence (CARI, AFRICON)
   - Blog technique
   - Tutorial open source

### Médias

- **TV** : RTI, NCI, A+ Ivoire
- **Radio** : RFI Afrique, Radio Nostalgie
- **Presse** : Fraternité Matin, Soir Info
- **Web** : Abidjan.net, afrikmag, LinkedIn

---

## 🚀 Go to Market

### Message Clé

> "ZKA Marchés transforme la gestion de nos marchés avec l'Intelligence Artificielle. Sécurité, efficacité, données : le marché du futur, aujourd'hui."

### Proposition de Valeur

**Pour les Autorités** :

- Réduction accidents et incidents
- Données pour décisions éclairées
- Image moderne et innovante

**Pour les Commerçants** :

- Meilleure sécurité
- Moins de congestion
- Plus de clients (expérience améliorée)

**Pour les Usagers** :

- Navigation facilitée
- Temps réduit
- Expérience agréable

---

## ✅ Checklist Avant Lancement

### Technique

- [ ] Modèle entraîné (mAP > 65%)
- [ ] Tests validés
- [ ] Serveur configuré
- [ ] Caméras installées
- [ ] Réseau sécurisé
- [ ] Backup automatique
- [ ] Monitoring en place
- [ ] Documentation complète

### Légal

- [ ] Autorisations filmage obtenues
- [ ] RGPD/Protection données respectée
- [ ] Contrats partenaires signés
- [ ] Assurances souscrites

### Organisationnel

- [ ] Équipe formée
- [ ] Process définis
- [ ] Hotline support
- [ ] Plan maintenance

### Communication

- [ ] Site web/landing page
- [ ] Communiqué presse prêt
- [ ] Vidéo démo produite
- [ ] Réseaux sociaux actifs

---

## 🎯 Vision Long Terme

### An 1 : Abidjan (15 marchés)

- Déploiement progressif
- Collecte données massives
- Amélioration continue

### An 2 : Côte d'Ivoire (50+ marchés)

- Extension Bouaké, Yamoussoukro, San Pedro
- Gares routières
- Centers commerciaux

### An 3 : Afrique de l'Ouest

- Dakar, Bamako, Lomé, Cotonou
- Partenariats CEDEAO
- Solution SaaS

### An 5 : Impact Panafricain

- 1000+ sites équipés
- 10M+ personnes impactées
- Standard de référence

---

**Le futur des marchés africans commence ici. 🚀🇨🇮**

---

_Document créé le 19 décembre 2025 - Project ZKA Marchés - ESATIC_
