"""
Configuration Module for Unified Detection System
==================================================
Centralized configuration for paths, parameters, colors, and settings
"""

import os
from pathlib import Path

# ==================== PROJECT PATHS ====================
# Base directories
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent

# YOLOv8 Models (external paths)
BOTTLE_YOLO_MODEL = PROJECT_ROOT / "test" / "yolov8n.pt"  # For bottle detection (box_bottle)
CAP_YOLO_MODEL = PROJECT_ROOT / "Bottle-Bottle-Cap-Detection-System-main - Copie" / "best.pt"  # For cap detection

# ResNet Brand Classifier (external paths)
BRAND_CLASSIFIER_MODEL = PROJECT_ROOT / "test" / "bottle_recognition_system" / "models" / "compatible_classifier.h5"
BRAND_CLASSES_JSON = PROJECT_ROOT / "test" / "bottle_recognition_system" / "models" / "compatible_classifier_classes.json"

# Output directories
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"
VIDEOS_DIR = OUTPUT_DIR / "videos"
LOGS_DIR = OUTPUT_DIR / "logs"

# Create output directories
for directory in [OUTPUT_DIR, SCREENSHOTS_DIR, VIDEOS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# ==================== DETECTION PARAMETERS ====================
class DetectionConfig:
    """Detection configuration parameters"""
    
    # YOLO Detection Parameters
    BOTTLE_CONFIDENCE_THRESHOLD = 0.5  # Confidence for bottle detection
    CAP_CONFIDENCE_THRESHOLD = 0.6     # Confidence for cap detection
    IOU_THRESHOLD = 0.45               # IoU threshold for NMS
    
    # Brand Classification Parameters
    BRAND_CONFIDENCE_THRESHOLD = 0.4   # Minimum confidence for brand classification
    BRAND_INPUT_SIZE = (224, 224)      # Input size for ResNet classifier
    
    # COCO class IDs
    BOTTLE_CLASS_ID = 39  # Standard COCO class for bottle
    
    # Cap detection classes (from data.yaml)
    CAP_CLASSES = {
        'Broken Cap': 0,
        'Avec Bouchon': 1,   # Remplace Broken Ring
        'Sans Bouchon': 2,  # Remplace Good Cap
        'Sans Bouchon': 3,  # Remplace Loose Cap
        'Avec Bouchon': 4   # Remplace No Cap
    }

    # Reverse mapping for cap classes
    CAP_ID_TO_NAME = {0: 'Broken Cap', 1: 'Avec Bouchon', 2: 'Sans Bouchon', 3: 'Sans Bouchon', 4: 'Avec Bouchon'}
    
    # Brand classes (loaded dynamically from JSON)
    BRAND_CLASSES = [
        "Ain_Atlas", "Ain_Ifrane", "Ain_Saiss", "Aquafina", "Bahia",
        "Ifrane", "Mondariz", "Oulmes", "Sidi_Ali", "Sidi_Hrazem"
    ]

# ==================== CAMERA CONFIGURATION ====================
class CameraConfig:
    """Camera and video capture settings"""
    
    DEVICE_ID = 0               # Default camera device
    FRAME_WIDTH = 640           # Capture width (compatibilité maximale)
    FRAME_HEIGHT = 480          # Capture height (compatibilité maximale)
    FPS = 30                    # Target FPS
    
    # Video recording settings
    VIDEO_CODEC = 'mp4v'        # Codec for video recording
    VIDEO_EXTENSION = '.mp4'    # Video file extension

# ==================== UI CONFIGURATION ====================
class UIConfig:
    """User interface settings and colors"""
    
    # Window settings
    WINDOW_TITLE = "Système de Détection Unifié - Bouteilles & Bouchons"
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    
    # Video display settings
    VIDEO_DISPLAY_WIDTH = 960
    VIDEO_DISPLAY_HEIGHT = 720
    
    # Colors for bounding boxes (BGR format for OpenCV)
    COLORS = {
        'bottle': (255, 0, 0),       # Blue for bottles
        'with_cap': (0, 255, 0),     # Green for objects with cap
        'without_cap': (0, 0, 255),  # Red for objects without cap
        'good_cap': (0, 200, 0),     # Dark green for good caps
        'bad_cap': (0, 165, 255)     # Orange for broken/loose caps
    }
    
    # Text settings
    FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    FONT_THICKNESS = 2
    TEXT_COLOR = (255, 255, 255)  # White
    TEXT_BG_COLOR = (0, 0, 0)     # Black background
    
    # Box settings
    BOX_THICKNESS = 2
    
    # Statistics panel colors
    PANEL_BG_COLOR = "#2b2b2b"
    PANEL_TEXT_COLOR = "#ffffff"
    PANEL_HIGHLIGHT_COLOR = "#4a9eff"

# ==================== PROCESSING CONFIGURATION ====================
class ProcessingConfig:
    """Processing and performance settings"""
    
    # Performance
    ENABLE_GPU = True           # Use GPU if available
    MAX_FPS = 30                # Maximum FPS cap
    SKIP_FRAMES = 0             # Skip frames for performance (0 = no skip)
    
    # Image preprocessing
    ENHANCE_CONTRAST = True     # Apply contrast enhancement
    DENOISE = False             # Apply denoising (slower)
    
    # Detection modes (can be toggled in UI)
    ENABLE_BOTTLE_DETECTION = True
    ENABLE_CAP_DETECTION = True
    ENABLE_BRAND_CLASSIFICATION = True
    
    # Display options
    SHOW_FPS = True
    SHOW_CONFIDENCE = True
    SHOW_PROCESSING_TIME = True
    SHOW_STATISTICS = True

# ==================== HELPER FUNCTIONS ====================
def get_model_path(model_name: str) -> Path:
    """
    Get the full path for a model file
    
    Args:
        model_name: Name of the model
        
    Returns:
        Full path to the model
    """
    paths = {
        'bottle_yolo': BOTTLE_YOLO_MODEL,
        'cap_yolo': CAP_YOLO_MODEL,
        'brand_classifier': BRAND_CLASSIFIER_MODEL
    }
    return paths.get(model_name, BASE_DIR / model_name)

def validate_models() -> dict:
    """
    Validate that all required models exist
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'bottle_yolo': BOTTLE_YOLO_MODEL.exists(),
        'cap_yolo': CAP_YOLO_MODEL.exists(),
        'brand_classifier': BRAND_CLASSIFIER_MODEL.exists(),
        'brand_classes': BRAND_CLASSES_JSON.exists()
    }
    return results

def print_config_summary():
    """Print configuration summary for debugging"""
    print("=" * 60)
    print("UNIFIED DETECTION SYSTEM - CONFIGURATION")
    print("=" * 60)
    print(f"Base Directory: {BASE_DIR}")
    print(f"\nModel Paths:")
    print(f"  - Bottle YOLO: {BOTTLE_YOLO_MODEL}")
    print(f"  - Cap YOLO: {CAP_YOLO_MODEL}")
    print(f"  - Brand Classifier: {BRAND_CLASSIFIER_MODEL}")
    print(f"\nModel Validation:")
    for model, exists in validate_models().items():
        status = "✓ Found" if exists else "✗ Missing"
        print(f"  - {model}: {status}")
    print(f"\nOutput Directories:")
    print(f"  - Screenshots: {SCREENSHOTS_DIR}")
    print(f"  - Videos: {VIDEOS_DIR}")
    print(f"  - Logs: {LOGS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    # Test configuration
    print_config_summary()
