# 🚀 Guide de Démarrage Rapide

## Installation en 3 Étapes

### 1️⃣ Installer les Dépendances

Ouvrez PowerShell dans ce dossier et exécutez :

```powershell
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\activate

# Installer les packages
pip install -r requirements.txt
```

### 2️⃣ Vérifier les Modèles

```powershell
python main.py --check-models
```

Vous devriez voir :
```
✓ bottle_yolo: TROUVÉ
✓ cap_yolo: TROUVÉ
✓ brand_classifier: TROUVÉ
✓ brand_classes: TROUVÉ
```

### 3️⃣ Lancer l'Application

```powershell
python main.py
```

## 🎮 Utilisation Rapide

1. **Cliquez sur "▶ Démarrer Caméra"**
2. **Positionnez une bouteille devant la caméra**
3. **Observez la détection en temps réel !**

### Actions Disponibles
- 📷 **Capture** : Prendre une photo
- ⏺️ **Enregistrer** : Enregistrer une vidéo
- ☑️ **Options** : Activer/désactiver les détections
- 🎚️ **Seuils** : Ajuster la sensibilité

## ⚙️ Paramètres par Défaut

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| Résolution | 1280x720 | Résolution de capture |
| FPS cible | 30 | Images par seconde |
| Seuil bouteilles | 0.5 | Confiance minimum |
| Seuil bouchons | 0.6 | Confiance minimum |

## 🎨 Code Couleur des Détections

- 🔵 **BLEU** : Bouteille détectée + marque
- 🟢 **VERT** : Bouchon présent
- 🔴 **ROUGE** : Bouchon manquant

## 📁 Où Trouver les Fichiers

- **Screenshots** : `outputs/screenshots/`
- **Vidéos** : `outputs/videos/`
- **Logs** : `outputs/logs/`

## 🆘 Problèmes Courants

### ❌ Erreur "No module named 'tensorflow'"
```powershell
pip install tensorflow
```

### ❌ Erreur "Cannot open webcam"
```powershell
# Essayer avec une autre caméra
python main.py --camera-id 1
```

### ❌ FPS trop bas
```powershell
# Forcer le mode CPU (parfois plus stable)
python main.py --cpu
```

### ❌ Modèles manquants
Vérifiez que les projets sources existent dans le dossier parent :
- `../test/`
- `../Bottle-Bottle-Cap-Detection-System-main - Copie/`

## 🎯 Conseils pour de Meilleurs Résultats

1. **Éclairage** : Utilisez un bon éclairage
2. **Distance** : Placez la bouteille à 30-50 cm de la caméra
3. **Fond** : Préférez un fond uni
4. **Stabilité** : Évitez les mouvements brusques

## 📞 Besoin d'Aide ?

1. Consultez le `README.md` complet
2. Exécutez en mode debug : `python main.py --debug`
3. Vérifiez les logs dans `outputs/logs/`

---

**Bon détection ! 🎉**
