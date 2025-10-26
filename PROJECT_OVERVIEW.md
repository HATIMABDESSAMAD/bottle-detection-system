# 📊 Vue d'Ensemble du Projet

## 🎯 Objectif Global

Créer un système unifié de détection et classification d'objets en temps réel qui combine deux projets existants :
1. **Détection de bouteilles + Classification de marques**
2. **Détection d'objets avec/sans bouchon**

## 🏗️ Architecture Détaillée

### 1. Configuration (`config.py`)

**Rôle** : Centraliser toute la configuration du système

**Sections** :
- `DetectionConfig` : Paramètres de détection (seuils, classes)
- `CameraConfig` : Configuration caméra et vidéo
- `UIConfig` : Paramètres d'interface graphique
- `ProcessingConfig` : Options de traitement

**Chemins des Modèles** :
```python
BOTTLE_YOLO_MODEL = ../test/yolov8n.pt
CAP_YOLO_MODEL = ../Bottle-Bottle-Cap-Detection-System-main - Copie/best.pt
BRAND_CLASSIFIER_MODEL = ../test/bottle_recognition_system/models/brand_classifier.h5
```

### 2. Pipeline de Détection (`detection_pipeline.py`)

**Rôle** : Orchestrer la détection et classification

**Classe Principale** : `UnifiedDetectionPipeline`

**Composants** :
1. **Détecteur de Bouteilles** (YOLOv8)
   - Modèle : YOLOv8n
   - Classe COCO 39 (bottle)
   - Seuil par défaut : 0.5

2. **Détecteur de Bouchons** (YOLOv8)
   - Modèle personnalisé : best.pt
   - 5 classes : Good Cap, Loose Cap, Broken Cap, Broken Ring, No Cap
   - Seuil par défaut : 0.6

3. **Classificateur de Marques** (ResNet50V2)
   - Modèle : brand_classifier.h5
   - 10 marques de bouteilles d'eau
   - Input : 224x224 pixels

**Flux de Traitement** :
```
Frame → Détection Bouteilles → Classification Marques
                             ↘
                               Résultats Combinés
                             ↗
Frame → Détection Bouchons
```

### 3. Utilitaires (`utils.py`)

**Classes Utilitaires** :
- `FPSCounter` : Calcul du FPS en temps réel
- `DetectionStatistics` : Suivi des statistiques

**Fonctions Principales** :
- `preprocess_image()` : Amélioration de contraste, débruitage
- `extract_roi()` : Extraction de région d'intérêt
- `draw_bounding_box()` : Annotation des détections
- `draw_detection_info()` : Overlay d'informations
- `save_screenshot()` : Sauvegarde d'images
- `create_video_writer()` : Enregistrement vidéo
- `calculate_iou()` : Intersection over Union
- `apply_nms()` : Non-Maximum Suppression

### 4. Interface Graphique (`interface.py`)

**Rôle** : Fournir une GUI interactive

**Classe Principale** : `DetectionInterface`

**Composants UI** :

#### Panneau Gauche (Vidéo)
- Canvas pour flux vidéo en temps réel
- Boutons de contrôle :
  - ▶️ Démarrer/Arrêter Caméra
  - 📷 Capture d'écran
  - ⏺️ Enregistrement vidéo

#### Panneau Droit (Contrôles)
- **Statistiques** :
  - FPS actuel
  - Compteur de bouteilles
  - Compteur d'objets avec/sans bouchon
  - Liste des marques détectées

- **Options de Détection** :
  - Checkbox : Activer/Désactiver bouteilles
  - Checkbox : Activer/Désactiver bouchons
  - Checkbox : Activer/Désactiver classification

- **Seuils de Confiance** :
  - Slider : Seuil bouteilles (0.1-0.9)
  - Slider : Seuil bouchons (0.1-0.9)

**Threading** :
- Thread principal : GUI Tkinter
- Thread secondaire : Chargement des modèles
- Loop vidéo : Traitement frame par frame

### 5. Point d'Entrée (`main.py`)

**Rôle** : Lancer l'application avec options CLI

**Arguments** :
```bash
--check-models   # Vérifier modèles
--cpu            # Forcer mode CPU
--debug          # Mode debug
--camera-id N    # Sélectionner caméra
```

**Séquence de Démarrage** :
1. Parser les arguments
2. Afficher configuration (si debug)
3. Vérifier présence des modèles
4. Appliquer les options (CPU, camera ID)
5. Lancer l'interface GUI

## 🔄 Flux de Données Complet

```
┌─────────────────────────────────────────────────────────┐
│                    UTILISATEUR                          │
│  (Lance l'application, contrôle via GUI)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   MAIN.PY                               │
│  • Parse arguments                                      │
│  • Valide modèles                                       │
│  • Lance interface                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              INTERFACE.PY (GUI)                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Panneau Vidéo       │    Panneau Contrôles      │  │
│  │  • Flux en direct    │    • Statistiques         │  │
│  │  • Annotations       │    • Options              │  │
│  │  • Boutons           │    • Sliders              │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ Capture frame
                     ▼
┌─────────────────────────────────────────────────────────┐
│           DETECTION_PIPELINE.PY                         │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │ YOLOv8 Bottles  │  │  YOLOv8 Caps     │            │
│  │ • Détecte bbox  │  │  • Détecte bbox  │            │
│  └────────┬─────────┘  └────────┬─────────┘            │
│           │                     │                       │
│           ▼                     │                       │
│  ┌──────────────────┐           │                       │
│  │  ResNet Brand    │           │                       │
│  │  • Extrait ROI   │           │                       │
│  │  • Classifie     │           │                       │
│  └────────┬─────────┘           │                       │
│           │                     │                       │
│           └──────────┬──────────┘                       │
│                      │                                   │
│                      ▼                                   │
│            Résultats Combinés                           │
│            {bottles: [...],                             │
│             caps: [...]}                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  UTILS.PY                               │
│  • Dessine bounding boxes                               │
│  • Calcule FPS                                          │
│  • Met à jour statistiques                              │
│  • Sauvegarde screenshots/vidéos                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               AFFICHAGE & SORTIE                        │
│  • Frame annotée → GUI                                  │
│  • Screenshots → outputs/screenshots/                   │
│  • Vidéos → outputs/videos/                             │
│  • Logs → outputs/logs/                                 │
└─────────────────────────────────────────────────────────┘
```

## 📦 Dépendances Clés

### Deep Learning
- **TensorFlow** : Framework pour ResNet
- **Keras** : API haut niveau pour ResNet
- **Ultralytics** : Librairie YOLOv8

### Computer Vision
- **OpenCV** : Traitement d'image, capture vidéo
- **NumPy** : Calculs matriciels

### GUI
- **Tkinter** : Interface graphique
- **Pillow** : Conversion d'images pour Tkinter

## 🎨 Code Couleur des Détections

| Type de Détection | Couleur | Code BGR | Usage |
|-------------------|---------|----------|-------|
| Bouteille | Bleu | (255, 0, 0) | Box + marque |
| Avec bouchon | Vert | (0, 255, 0) | Bouchon OK |
| Sans bouchon | Rouge | (0, 0, 255) | Bouchon manquant |
| Bon bouchon | Vert foncé | (0, 200, 0) | Good Cap |
| Mauvais bouchon | Orange | (0, 165, 255) | Broken/Loose |

## 📊 Métriques et Performance

### Métriques Trackées
- **FPS** : Images par seconde
- **Compteurs** :
  - Nombre total de bouteilles
  - Objets avec bouchon
  - Objets sans bouchon
  - Marques détectées (avec fréquence)
- **Temps de traitement** : Par frame

### Optimisations
1. **Batch processing** : Prédictions groupées
2. **Résolution adaptative** : Réduction si FPS < 15
3. **Skip frames** : Option pour sauter des frames
4. **GPU acceleration** : TensorFlow + CUDA
5. **NMS** : Suppression de détections redondantes

## 🔐 Sécurité et Validation

### Validation des Entrées
- Vérification des chemins de modèles
- Validation des indices de caméra
- Vérification des dimensions d'image
- Gestion des erreurs de lecture vidéo

### Gestion d'Erreurs
- Try-catch sur chargement modèles
- Fallback sur erreurs GPU → CPU
- Messages d'erreur informatifs
- Logs détaillés en mode debug

## 📈 Évolutivité

### Extensions Possibles
1. **Multi-threading** : Traitement parallèle
2. **API REST** : Exposer les fonctionnalités
3. **Base de données** : Stocker les détections
4. **Tableaux de bord** : Visualisation avancée
5. **Export données** : CSV, Excel, JSON
6. **Mode batch** : Traitement de vidéos existantes
7. **Notifications** : Alertes sur événements

### Nouvelles Fonctionnalités
- Détection de défauts supplémentaires
- Support de nouveaux types d'objets
- Reconnaissance de codes-barres
- Analyse de qualité d'image
- Tracking d'objets multi-frames

## 🧪 Tests et Validation

### Script de Test
`test_setup.py` valide :
- Version Python (≥3.8)
- Packages installés
- Modèles présents
- Accès caméra
- Disponibilité GPU

### Tests Unitaires (à développer)
- Test des fonctions utils
- Test du pipeline de détection
- Test de l'interface (mocking)

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation complète |
| `QUICK_START.md` | Guide de démarrage rapide |
| `PROJECT_OVERVIEW.md` | Ce fichier - vue d'ensemble |
| Docstrings | Documentation inline du code |

## 🎓 Références Techniques

### YOLOv8
- Architecture : CSPDarknet + PANet + YOLOv8 Head
- Input : 640x640 par défaut
- Classes : 80 classes COCO ou custom

### ResNet50V2
- Architecture : 50 couches avec skip connections
- Input : 224x224x3
- Transfer learning depuis ImageNet

### Formats de Données
- Images : BGR (OpenCV), RGB (PIL/TensorFlow)
- Bounding boxes : (x1, y1, x2, y2)
- Prédictions : Numpy arrays

---

**Document maintenu à jour**  
**Dernière mise à jour** : Octobre 2025
