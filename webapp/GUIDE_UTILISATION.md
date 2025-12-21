# 📖 Guide d'Utilisation - YOLOv5 Vision AI

## 🚀 Démarrage Rapide

### Lancer l'application
```powershell
cd webapp\backend
python main.py
```

Puis ouvrez : **http://localhost:8001**

---

## 📱 Les 4 Onglets de l'Application

### 1️⃣ **Webcam en Direct** 🎥
**Ce que ça fait :** Détecte les objets en temps réel depuis votre caméra

**Comment l'utiliser :**
1. Cliquez sur le bouton vert **"Démarrer"**
2. Autorisez l'accès à votre webcam
3. Les détections apparaissent instantanément avec des rectangles verts
4. À droite, vous voyez la liste des objets détectés

**Quand l'utiliser :**
- Pour détecter des objets autour de vous en direct
- Pour tester le modèle rapidement
- Pour surveiller un espace en temps réel

---

### 2️⃣ **Upload Images** 📤
**Ce que ça fait :** Analyse des photos depuis votre ordinateur

**Comment l'utiliser :**
1. **Glissez-déposez** vos images dans la zone bleue en pointillés
   - OU cliquez sur **"Choisir des fichiers"**
2. Sélectionnez une ou plusieurs images (JPG, PNG)
3. Cliquez sur **"Analyser les images"**
4. Les résultats s'affichent à droite avec les objets détectés

**Quand l'utiliser :**
- Pour analyser des photos existantes
- Pour traiter plusieurs images en même temps
- Quand vous n'avez pas de webcam
- Pour garder les résultats

---

### 3️⃣ **Dashboard** 📊
**Ce que ça fait :** Affiche les statistiques de toutes vos détections

**Ce que vous voyez :**
- **Total Détections** : Nombre d'objets trouvés au total
- **Images Traitées** : Combien d'images vous avez analysées
- **FPS Moyen** : Vitesse de traitement
- **Graphique circulaire** : Quels objets sont les plus détectés
- **Graphique de performance** : Évolution des temps de traitement

**Quand l'utiliser :**
- Pour voir vos performances globales
- Pour comprendre quels objets sont détectés le plus souvent
- Pour analyser la vitesse de traitement

---

### 4️⃣ **Historique** 📜
**Ce que ça fait :** Liste toutes vos détections précédentes

**Ce que vous voyez :**
- Date et heure de chaque détection
- Nom du fichier
- Liste des objets trouvés avec leur confiance

**Actions possibles :**
- **Bouton rouge "Effacer"** : Supprime tout l'historique

**Quand l'utiliser :**
- Pour revoir vos anciennes détections
- Pour comparer les résultats
- Pour retrouver une analyse passée

---

## ⚙️ Paramètres Ajustables

### 🎯 **Modèle** (en bas de la webcam)
Choisissez la précision vs vitesse :
- **YOLOv5n (Nano)** : ⚡ Très rapide, moins précis
- **YOLOv5s (Small)** : ✅ RECOMMANDÉ - Équilibré
- **YOLOv5m (Medium)** : Plus précis, un peu plus lent
- **YOLOv5l (Large)** : Très précis, plus lent
- **YOLOv5x (Extra Large)** : 🎯 Maximum de précision, le plus lent

### 🎚️ **Confiance** (curseur)
- **Valeur basse (0.1-0.3)** : Détecte plus d'objets, mais plus d'erreurs
- **Valeur moyenne (0.4-0.6)** : ✅ RECOMMANDÉ - Bon équilibre
- **Valeur haute (0.7-0.9)** : Seulement les détections très sûres

---

## 🌙 Fonctionnalités Supplémentaires

### **Mode Sombre/Clair**
- Cliquez sur l'icône 🌙 en haut à droite
- Préférence sauvegardée automatiquement

### **Indicateur "En ligne"**
- Point vert qui clignote : Le serveur est connecté ✅
- Si rouge : Problème de connexion ❌

---

## 🎨 Objets Détectables

YOLOv5 peut détecter **80 objets** différents :

**Personnes et animaux :**
- Personne, chien, chat, oiseau, cheval, mouton, vache, etc.

**Véhicules :**
- Voiture, moto, bus, camion, vélo, train, avion, bateau

**Mobilier :**
- Chaise, canapé, table, lit, bureau

**Électronique :**
- Téléphone, ordinateur, TV, clavier, souris

**Nourriture :**
- Pomme, banane, sandwich, pizza, gâteau

**Et bien plus !**

---

## 🔧 Résolution des Problèmes

### ❌ "Aucune détection"
**Causes possibles :**
- Confiance trop élevée → Baissez le curseur à 0.25
- Objet trop petit → Rapprochez-vous
- Objet non reconnu → Vérifiez la liste des 80 objets
- Mauvais éclairage → Améliorez la lumière

**Solution :**
1. Vérifiez dans le terminal que le modèle est bien chargé
2. Regardez si "✅ Modèle préchargé avec succès!" apparaît
3. Baissez la confiance à 0.20
4. Essayez avec des objets courants (personne, téléphone, chaise)

### 🎥 Webcam ne s'active pas
1. Vérifiez les permissions du navigateur
2. Fermez les autres applications utilisant la webcam (Zoom, Teams, etc.)
3. Rechargez la page (F5)

### 🐌 Application lente
1. Choisissez **YOLOv5n** (plus rapide)
2. Fermez les autres onglets du navigateur
3. Réduisez la résolution de la webcam

### 📡 Erreur de connexion
1. Vérifiez que le serveur est lancé : `python main.py`
2. Vérifiez l'URL : **http://localhost:8001**
3. Désactivez temporairement l'antivirus/pare-feu

---

## 💡 Astuces Pro

1. **Meilleure détection :**
   - Bon éclairage
   - Objet face caméra
   - Distance moyenne (1-3 mètres)

2. **Performance optimale :**
   - Utilisez YOLOv5s pour commencer
   - Confiance à 0.25
   - Fermez les applications inutiles

3. **Tests efficaces :**
   - Commencez avec des objets simples : personne, téléphone, bouteille
   - Testez d'abord avec Upload Images pour vérifier que tout fonctionne
   - Puis passez à la webcam

---

## 📞 Support

Si rien ne fonctionne :
1. Regardez le terminal pour les messages d'erreur
2. Vérifiez que toutes les dépendances sont installées
3. Essayez de redémarrer le serveur (Ctrl+C puis relancer)

---

## 🎯 Cas d'Usage

**Sécurité :**
- Détection de personnes dans une zone
- Comptage de visiteurs

**Inventaire :**
- Détecter et compter des objets
- Vérifier la présence d'équipements

**Recherche :**
- Analyser des collections d'images
- Classifier des photos

**Éducation :**
- Apprendre la vision par ordinateur
- Démonstration d'IA

---

Amusez-vous bien avec YOLOv5 Vision AI ! 🚀✨
