"""
Unified Detection System Package
=================================

Application Python pour la détection et classification d'objets en temps réel.
Combine YOLOv8 pour la détection et ResNet pour la classification.

Modules:
    - config: Configuration centralisée
    - detection_pipeline: Pipeline de détection unifié
    - interface: Interface graphique Tkinter
    - utils: Fonctions utilitaires
    - main: Point d'entrée de l'application

Usage:
    python main.py
"""

__version__ = "1.0.0"
__author__ = "Unified Detection Team"
__date__ = "October 2025"

# Package metadata
__all__ = [
    'config',
    'detection_pipeline',
    'interface',
    'utils',
    'main'
]
