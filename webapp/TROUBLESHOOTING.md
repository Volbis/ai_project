# 🔧 Guide de Dépannage - YOLOv5 Web App

## ✅ Serveur Démarré !

Le serveur est maintenant actif sur **http://localhost:8001**

---

## 🎥 Problème de Webcam

### Vérifications Importantes :

#### 1. **Permissions du Navigateur** ⚠️

- Lorsque vous cliquez sur "Démarrer", le navigateur doit demander l'autorisation d'accès à la webcam
- **Vérifiez** : Cliquez sur l'icône de cadenas 🔒 dans la barre d'adresse
- **Autorisez** : Caméra et Microphone pour `localhost`

#### 2. **Navigateur Moderne Requis** 🌐

- ✅ **Recommandé** : Chrome, Edge, Firefox récent
- ❌ **Non supporté** : Internet Explorer
- L'API WebRTC doit être disponible

#### 3. **HTTPS vs HTTP** 🔐

- Sur `localhost` : HTTP fonctionne
- Sur réseau distant : HTTPS obligatoire pour webcam

#### 4. **Simple Browser de VS Code** 💡

Le Simple Browser de VS Code peut avoir des limitations avec la webcam.

**Solution** : Ouvrez dans un navigateur externe :

```
http://localhost:8001
```

---

## 🔍 Tests à Effectuer

### Test 1 : Upload d'Image

1. Allez dans l'onglet **"Upload Images"**
2. Glissez une photo (personne, voiture, animal)
3. Cliquez sur **"Analyzer les images"**
4. ✅ Si cela fonctionne → Le backend marche !

### Test 2 : Console du Navigateur

1. Appuyez sur **F12** pour ouvrir DevTools
2. Allez dans l'onglet **"Console"**
3. Cliquez sur **"Démarrer"** la webcam
4. Regardez les messages d'erreur

**Erreurs Courantes** :

```javascript
// Permission refusée
"NotAllowedError: Permission denied"
→ Solution : Autoriser la caméra dans les paramètres du navigateur

// Webcam non trouvée
"NotFoundError: Requested device not found"
→ Solution : Vérifier qu'une webcam est connectée

// WebSocket fermé
"WebSocket connection closed"
→ Solution : Le serveur est peut-être arrêté
```

---

## 🔧 Solutions Rapides

### Solution 1 : Ouvrir dans Chrome/Edge

```powershell
# Ouvrir directement dans Chrome
start chrome http://localhost:8001

# Ou dans Edge
start msedge http://localhost:8001
```

### Solution 2 : Vérifier les Permissions Windows

1. **Windows 11** : Paramètres → Confidentialité et sécurité → Caméra
2. Vérifier que "Autoriser les applications à accéder à votre caméra" est activé

### Solution 3 : Tester avec une Image d'abord

- Commencez par l'onglet **"Upload Images"**
- Testez avec une photo de personne ou d'objet
- Cela confirme que YOLOv5 fonctionne

---

## 📊 Vérifier l'État du Serveur

### Dans le Terminal

Le serveur doit afficher :

```
✅ Modules YOLOv5 importés avec succès
✅ Modèle yolov5s chargé avec succès!
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Tester l'API

Ouvrez dans un navigateur :

```
http://localhost:8001/api
```

Vous devez voir :

```json
{
  "message": "YOLOv5 Detection API",
  "version": "1.0.0",
  "yolov5_available": true
}
```

---

## 🎯 Objects Détectables

YOLOv5 détecte **80 classes d'objets** dont :

### Personnes & Animaux 👥🐕

- person, cat, dog, horse, sheep, cow, bird, etc.

### Véhicules 🚗

- car, truck, bus, motorcycle, bicycle, airplane, train

### Objects du Quotidien 📱

- laptop, keyboard, mouse, phone, bottle, cup, chair, etc.

### Sport ⚽

- ball, tennis racket, skateboard, etc.

**Note** : YOLOv5 ne détecte pas :

- ❌ Texte ou chiffres
- ❌ Émotions ou sentiments
- ❌ Objects abstraits

---

## 🐛 Debugging Avancé

### Voir les logs en temps réel

Le terminal affiche les détections :

```
✅ Détection terminée: 3 objects trouvés en 0.145s
```

### Tester le WebSocket manuellement

Dans la console du navigateur (F12) :

```javascript
const ws = new WebSocket("ws://localhost:8001/ws");
ws.onopen = () => console.log("Connecté!");
ws.onerror = (e) => console.error("Erreur:", e);
```

---

## 📞 Checklist Complète

- [ ] Serveur actif sur http://localhost:8001
- [ ] Page s'ouvre dans le navigateur
- [ ] Terminal affiche "Uvicorn running"
- [ ] Test Upload fonctionne
- [ ] Permissions caméra autorisées
- [ ] Navigateur moderne (Chrome/Edge/Firefox)
- [ ] Console browser (F12) ne montre pas d'erreurs
- [ ] WebSocket connecté (voir console)

---

## ✨ Tout Fonctionne !

Si vous voyez :

- ✅ Flux vidéo de la webcam
- ✅ Boîtes vertes autour des objects détectés
- ✅ Liste des détections à droite qui se met à jour
- ✅ FPS et latence affichés

**Félicitations ! 🎉** Votre application YOLOv5 fonctionne parfaitement !

---

## 🚀 Commandes Utiles

### Redémarrer le serveur

```powershell
# Arrêter : Ctrl+C dans le terminal
# Redémarrer :
cd "c:\Users\HP\OneDrive - Ecole Supérieure Africaine des Technologies de l'Information et de la Communication (ESATIC)\Bureau\yolov5\webapp\backend"
python main.py
```

### Changer le port

Modifier dans `main.py` ligne 478 :

```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changer 8001
```

---

## 📖 Documentation

- **API Docs** : http://localhost:8001/docs
- **Statistiques** : http://localhost:8001/statistics
- **Modèles disponibles** : http://localhost:8001/models

---

**Besoin d'aide ?** Consultez les logs du terminal et la console du navigateur (F12) pour plus de détails sur les erreurs.
