# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées ici.

## [1.0.0] - 2025-10-12

### 🎉 Version Initiale

#### ✨ Fonctionnalités Ajoutées

**Détection Multi-Objets**
- Détection de bouteilles avec YOLOv8
- Détection de bouchons (5 classes : Good Cap, Loose Cap, Broken Cap, Broken Ring, No Cap)
- Classification de marques avec ResNet50V2 (10 marques)

**Interface Graphique**
- Interface Tkinter moderne avec thème sombre
- Flux vidéo en temps réel
- Panneau de statistiques dynamique
- Boutons de contrôle :
  - Démarrer/Arrêter caméra
  - Capture d'écran
  - Enregistrement vidéo
- Options configurables :
  - Activer/Désactiver chaque type de détection
  - Sliders pour ajuster les seuils de confiance

**Pipeline de Détection**
- Architecture unifiée combinant 2 modèles YOLOv8 + 1 ResNet
- Traitement en temps réel (>15 FPS)
- Support GPU avec TensorFlow
- Classification automatique des marques pour les bouteilles détectées

**Utilitaires**
- Calcul FPS en temps réel
- Tracking des statistiques de détection
- Prétraitement d'images (CLAHE, débruitage)
- Extraction ROI intelligente
- Annotations colorées avec bounding boxes
- Sauvegarde de screenshots
- Enregistrement vidéo
- Logging des événements

**Configuration**
- Configuration centralisée dans `config.py`
- Chemins de modèles configurables
- Paramètres de détection ajustables
- Palette de couleurs personnalisable
- Options de performance

**Documentation**
- README.md complet
- QUICK_START.md pour démarrage rapide
- INSTALLATION_GUIDE.md détaillé
- PROJECT_OVERVIEW.md architecture technique
- START_HERE.md point d'entrée
- Docstrings pour toutes les fonctions

**Scripts Utilitaires**
- `main.py` : Point d'entrée avec arguments CLI
- `demo.py` : Mode démo sans GUI
- `test_setup.py` : Tests d'installation
- `run.bat` : Lanceur automatique Windows

#### 🎨 Design

- Interface moderne avec thème sombre
- Code couleur des détections :
  - 🔵 Bleu : Bouteilles
  - 🟢 Vert : Avec bouchon
  - 🔴 Rouge : Sans bouchon
- Emojis pour meilleure UX
- Layout responsive

#### ⚙️ Configuration

- Support Windows, Linux, macOS
- Python 3.8+
- GPU optionnel mais recommandé
- Mode CPU fallback

#### 📦 Dépendances

- TensorFlow >= 2.10.0
- OpenCV >= 4.8.0
- Ultralytics >= 8.0.0
- Pillow >= 10.0.0
- NumPy >= 1.24.0

---

## [Roadmap] - Futures Versions

### Version 1.1.0 (Planifiée)

#### 🔮 Fonctionnalités Prévues

- [ ] Support multi-caméras simultanées
- [ ] Export des statistiques en CSV/Excel
- [ ] Mode batch pour traiter des vidéos existantes
- [ ] Notifications en temps réel (email/webhooks)
- [ ] Dashboard web avec Flask/FastAPI

### Version 1.2.0 (Planifiée)

#### 🚀 Améliorations

- [ ] Optimisation des performances (multi-threading)
- [ ] Support de nouvelles marques de bouteilles
- [ ] Détection de défauts supplémentaires
- [ ] API REST pour intégration
- [ ] Base de données pour historique

### Version 1.3.0 (Planifiée)

#### 🤖 Intelligence Artificielle

- [ ] Tracking d'objets multi-frames
- [ ] Reconnaissance de codes-barres
- [ ] Analyse de qualité d'image
- [ ] Détection d'anomalies avancée
- [ ] Apprentissage continu

### Version 2.0.0 (Future)

#### 💎 Évolutions Majeures

- [ ] Réécriture en PyQt6 pour UI moderne
- [ ] Support mobile (Android/iOS)
- [ ] Cloud deployment
- [ ] Modèles optimisés (ONNX, TensorRT)
- [ ] Interface multilingue

---

## 📊 Format du Changelog

Ce changelog suit le format [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

### Types de Changements

- **✨ Added** : Nouvelles fonctionnalités
- **🔧 Changed** : Modifications de fonctionnalités existantes
- **⚠️ Deprecated** : Fonctionnalités obsolètes
- **🗑️ Removed** : Fonctionnalités supprimées
- **🐛 Fixed** : Corrections de bugs
- **🔒 Security** : Correctifs de sécurité

---

**Dernière mise à jour** : 12 Octobre 2025
