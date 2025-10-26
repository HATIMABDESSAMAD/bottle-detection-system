"""
Main Entry Point for Unified Detection System
=============================================
Launches the application with command-line argument support
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import tkinter as tk
from interface import DetectionInterface
from config import print_config_summary, validate_models


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Système Unifié de Détection de Bouteilles et Bouchons',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemples d'utilisation:
  python main.py                    # Lancer l'application normalement
  python main.py --check-models     # Vérifier les modèles
  python main.py --cpu              # Forcer l'utilisation du CPU
  python main.py --debug            # Mode debug avec logs détaillés
        '''
    )
    
    parser.add_argument(
        '--check-models',
        action='store_true',
        help='Vérifier la présence des modèles sans lancer l\'interface'
    )
    
    parser.add_argument(
        '--cpu',
        action='store_true',
        help='Forcer l\'utilisation du CPU (désactiver GPU)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Activer le mode debug avec logs détaillés'
    )
    
    parser.add_argument(
        '--camera-id',
        type=int,
        default=0,
        help='ID de la caméra à utiliser (défaut: 0)'
    )
    
    return parser.parse_args()


def check_models_status():
    """
    Check and display models status
    
    Returns:
        True if all models are found, False otherwise
    """
    print("\n" + "="*60)
    print("VÉRIFICATION DES MODÈLES")
    print("="*60)
    
    validation = validate_models()
    all_valid = True
    
    for model_name, exists in validation.items():
        status = "✓ TROUVÉ" if exists else "✗ MANQUANT"
        symbol = "✓" if exists else "✗"
        
        print(f"{symbol} {model_name.replace('_', ' ').title()}: {status}")
        
        if not exists:
            all_valid = False
    
    print("="*60)
    
    if all_valid:
        print("\n✓ Tous les modèles sont présents!")
    else:
        print("\n⚠ ATTENTION: Certains modèles sont manquants!")
        print("L'application fonctionnera en mode dégradé.")
        print("\nEmplacements attendus:")
        print("  - Détecteur de bouteilles: test/yolov8n.pt")
        print("  - Détecteur de bouchons: Bottle-Bottle-Cap-Detection-System-main - Copie/best.pt")
        print("  - Classificateur de marques: test/bottle_recognition_system/models/brand_classifier.h5")
    
    print()
    return all_valid


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Display configuration
    if args.debug:
        print_config_summary()
    
    # Check models if requested
    if args.check_models:
        check_models_status()
        sys.exit(0)
    
    # Update config based on arguments
    if args.cpu:
        from config import ProcessingConfig
        ProcessingConfig.ENABLE_GPU = False
        print("⚠ Mode CPU forcé - GPU désactivé")
    
    if args.camera_id != 0:
        from config import CameraConfig
        CameraConfig.DEVICE_ID = args.camera_id
        print(f"📷 Utilisation de la caméra ID: {args.camera_id}")
    
    # Check models before starting
    print("\n🔍 Vérification des modèles...")
    models_ok = check_models_status()
    
    if not models_ok:
        response = input("\nContinuer quand même? (o/N): ")
        if response.lower() != 'o':
            print("❌ Lancement annulé.")
            sys.exit(1)
    
    # Launch GUI
    try:
        print("\n🚀 Lancement de l'interface graphique...")
        print("   Initialisation en cours, veuillez patienter...\n")
        
        root = tk.Tk()
        app = DetectionInterface(root)
        
        print("✓ Interface lancée avec succès!")
        print("  Pour quitter: Fermez la fenêtre ou utilisez Ctrl+C\n")
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Arrêt demandé par l'utilisateur")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {e}")
        
        if args.debug:
            import traceback
            print("\nTrace complète:")
            traceback.print_exc()
        
        sys.exit(1)


if __name__ == "__main__":
    # Set up exception handling
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
