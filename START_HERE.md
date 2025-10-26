# 🎯 COMMENCEZ ICI !

Bienvenue dans le **Système Unifié de Détection de Bouteilles et Bouchons** ! 🚀

## 🎬 Démarrage en 30 Secondes

### Option 1 : Double-Clic (Windows)
```
📁 Double-cliquez sur : run.bat
```
✅ Tout sera installé et lancé automatiquement !

### Option 2 : Ligne de Commande
```powershell
pip install -r requirements.txt
python main.py
```

## 📚 Documentation

Choisissez votre niveau :

### 🟢 Débutant
- **`QUICK_START.md`** ← Commencez par là !
  - Installation simple
  - Utilisation de base
  - Résolution de problèmes courants

### 🟡 Intermédiaire  
- **`README.md`** 
  - Documentation complète
  - Toutes les fonctionnalités
  - Configuration avancée

### 🔴 Avancé
- **`PROJECT_OVERVIEW.md`**
  - Architecture détaillée
  - Flux de données
  - Aspects techniques

- **`INSTALLATION_GUIDE.md`**
  - Installation GPU/CUDA
  - Résolution de problèmes avancés
  - Optimisation des performances

## ✅ Checklist de Démarrage

Avant de lancer l'application :

- [ ] Python 3.8+ installé
- [ ] Webcam fonctionnelle
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Modèles présents (vérifier avec `python main.py --check-models`)

## 🎮 Commandes Principales

```powershell
# Lancer l'application
python main.py

# Vérifier l'installation
python test_setup.py

# Vérifier les modèles
python main.py --check-models

# Mode démo (sans GUI)
python demo.py

# Forcer le mode CPU
python main.py --cpu

# Mode debug
python main.py --debug
```

## 🎨 Que Va Faire Cette Application ?

L'application détectera en temps réel :

1. 🍶 **Bouteilles** (avec leur marque)
   - Ain Atlas
   - Ain Ifrane
   - Aquafina
   - Bahia
   - Oulmes
   - Sidi Ali
   - ... et 4 autres marques

2. ✅ **Objets avec bouchon**
   - Bouchon bon état
   - Bouchon desserré
   - Bouchon cassé

3. ❌ **Objets sans bouchon**

## 🖼️ Interface

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────────────────┐  ┌──────────────────────────┐ │
│  │                         │  │  📊 STATISTIQUES         │ │
│  │    📹 FLUX VIDÉO       │  │                          │ │
│  │    EN TEMPS RÉEL       │  │  FPS: 25.3               │ │
│  │                         │  │  🍶 Bouteilles: 2        │ │
│  │  [Détections affichées] │  │  ✅ Avec Bouchon: 1      │ │
│  │                         │  │  ❌ Sans Bouchon: 1      │ │
│  │                         │  │                          │ │
│  │                         │  │  🏷️ Marques:            │ │
│  │                         │  │  • Aquafina              │ │
│  └─────────────────────────┘  │  • Bahia                 │ │
│                                │                          │ │
│  ▶️ Démarrer  📷 Capture     │  ⚙️ OPTIONS              │ │
│  ⏺️ Enregistrer              │  ☑️ Détecter bouteilles  │ │
│                                │  ☑️ Détecter bouchons    │ │
│                                │  ☑️ Classifier marques   │ │
│                                │                          │ │
│                                │  🎚️ Seuils Confiance   │ │
│                                │  Bouteilles: ────●───    │ │
│                                │  Bouchons:   ────●───    │ │
│                                └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Premiers Pas Recommandés

1. **Installer** : Suivez `QUICK_START.md`
2. **Tester** : `python test_setup.py`
3. **Lancer** : `python main.py`
4. **Expérimenter** : Essayez les différentes options
5. **Explorer** : Consultez `README.md` pour plus de détails

## ⚙️ Structure des Fichiers

```
unified_detection_app/
│
├── 📄 START_HERE.md          ← Vous êtes ici !
├── 📄 QUICK_START.md         ← Guide rapide
├── 📄 README.md              ← Documentation complète
├── 📄 INSTALLATION_GUIDE.md  ← Guide installation détaillé
├── 📄 PROJECT_OVERVIEW.md    ← Architecture technique
│
├── 🐍 main.py                ← LANCEZ CECI
├── 🐍 config.py              ← Configuration
├── 🐍 detection_pipeline.py  ← Détection IA
├── 🐍 interface.py           ← Interface graphique
├── 🐍 utils.py               ← Fonctions utilitaires
├── 🐍 demo.py                ← Mode démo
├── 🐍 test_setup.py          ← Tests d'installation
│
├── 🦇 run.bat                ← Lanceur Windows
├── 📋 requirements.txt       ← Dépendances Python
│
└── 📁 outputs/               ← Screenshots, vidéos, logs
```

## 🆘 Problèmes ?

### Erreur au lancement ?
1. Vérifier : `python test_setup.py`
2. Consulter : `INSTALLATION_GUIDE.md`
3. Mode debug : `python main.py --debug`

### Caméra ne fonctionne pas ?
```powershell
python main.py --camera-id 1
```

### FPS trop bas ?
```powershell
python main.py --cpu
```

## 🎓 Tutoriel Vidéo (Conceptuel)

1. **Installation** (2 min)
   - Installer Python
   - Installer dépendances
   - Vérifier modèles

2. **Premier Lancement** (1 min)
   - Démarrer l'application
   - Présentation de l'interface

3. **Utilisation** (3 min)
   - Démarrer la caméra
   - Tester les détections
   - Prendre des captures
   - Enregistrer une vidéo

4. **Configuration** (2 min)
   - Ajuster les seuils
   - Activer/désactiver détections
   - Options avancées

## 💡 Conseils Pro

- 💡 Utilisez un bon éclairage pour de meilleures détections
- 💡 Placez les objets à 30-50 cm de la caméra
- 💡 Fond uni = meilleurs résultats
- 💡 Ajustez les seuils si trop/pas assez de détections

## 🎯 Objectifs du Projet

Ce système unifie deux projets :
- ✅ Détection de bouteilles + classification de marques
- ✅ Détection d'objets avec/sans bouchon

**Résultat** : Un système complet de contrôle qualité !

## 📞 Support

1. ✅ Consultez la documentation
2. 🔍 Utilisez `python main.py --debug`
3. 📝 Vérifiez les logs : `outputs/logs/`

## 🚀 C'est Parti !

**Prêt à commencer ?**

```powershell
# Windows : Double-clic
run.bat

# Ou ligne de commande
python main.py
```

---

**Bon détection ! 🎉🍶**

**Questions fréquentes dans `QUICK_START.md`**
