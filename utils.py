"""
Utility Functions for Unified Detection System
==============================================
Helper functions for image processing, annotations, FPS calculation, etc.
"""

import cv2
import numpy as np
import time
from typing import Tuple, List, Dict, Optional
from collections import deque
import json
from datetime import datetime
from pathlib import Path


class FPSCounter:
    """Calculate and track FPS over a rolling window"""
    
    def __init__(self, window_size: int = 30):
        """
        Initialize FPS counter
        
        Args:
            window_size: Number of frames to average over
        """
        self.window_size = window_size
        self.frame_times = deque(maxlen=window_size)
        self.last_time = time.time()
    
    def update(self) -> float:
        """
        Update FPS calculation
        
        Returns:
            Current FPS
        """
        current_time = time.time()
        self.frame_times.append(current_time - self.last_time)
        self.last_time = current_time
        
        if len(self.frame_times) > 0:
            return len(self.frame_times) / sum(self.frame_times)
        return 0.0
    
    def get_fps(self) -> float:
        """Get current FPS"""
        if len(self.frame_times) > 0:
            return len(self.frame_times) / sum(self.frame_times)
        return 0.0


class DetectionStatistics:
    """Track detection statistics"""
    
    def __init__(self):
        """Initialize statistics tracker"""
        self.reset()
    
    def reset(self):
        """Reset all statistics"""
        self.bottle_count = 0
        self.with_cap_count = 0
        self.without_cap_count = 0
        self.brand_counts = {}
        self.total_frames = 0
        self.start_time = time.time()
    
    def update(self, bottles: int = 0, with_cap: int = 0, without_cap: int = 0, 
               brands: List[str] = None):
        """
        Update statistics
        
        Args:
            bottles: Number of bottles detected
            with_cap: Number of objects with cap
            without_cap: Number of objects without cap
            brands: List of detected brands
        """
        self.bottle_count += bottles
        self.with_cap_count += with_cap
        self.without_cap_count += without_cap
        self.total_frames += 1
        
        if brands:
            for brand in brands:
                self.brand_counts[brand] = self.brand_counts.get(brand, 0) + 1
    
    def get_summary(self) -> Dict:
        """Get statistics summary"""
        elapsed_time = time.time() - self.start_time
        return {
            'bottles': self.bottle_count,
            'with_cap': self.with_cap_count,
            'without_cap': self.without_cap_count,
            'brands': dict(self.brand_counts),
            'total_frames': self.total_frames,
            'elapsed_time': elapsed_time,
            'avg_bottles_per_frame': self.bottle_count / max(1, self.total_frames),
            'avg_fps': self.total_frames / max(1, elapsed_time)
        }


def preprocess_image(image: np.ndarray, enhance_contrast: bool = True, 
                     denoise: bool = False) -> np.ndarray:
    """
    Preprocess image for better detection
    
    Args:
        image: Input image
        enhance_contrast: Apply contrast enhancement
        denoise: Apply denoising
        
    Returns:
        Preprocessed image
    """
    processed = image.copy()
    
    if enhance_contrast:
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        processed = cv2.merge([l, a, b])
        processed = cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)
    
    if denoise:
        processed = cv2.fastNlMeansDenoisingColored(processed, None, 10, 10, 7, 21)
    
    return processed


def extract_roi(image: np.ndarray, bbox: Tuple[int, int, int, int], 
                padding: float = 0.1) -> Optional[np.ndarray]:
    """
    Extract region of interest from image with optional padding
    
    Args:
        image: Source image
        bbox: Bounding box (x1, y1, x2, y2)
        padding: Padding percentage (0.1 = 10% padding)
        
    Returns:
        Cropped ROI or None if invalid
    """
    h, w = image.shape[:2]
    x1, y1, x2, y2 = bbox
    
    # Add padding
    box_w = x2 - x1
    box_h = y2 - y1
    pad_w = int(box_w * padding)
    pad_h = int(box_h * padding)
    
    # Ensure bounds
    x1 = max(0, x1 - pad_w)
    y1 = max(0, y1 - pad_h)
    x2 = min(w, x2 + pad_w)
    y2 = min(h, y2 + pad_h)
    
    if x2 <= x1 or y2 <= y1:
        return None
    
    return image[y1:y2, x1:x2]


def resize_for_classifier(image: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Resize image for classifier input
    
    Args:
        image: Input image
        target_size: Target size (width, height)
        
    Returns:
        Resized image
    """
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)


def draw_bounding_box(image: np.ndarray, bbox: Tuple[int, int, int, int],
                      label: str, confidence: float, color: Tuple[int, int, int],
                      thickness: int = 2, font_scale: float = 0.6) -> np.ndarray:
    """
    Draw bounding box with label on image
    
    Args:
        image: Input image
        bbox: Bounding box (x1, y1, x2, y2)
        label: Text label
        confidence: Confidence score
        color: Box color (BGR)
        thickness: Box line thickness
        font_scale: Font scale for text
        
    Returns:
        Image with drawn box
    """
    x1, y1, x2, y2 = map(int, bbox)
    
    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    
    # Prepare label text
    text = f"{label}: {confidence:.2f}"

    # Get text size
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Draw text background (top)
    cv2.rectangle(image, (x1, y1 - text_height - baseline - 5), 
                  (x1 + text_width, y1), color, -1)
    # Draw text (top)
    cv2.putText(image, text, (x1, y1 - baseline - 2), 
                font, font_scale, (255, 255, 255), thickness)

    return image

def draw_bounding_box_bottom(image: np.ndarray, bbox: Tuple[int, int, int, int],
                             label: str, confidence: float, color: Tuple[int, int, int],
                             thickness: int = 2, font_scale: float = 0.6) -> np.ndarray:
    """
    Draw bounding box with label below the box (for brand)
    """
    x1, y1, x2, y2 = map(int, bbox)
    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    # Prepare label text
    text = f"{label}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    # Draw text background (bottom)
    cv2.rectangle(image, (x1, y2), (x1 + text_width, y2 + text_height + baseline + 5), color, -1)
    # Draw text (bottom)
    cv2.putText(image, text, (x1, y2 + text_height + baseline), font, font_scale, (255, 255, 255), thickness)
    return image


def draw_detection_info(image: np.ndarray, fps: float, detection_counts: Dict,
                        processing_time: float = None, 
                        position: str = 'top-left') -> np.ndarray:
    """
    Draw detection information overlay on image
    
    Args:
        image: Input image
        fps: Current FPS
        detection_counts: Dictionary with detection counts
        processing_time: Processing time in seconds
        position: Position of info ('top-left', 'top-right', 'bottom-left', 'bottom-right')
        
    Returns:
        Image with info overlay
    """
    h, w = image.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    color = (255, 255, 255)
    bg_color = (0, 0, 0)
    
    # Build info text
    info_lines = [
        f"FPS: {fps:.1f}",
        f"Bottles: {detection_counts.get('bottles', 0)}",
        f"With Cap: {detection_counts.get('with_cap', 0)}",
        f"Without Cap: {detection_counts.get('without_cap', 0)}"
    ]
    
    if processing_time:
        info_lines.append(f"Process: {processing_time*1000:.1f}ms")
    
    # Calculate position
    line_height = 25
    padding = 10
    
    if position == 'top-left':
        x, y = padding, padding + 20
    elif position == 'top-right':
        x, y = w - 200, padding + 20
    elif position == 'bottom-left':
        x, y = padding, h - len(info_lines) * line_height - padding
    else:  # bottom-right
        x, y = w - 200, h - len(info_lines) * line_height - padding
    
    # Draw background rectangle
    cv2.rectangle(image, (x - 5, y - 20), 
                  (x + 190, y + len(info_lines) * line_height), 
                  bg_color, -1)
    
    # Draw text lines
    for i, line in enumerate(info_lines):
        cv2.putText(image, line, (x, y + i * line_height), 
                    font, font_scale, color, thickness)
    
    return image


def save_screenshot(image: np.ndarray, output_dir: Path, 
                    prefix: str = "screenshot") -> str:
    """
    Save screenshot with timestamp
    
    Args:
        image: Image to save
        output_dir: Output directory
        prefix: Filename prefix
        
    Returns:
        Path to saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = output_dir / filename
    
    cv2.imwrite(str(filepath), image)
    return str(filepath)


def create_video_writer(output_path: Path, fps: int, frame_size: Tuple[int, int],
                       codec: str = 'mp4v') -> cv2.VideoWriter:
    """
    Create video writer object
    
    Args:
        output_path: Output video path
        fps: Frames per second
        frame_size: Frame size (width, height)
        codec: Video codec
        
    Returns:
        VideoWriter object
    """
    fourcc = cv2.VideoWriter_fourcc(*codec)
    return cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)


def log_detection_event(log_dir: Path, event_type: str, data: Dict):
    """
    Log detection event to JSON file
    
    Args:
        log_dir: Log directory
        event_type: Type of event
        data: Event data
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'event_type': event_type,
        'data': data
    }
    
    log_file = log_dir / f"detection_log_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Append to log file
    logs = []
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)


def calculate_iou(box1: Tuple[int, int, int, int], 
                  box2: Tuple[int, int, int, int]) -> float:
    """
    Calculate Intersection over Union (IoU) between two boxes
    
    Args:
        box1: First box (x1, y1, x2, y2)
        box2: Second box (x1, y1, x2, y2)
        
    Returns:
        IoU value
    """
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    # Calculate intersection
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return 0.0
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Calculate union
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0


def apply_nms(boxes: List[Tuple], scores: List[float], 
              iou_threshold: float = 0.45) -> List[int]:
    """
    Apply Non-Maximum Suppression
    
    Args:
        boxes: List of bounding boxes
        scores: List of confidence scores
        iou_threshold: IoU threshold for suppression
        
    Returns:
        Indices of boxes to keep
    """
    if len(boxes) == 0:
        return []
    
    # Sort by score
    indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    keep = []
    
    while indices:
        current = indices[0]
        keep.append(current)
        indices = indices[1:]
        
        # Remove boxes with high IoU
        indices = [i for i in indices 
                   if calculate_iou(boxes[current], boxes[i]) < iou_threshold]
    
    return keep


if __name__ == "__main__":
    # Test utilities
    print("Utility functions loaded successfully!")
    
    # Test FPS counter
    fps_counter = FPSCounter()
    for _ in range(10):
        time.sleep(0.033)  # ~30 FPS
        fps = fps_counter.update()
    print(f"FPS Test: {fps_counter.get_fps():.2f} FPS")
    
    # Test statistics
    stats = DetectionStatistics()
    stats.update(bottles=2, with_cap=1, brands=["Aquafina", "Bahia"])
    print(f"Statistics: {stats.get_summary()}")
