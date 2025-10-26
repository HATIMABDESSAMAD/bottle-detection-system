"""
Unified Detection Pipeline
===========================
Combines YOLOv8 detection for bottles and caps with ResNet brand classification
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path

from config import (
    DetectionConfig, BOTTLE_YOLO_MODEL, CAP_YOLO_MODEL,
    BRAND_CLASSIFIER_MODEL, BRAND_CLASSES_JSON
)
from utils import extract_roi, resize_for_classifier


class UnifiedDetectionPipeline:
    """
    Unified detection pipeline combining:
    - YOLOv8 for bottle detection (box_bottle)
    - YOLOv8 for cap detection (with_cap/without_cap)
    - ResNet for brand classification
    """
    
    def __init__(self, enable_gpu: bool = True):
        """
        Initialize the unified detection pipeline
        
        Args:
            enable_gpu: Enable GPU acceleration
        """
        self.enable_gpu = enable_gpu
        self._configure_gpu()
        
        # Models
        self.bottle_detector = None
        self.cap_detector = None
        self.brand_classifier = None
        self.brand_classes = []
        
        # Configuration
        self.bottle_conf = DetectionConfig.BOTTLE_CONFIDENCE_THRESHOLD
        self.cap_conf = DetectionConfig.CAP_CONFIDENCE_THRESHOLD
        self.iou_threshold = DetectionConfig.IOU_THRESHOLD
        self.brand_conf = DetectionConfig.BRAND_CONFIDENCE_THRESHOLD
        
        # Load models
        self._load_models()
        
        print("✓ Unified Detection Pipeline initialized successfully!")
    
    def _configure_gpu(self):
        """Configure GPU settings for TensorFlow"""
        if self.enable_gpu:
            try:
                gpus = tf.config.list_physical_devices('GPU')
                if gpus:
                    for gpu in gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                    print(f"✓ GPU enabled: {len(gpus)} GPU(s) available")
                else:
                    print("⚠ No GPU found, using CPU")
            except Exception as e:
                print(f"⚠ GPU configuration error: {e}")
        else:
            # Disable GPU
            tf.config.set_visible_devices([], 'GPU')
            print("✓ Running on CPU mode")
    
    def _load_models(self):
        """Load all detection and classification models"""
        try:
            # Load bottle detection model (YOLOv8)
            if BOTTLE_YOLO_MODEL.exists():
                print(f"Loading bottle detector: {BOTTLE_YOLO_MODEL}")
                self.bottle_detector = YOLO(str(BOTTLE_YOLO_MODEL))
                print("✓ Bottle detector loaded")
            else:
                print(f"⚠ Bottle detector not found at {BOTTLE_YOLO_MODEL}")
                print("  Loading default YOLOv8n model...")
                self.bottle_detector = YOLO('yolov8n.pt')
            
            # Load cap detection model (YOLOv8)
            if CAP_YOLO_MODEL.exists():
                print(f"Loading cap detector: {CAP_YOLO_MODEL}")
                self.cap_detector = YOLO(str(CAP_YOLO_MODEL))
                print("✓ Cap detector loaded")
            else:
                print(f"⚠ Cap detector not found at {CAP_YOLO_MODEL}")
                self.cap_detector = None
            
            # Load brand classifier (ResNet)
            if BRAND_CLASSIFIER_MODEL.exists():
                print(f"Loading brand classifier: {BRAND_CLASSIFIER_MODEL}")
                try:
                    self.brand_classifier = keras.models.load_model(str(BRAND_CLASSIFIER_MODEL), compile=False)
                    print("✓ Brand classifier loaded (compile=False)")
                except Exception as e:
                    print(f"✗ Error loading brand classifier: {e}")
                    print("[INFO] Classification de marque désactivée. Le reste du système reste fonctionnel.")
                    self.brand_classifier = None
                # Load brand classes
                if BRAND_CLASSES_JSON.exists():
                    with open(BRAND_CLASSES_JSON, 'r') as f:
                        self.brand_classes = json.load(f)
                    print(f"✓ Loaded {len(self.brand_classes)} brand classes")
                else:
                    self.brand_classes = DetectionConfig.BRAND_CLASSES
                    print(f"⚠ Using default brand classes")
            else:
                print(f"⚠ Brand classifier not found at {BRAND_CLASSIFIER_MODEL}")
                print("[INFO] Classification de marque désactivée. Le reste du système reste fonctionnel.")
                self.brand_classifier = None
            
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            raise
    
    def detect_bottles(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect bottles in frame using YOLOv8
        
        Args:
            frame: Input frame
            
        Returns:
            List of detection dictionaries with bbox, confidence
        """
        if self.bottle_detector is None:
            return []
        
        try:
            results = self.bottle_detector(frame, conf=self.bottle_conf, 
                                          iou=self.iou_threshold, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class ID
                    cls_id = int(box.cls[0])
                    
                    # Filter for bottle class (COCO class 39)
                    if cls_id == DetectionConfig.BOTTLE_CLASS_ID:
                        xyxy = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0])
                        
                        detections.append({
                            'type': 'bottle',
                            'bbox': tuple(map(int, xyxy)),
                            'confidence': conf,
                            'class_id': cls_id
                        })
            
            return detections
            
        except Exception as e:
            print(f"Error in bottle detection: {e}")
            return []
    
    def detect_caps(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect caps in frame using YOLOv8
        
        Args:
            frame: Input frame
            
        Returns:
            List of detection dictionaries with bbox, confidence, cap_status
        """
        if self.cap_detector is None:
            return []
        
        try:
            results = self.cap_detector(frame, conf=self.cap_conf, 
                                       iou=self.iou_threshold, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    
                    # Get cap status from class name
                    cap_status = DetectionConfig.CAP_ID_TO_NAME.get(cls_id, "Unknown")
                    # Nouvelle catégorisation corrigée
                    if cap_status == 'Avec Bouchon':
                        category = 'with_cap'
                    elif cap_status == 'Sans Bouchon':
                        category = 'without_cap'
                    elif cap_status == 'Broken Cap':
                        category = 'broken_cap'
                    else:
                        category = 'unknown'

                    detections.append({
                        'type': 'cap',
                        'category': category,
                        'cap_status': cap_status,
                        'bbox': tuple(map(int, xyxy)),
                        'confidence': conf,
                        'class_id': cls_id
                    })
            
            return detections
            
        except Exception as e:
            print(f"Error in cap detection: {e}")
            return []
    
    def classify_brand(self, frame: np.ndarray, bbox: Tuple[int, int, int, int]) -> Optional[Dict]:
        """
        Classify bottle brand from ROI
        
        Args:
            frame: Input frame
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Dictionary with brand name and confidence, or None
        """
        if self.brand_classifier is None or len(self.brand_classes) == 0:
            # Classification désactivée, retourne None
            return None
        
        try:
            # Extract ROI
            roi = extract_roi(frame, bbox, padding=0.05)
            if roi is None or roi.size == 0:
                return None
            
            # Preprocess for classifier
            roi_resized = resize_for_classifier(roi, DetectionConfig.BRAND_INPUT_SIZE)
            roi_normalized = roi_resized.astype(np.float32) / 255.0
            roi_batch = np.expand_dims(roi_normalized, axis=0)
            
            # Predict
            predictions = self.brand_classifier.predict(roi_batch, verbose=0)
            
            # Get top prediction
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            # Check confidence threshold
            if confidence < self.brand_conf:
                return None
            
            brand_name = self.brand_classes[class_idx]
            
            return {
                'brand': brand_name,
                'confidence': confidence
            }
            
        except Exception as e:
            print(f"Error in brand classification: {e}")
            return None
    
    def process_frame(self, frame: np.ndarray, 
                     enable_bottle: bool = True,
                     enable_cap: bool = True,
                     enable_brand: bool = True) -> Dict:
        """
        Process a single frame with all detection and classification
        
        Args:
            frame: Input frame
            enable_bottle: Enable bottle detection
            enable_cap: Enable cap detection
            enable_brand: Enable brand classification
            
        Returns:
            Dictionary with all detections and classifications
        """
        results = {
            'bottles': [],
            'caps': [],
            'frame_shape': frame.shape
        }
        
        # Detect bottles
        if enable_bottle:
            bottle_detections = self.detect_bottles(frame)
            
            # Classify brands for each bottle
            if enable_brand:
                for detection in bottle_detections:
                    brand_info = self.classify_brand(frame, detection['bbox'])
                    if brand_info:
                        detection['brand'] = brand_info['brand']
                        detection['brand_confidence'] = brand_info['confidence']
            
            results['bottles'] = bottle_detections
        
        # Detect caps
        if enable_cap:
            cap_detections = self.detect_caps(frame)
            results['caps'] = cap_detections
        
        return results
    
    def get_detection_counts(self, results: Dict) -> Dict:
        """
        Get counts of detected objects
        
        Args:
            results: Detection results from process_frame
            
        Returns:
            Dictionary with counts
        """
        counts = {
            'bottles': len(results.get('bottles', [])),
            'with_cap': 0,
            'without_cap': 0,
            'total_caps': len(results.get('caps', []))
        }
        
        # Count caps by category
        for cap in results.get('caps', []):
            category = cap.get('category', 'unknown')
            if category == 'with_cap':
                counts['with_cap'] += 1
            elif category == 'without_cap':
                counts['without_cap'] += 1
        
        return counts
    
    def get_detected_brands(self, results: Dict) -> List[str]:
        """
        Get list of detected brands
        
        Args:
            results: Detection results from process_frame
            
        Returns:
            List of brand names
        """
        brands = []
        for bottle in results.get('bottles', []):
            if 'brand' in bottle:
                brands.append(bottle['brand'])
        return brands
    
    def update_confidence_thresholds(self, bottle_conf: float = None,
                                    cap_conf: float = None,
                                    brand_conf: float = None):
        """
        Update confidence thresholds
        
        Args:
            bottle_conf: Bottle detection confidence
            cap_conf: Cap detection confidence
            brand_conf: Brand classification confidence
        """
        if bottle_conf is not None:
            self.bottle_conf = bottle_conf
        if cap_conf is not None:
            self.cap_conf = cap_conf
        if brand_conf is not None:
            self.brand_conf = brand_conf
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            'bottle_detector': self.bottle_detector is not None,
            'cap_detector': self.cap_detector is not None,
            'brand_classifier': self.brand_classifier is not None,
            'num_brands': len(self.brand_classes),
            'brands': self.brand_classes
        }


if __name__ == "__main__":
    # Test the pipeline
    print("Testing Unified Detection Pipeline...")
    
    try:
        pipeline = UnifiedDetectionPipeline(enable_gpu=True)
        
        # Print model info
        info = pipeline.get_model_info()
        print("\nModel Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print("\n✓ Pipeline test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Pipeline test failed: {e}")
