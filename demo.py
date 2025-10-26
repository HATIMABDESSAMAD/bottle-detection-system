"""
Demo Script - Unified Detection System
======================================
Simple demonstration without GUI for testing
"""

import cv2
import time
from pathlib import Path

from detection_pipeline import UnifiedDetectionPipeline
from utils import FPSCounter, draw_bounding_box, draw_detection_info
from config import UIConfig, CameraConfig


def run_demo(duration_seconds: int = 30, save_output: bool = True):
    """
    Run a simple demo of the detection system
    
    Args:
        duration_seconds: How long to run the demo
        save_output: Whether to save output video
    """
    print("="*60)
    print("UNIFIED DETECTION SYSTEM - DEMO MODE")
    print("="*60)
    print()
    
    # Initialize pipeline
    print("Initializing detection pipeline...")
    try:
        pipeline = UnifiedDetectionPipeline(enable_gpu=True)
        print("✓ Pipeline initialized")
    except Exception as e:
        print(f"✗ Failed to initialize pipeline: {e}")
        return
    
    # Open camera
    print("Opening camera...")
    camera = cv2.VideoCapture(CameraConfig.DEVICE_ID, cv2.CAP_DSHOW)
    
    if not camera.isOpened():
        print("✗ Cannot open camera")
        return
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CameraConfig.FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraConfig.FRAME_HEIGHT)
    print("✓ Camera opened")
    
    # Setup video writer if needed
    video_writer = None
    if save_output:
        output_path = Path(__file__).parent / "outputs" / "demo_output.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            20.0,
            (CameraConfig.FRAME_WIDTH, CameraConfig.FRAME_HEIGHT)
        )
        print(f"✓ Video writer created: {output_path}")
    
    # Initialize FPS counter
    fps_counter = FPSCounter()
    
    print()
    print(f"Running demo for {duration_seconds} seconds...")
    print("Press 'q' to quit early")
    print("Press 's' to save screenshot")
    print()
    
    start_time = time.time()
    frame_count = 0
    
    try:
        while True:
            # Check time limit
            elapsed = time.time() - start_time
            if elapsed > duration_seconds:
                break
            
            # Read frame
            ret, frame = camera.read()
            if not ret:
                print("Warning: Failed to read frame")
                continue
            
            # Process frame
            results = pipeline.process_frame(
                frame,
                enable_bottle=True,
                enable_cap=True,
                enable_brand=True
            )
            
            # Draw detections
            annotated_frame = frame.copy()
            
            # Draw bottles (blue)
            for bottle in results.get('bottles', []):
                label = "Bottle"
                if 'brand' in bottle:
                    label = bottle['brand']
                
                draw_bounding_box(
                    annotated_frame,
                    bottle['bbox'],
                    label,
                    bottle['confidence'],
                    UIConfig.COLORS['bottle']
                )
            
            # Draw caps (green/red)
            for cap in results.get('caps', []):
                color = UIConfig.COLORS.get(cap['category'], (128, 128, 128))
                label = cap['cap_status']
                
                draw_bounding_box(
                    annotated_frame,
                    cap['bbox'],
                    label,
                    cap['confidence'],
                    color
                )
            
            # Update FPS
            fps = fps_counter.update()
            
            # Get counts
            counts = pipeline.get_detection_counts(results)
            
            # Draw info
            draw_detection_info(
                annotated_frame,
                fps,
                counts,
                position='top-left'
            )
            
            # Save to video
            if video_writer is not None:
                video_writer.write(annotated_frame)
            
            # Display
            cv2.imshow('Unified Detection Demo', annotated_frame)
            
            # Handle keyboard
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nQuitting early...")
                break
            elif key == ord('s'):
                screenshot_path = Path(__file__).parent / "outputs" / f"demo_screenshot_{int(time.time())}.jpg"
                cv2.imwrite(str(screenshot_path), annotated_frame)
                print(f"Screenshot saved: {screenshot_path}")
            
            frame_count += 1
            
            # Print progress every 30 frames
            if frame_count % 30 == 0:
                print(f"Progress: {elapsed:.1f}s | FPS: {fps:.1f} | Bottles: {counts['bottles']} | Caps: {counts['with_cap']+counts['without_cap']}")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        # Cleanup
        camera.release()
        if video_writer is not None:
            video_writer.release()
        cv2.destroyAllWindows()
        
        print()
        print("="*60)
        print("DEMO SUMMARY")
        print("="*60)
        print(f"Total frames processed: {frame_count}")
        print(f"Average FPS: {fps_counter.get_fps():.1f}")
        print(f"Duration: {elapsed:.1f} seconds")
        
        if save_output:
            print(f"Output saved to: outputs/demo_output.mp4")
        
        print()
        print("✓ Demo completed successfully!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run demo of unified detection system')
    parser.add_argument('--duration', type=int, default=30, help='Demo duration in seconds')
    parser.add_argument('--no-save', action='store_true', help='Do not save output video')
    
    args = parser.parse_args()
    
    run_demo(
        duration_seconds=args.duration,
        save_output=not args.no_save
    )
