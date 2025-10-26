# 📦 Guide d'Installation Complet

## Prérequis Système

### 🖥️ Système d'Exploitation
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+)
- ✅ macOS (10.15+)

### 🐍 Python
- **Version requise** : Python 3.8 ou supérieur
- **Recommandé** : Python 3.10

**Vérifier votre version** :
```powershell
python --version
```

### 📷 Matériel
- **Webcam** : Intégrée ou USB
- **RAM** : 8 GB minimum, 16 GB recommandé
- **Processeur** : Intel i5/AMD Ryzen 5 ou supérieur
- **GPU** (Optionnel mais recommandé) :
  - NVIDIA GTX 1060 ou supérieur
  - CUDA 11.2+
  - cuDNN 8.1+

## 📥 Installation Pas à Pas

### Méthode 1 : Installation Automatique (Windows)

1. **Double-cliquez sur `run.bat`**
   - Le script installera automatiquement tout
   - Suivez les instructions à l'écran

### Méthode 2 : Installation Manuelle

#### Étape 1 : Cloner ou Télécharger le Projet

```powershell
cd "c:\Users\HATIM\Desktop\OD\bouchon  et marque\unified_detection_app"
```

#### Étape 2 : Créer un Environnement Virtuel

**Windows PowerShell** :
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS** :
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Étape 3 : Mettre à Jour pip

```powershell
python -m pip install --upgrade pip
```

#### Étape 4 : Installer les Dépendances

```powershell
pip install -r requirements.txt
```

Cette commande installera :
- TensorFlow (Deep Learning)
- OpenCV (Computer Vision)
- Ultralytics (YOLOv8)
- Pillow (Images)
- NumPy (Calculs)

**Temps estimé** : 5-15 minutes selon votre connexion

#### Étape 5 : Vérifier l'Installation

```powershell
python test_setup.py
```

Vous devriez voir :
```
✓ PASS     | Python Version
✓ PASS     | Required Packages
✓ PASS     | Model Files
✓ PASS     | Output Directories
✓ PASS     | Camera Access
✓ PASS     | GPU Support
```

## 🎮 Configuration des Modèles

### Structure Attendue

Le système attend les modèles dans cette structure :

```
bouchon  et marque/
├── unified_detection_app/      # ← Vous êtes ici
├── test/
│   ├── yolov8n.pt              # Modèle bouteilles
│   └── bottle_recognition_system/
│       └── models/
│           ├── brand_classifier.h5          # Classificateur
│           └── brand_classifier_classes.json # Classes
└── Bottle-Bottle-Cap-Detection-System-main - Copie/
    └── best.pt                 # Modèle bouchons
```

### Télécharger les Modèles Manquants

#### YOLOv8n (Détection de Bouteilles)

Si `test/yolov8n.pt` est manquant :

```powershell
# Le téléchargement se fera automatiquement au premier lancement
# Ou manuellement :
cd ..\test
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### Modèle de Bouchons

Le modèle `best.pt` doit être présent dans le projet source.
Si manquant, entraînez-le ou obtenez-le depuis le projet original.

#### Classificateur de Marques

Le modèle `brand_classifier.h5` doit être présent.
Si manquant, entraînez-le ou obtenez-le depuis le projet original.

## 🔧 Installation avec GPU (Optionnel)

### NVIDIA GPU avec CUDA

#### 1. Vérifier la Compatibilité GPU

```powershell
nvidia-smi
```

#### 2. Installer CUDA et cuDNN

**CUDA 11.8** (recommandé pour TensorFlow 2.10+) :
1. Télécharger depuis : https://developer.nvidia.com/cuda-11-8-0-download-archive
2. Installer avec les options par défaut

**cuDNN 8.6** :
1. Télécharger depuis : https://developer.nvidia.com/cudnn
2. Extraire et copier les fichiers dans le dossier CUDA

#### 3. Installer TensorFlow GPU

```powershell
pip uninstall tensorflow
pip install tensorflow-gpu==2.10.0
```

#### 4. Vérifier l'Installation GPU

```powershell
python -c "import tensorflow as tf; print('GPU:', tf.config.list_physical_devices('GPU'))"
```

## 🐛 Résolution de Problèmes

### Problème : "pip n'est pas reconnu"

**Solution** :
```powershell
python -m pip install --upgrade pip
```

### Problème : "Impossible de créer venv"

**Solution** :
```powershell
# Installer le module venv
pip install virtualenv
virtualenv venv
```

### Problème : Erreur lors de l'installation de TensorFlow

**Solutions** :

1. **Vérifier la version de Python** (doit être 3.8-3.11) :
   ```powershell
   python --version
   ```

2. **Installer une version spécifique** :
   ```powershell
   pip install tensorflow==2.10.0
   ```

3. **Sur Windows avec Python 3.11+** :
   ```powershell
   # TensorFlow peut ne pas être compatible
   # Utiliser Python 3.10
   ```

### Problème : Erreur OpenCV "DLL load failed"

**Solution Windows** :
```powershell
pip uninstall opencv-python
pip install opencv-python-headless
pip install opencv-python
```

### Problème : Caméra non détectée

**Solutions** :

1. **Vérifier les permissions** :
   - Windows : Paramètres → Confidentialité → Caméra
   - Autoriser l'accès aux applications

2. **Tester avec un autre ID** :
   ```powershell
   python main.py --camera-id 1
   ```

3. **Vérifier avec OpenCV** :
   ```powershell
   python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
   ```

### Problème : ImportError pour Ultralytics

**Solution** :
```powershell
pip install ultralytics --upgrade
```

### Problème : FPS très faible (<5)

**Solutions** :

1. **Forcer le mode CPU** :
   ```powershell
   python main.py --cpu
   ```

2. **Réduire la résolution** dans `config.py` :
   ```python
   CameraConfig.FRAME_WIDTH = 640
   CameraConfig.FRAME_HEIGHT = 480
   ```

3. **Augmenter les seuils de confiance** :
   ```python
   DetectionConfig.BOTTLE_CONFIDENCE_THRESHOLD = 0.7
   DetectionConfig.CAP_CONFIDENCE_THRESHOLD = 0.7
   ```

## 🔄 Mise à Jour

Pour mettre à jour les dépendances :

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\activate

# Mettre à jour pip
python -m pip install --upgrade pip

# Mettre à jour les packages
pip install --upgrade -r requirements.txt
```

## 🧪 Tester l'Installation

### Test Rapide

```powershell
python test_setup.py
```

### Test Complet

```powershell
# Vérifier la configuration
python -c "from config import print_config_summary; print_config_summary()"

# Tester le pipeline
python -c "from detection_pipeline import UnifiedDetectionPipeline; p = UnifiedDetectionPipeline()"

# Tester les utilitaires
python utils.py
```

## 📚 Prochaines Étapes

Une fois l'installation réussie :

1. **Lire le guide rapide** : `QUICK_START.md`
2. **Lancer l'application** : `python main.py`
3. **Explorer la documentation** : `README.md`

## 🆘 Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. ✅ Vérifier cette documentation
2. 🔍 Exécuter `python test_setup.py`
3. 🐛 Lancer en mode debug : `python main.py --debug`
4. 📝 Consulter les logs : `outputs/logs/`

---

**Bonne installation ! 🚀**
