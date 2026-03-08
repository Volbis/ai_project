# 🎯 OBJECTS DÉTECTABLES PAR YOLOV5

## ⚠️ IMPORTANT À SAVOIR

YOLOv5 détecte **80 types d'objets physiques** du quotidien.  
**IL NE DÉTECTE PAS** : texte, documents, visages individuals, émotions.

---

## ✅ OBJECTS QUE YOLOV5 PEUT DÉTECTER

### 👥 PERSONNES

- **person** (personne)

### 🐾 ANIMAUX (17 types)

- bird (oiseau)
- cat (chat)
- dog (chien)
- horse (cheval)
- sheep (mouton)
- cow (vache)
- elephant (éléphant)
- bear (ours)
- zebra (zèbre)
- giraffe (girafe)

### 🚗 VÉHICULES (8 types)

- bicycle (vélo)
- car (voiture)
- motorcycle (moto)
- airplane (avion)
- bus (bus)
- train (train)
- truck (camion)
- boat (bateau)

### 🚦 TRANSPORT

- traffic light (feu de circulation)
- fire hydrant (bouche d'incendie)
- stop sign (panneau stop)
- parking meter (parcmètre)
- bench (banc)

### 🏠 MOBILIER

- chair (chaise)
- couch (canapé)
- potted plant (plante en pot)
- bed (lit)
- dining table (table à manager)
- toilet (toilettes)

### 💻 ÉLECTRONIQUE

- tv (télévision)
- laptop (ordinateur portable)
- mouse (souris)
- remote (télécommande)
- keyboard (clavier)
- cell phone (téléphone portable)

### 🍽️ CUISINE

- microwave (micro-ondes)
- oven (four)
- toaster (grille-pain)
- sink (évier)
- refrigerator (réfrigérateur)

### 🍎 NOURRITURE

- bottle (bouteille)
- wine glass (verre à vin)
- cup (tasse)
- fork (fourchette)
- knife (couteau)
- spoon (cuillère)
- bowl (bol)
- banana (banane)
- apple (pomme)
- sandwich (sandwich)
- orange (orange)
- broccoli (broccoli)
- carrot (carotte)
- hot dog (hot-dog)
- pizza (pizza)
- donut (donut)
- cake (gâteau)

### 🎽 OBJECTS DIVERS

- umbrella (parapluie)
- handbag (sac à main)
- tie (cravate)
- suitcase (valise)
- frisbee (frisbee)
- skis (skis)
- snowboard (snowboard)
- sports ball (ballon de sport)
- kite (cerf-volant)
- baseball bat (batte de baseball)
- baseball glove (gant de baseball)
- skateboard (skateboard)
- surfboard (planche de surf)
- tennis racket (raquette de tennis)
- backpack (sac à dos)

### 📚 DIVERS

- book (livre) - **ATTENTION : détecte le livre physique, pas le texte dedans**
- clock (horloge)
- vase (vase)
- scissors (ciseaux)
- teddy bear (ours en peluche)
- hair drier (sèche-cheveux)
- toothbrush (brosse à dents)

---

## ❌ CE QUE YOLOV5 NE PEUT PAS DÉTECTER

### Documents & Texte

- ❌ Documents papier
- ❌ Texte écrit
- ❌ Pages d'examen
- ❌ Formulaires
- ❌ Cartes
- ❌ Panneaux avec du texte

### Détails humains

- ❌ Visages spécifiques
- ❌ Émotions
- ❌ Âge/genre
- ❌ Gestes précis

### Objects abstraits

- ❌ Concepts
- ❌ Couleurs seules
- ❌ Motifs
- ❌ Ombres

---

## 💡 CONSEILS POUR DE BONNES DÉTECTIONS

### ✅ BONNES CONDITIONS

1. **Éclairage** : Lumière naturelle ou bonne lumière artificielle
2. **Distance** : 1-3 mètres de la caméra
3. **Angle** : Object face à la caméra
4. **Taille** : Object assez grand dans l'image
5. **Netteté** : Image claire, pas floue

### ⚙️ RÉGLAGES RECOMMANDÉS

- **Modèle** : YOLOv5s (bon compromis)
- **Confiance** : 0.25 - 0.35 pour plus de détections
- **Confiance** : 0.50 - 0.70 pour être plus sélectif

### 🎯 EXAMPLES D'UTILISATION

**✅ Cas où ça marche bien :**

- Compter les personnes dans une pièce
- Détecter des voitures dans un parking
- Identifier des objects sur un bureau (laptop, phone, cup)
- Surveiller des animaux
- Détecter des bouteilles, fruits, objects du quotidien

**❌ Cas où ça ne marchera PAS :**

- Lire du texte sur un document
- Analyzer un examen écrit
- Détecter des signatures
- Reconnaître des visages spécifiques
- Lire des panneaux

---

## 🧪 TESTEZ MAINTENANT !

### Pour la Webcam :

1. Placez-vous devant la caméra → détectera **person**
2. Montrez votre téléphone → détectera **cell phone**
3. Montrez une bouteille → détectera **bottle**
4. Montrez une tasse → détectera **cup**

### Pour Upload :

1. Photo de vous → détectera **person**
2. Photo de voiture → détectera **car**
3. Photo de repas → détectera **pizza**, **bottle**, **cup**, etc.
4. Photo d'animal → détectera **dog**, **cat**, etc.

---

## 📊 POURQUOI VOTRE DOCUMENT N'EST PAS DÉTECTÉ ?

Votre image montre un **examen/devoir écrit** :

- ❌ Ce n'est pas un "object physique" que YOLOv5 connaît
- ❌ C'est du **texte** - YOLOv5 ne lit pas le texte
- ✅ Pour lire du texte, il faut un modèle **OCR** (Optical Character Recognition)

**Solution pour votre cas :**

- Pour détecter des objects : Utilisez des photos avec personnes, objects, animaux
- Pour lire du texte : Il faudrait un autre modèle (Tesseract OCR, EasyOCR, etc.)

---

## 🆘 BESOIN D'AIDE ?

**Si aucun object n'est détecté :**

1. Vérifiez que votre image contient un des 80 objects listés ci-dessus
2. Améliorez l'éclairage
3. Baissez le seuil de confiance à 0.20
4. Rapprochez l'objet de la caméra
5. Assurez-vous que l'objet est bien visible et net

**Pour la webcam qui ne détecte rien :**

1. Autorisez l'accès à la webcam dans le navigateur
2. Mettez-vous face à la caméra
3. Vérifiez que le serveur est bien lancé
4. Rechargez la page (F5)

---

Bon test ! 🚀
