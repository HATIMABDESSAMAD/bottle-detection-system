"""
Graphical User Interface for Unified Detection System
=====================================================
Modern Tkinter-based GUI with real-time video, controls, and statistics
"""


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

from config import UIConfig, CameraConfig, ProcessingConfig, SCREENSHOTS_DIR, VIDEOS_DIR
from detection_pipeline import UnifiedDetectionPipeline
from utils import (
    FPSCounter, DetectionStatistics, draw_bounding_box,
    draw_detection_info, save_screenshot, create_video_writer
)


class DetectionInterface:
    """Main GUI application for unified detection system"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the detection interface
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(UIConfig.WINDOW_TITLE)
        self.root.geometry(f"{UIConfig.WINDOW_WIDTH}x{UIConfig.WINDOW_HEIGHT}")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize pipeline
        self.pipeline = None
        self.camera = None
        self.is_running = False
        self.is_recording = False
        self.video_writer = None
        
        # Utilities
        self.fps_counter = FPSCounter()
        self.statistics = DetectionStatistics()
        
        # Detection settings
        self.enable_bottle_detection = tk.BooleanVar(value=True)
        self.enable_cap_detection = tk.BooleanVar(value=True)
        self.enable_brand_classification = tk.BooleanVar(value=True)
        
        # Create UI
        self._create_ui()
        
        # Initialize pipeline in background
        self._initialize_pipeline()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Video display
        left_frame = tk.Frame(main_frame, bg='#2b2b2b')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Video canvas
        self.video_label = tk.Label(left_frame, bg='#000000')
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        controls_frame = tk.Frame(left_frame, bg='#2b2b2b')
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_button = tk.Button(
            controls_frame, text="▶ Démarrer Caméra", 
            command=self._toggle_camera,
            bg='#4a9eff', fg='white', font=('Arial', 12, 'bold'),
            padx=20, pady=10, relief=tk.FLAT
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.screenshot_button = tk.Button(
            controls_frame, text="📷 Capture", 
            command=self._take_screenshot,
            bg='#4caf50', fg='white', font=('Arial', 12, 'bold'),
            padx=20, pady=10, relief=tk.FLAT, state=tk.DISABLED
        )
        self.screenshot_button.pack(side=tk.LEFT, padx=5)
        
        self.record_button = tk.Button(
            controls_frame, text="⏺ Enregistrer", 
            command=self._toggle_recording,
            bg='#f44336', fg='white', font=('Arial', 12, 'bold'),
            padx=20, pady=10, relief=tk.FLAT, state=tk.DISABLED
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Right panel - Statistics and settings
        right_frame = tk.Frame(main_frame, bg='#2b2b2b', width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            right_frame, text="Statistiques & Contrôles",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=10)
        
        # Statistics panel
        self._create_statistics_panel(right_frame)
        
        # Detection toggles
        self._create_detection_toggles(right_frame)
        
        # Confidence sliders
        self._create_confidence_sliders(right_frame)
        
        # Status bar
        self.status_label = tk.Label(
            right_frame, text="État: Prêt",
            bg='#2b2b2b', fg='#4a9eff', font=('Arial', 10)
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)
    
    def _create_statistics_panel(self, parent):
        """Create statistics display panel"""
        stats_frame = tk.LabelFrame(
            parent, text="Détections en Temps Réel",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 11, 'bold')
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # FPS
        self.fps_label = tk.Label(
            stats_frame, text="FPS: 0.0",
            bg='#2b2b2b', fg='#4a9eff', font=('Arial', 12, 'bold')
        )
        self.fps_label.pack(pady=5)
        
        # Bottle count
        self.bottle_label = tk.Label(
            stats_frame, text="🍶 Bouteilles: 0",
            bg='#2b2b2b', fg='#00aaff', font=('Arial', 11)
        )
        self.bottle_label.pack(pady=3, anchor=tk.W, padx=20)
        
        # With cap count
        self.with_cap_label = tk.Label(
            stats_frame, text="✅ Avec Bouchon: 0",
            bg='#2b2b2b', fg='#00ff00', font=('Arial', 11)
        )
        self.with_cap_label.pack(pady=3, anchor=tk.W, padx=20)
        
        # Without cap count
        self.without_cap_label = tk.Label(
            stats_frame, text="❌ Sans Bouchon: 0",
            bg='#2b2b2b', fg='#ff0000', font=('Arial', 11)
        )
        self.without_cap_label.pack(pady=3, anchor=tk.W, padx=20)
        
        # Brand display
        self.brand_frame = tk.Frame(stats_frame, bg='#2b2b2b')
        self.brand_frame.pack(fill=tk.BOTH, pady=5)
        
        brand_title = tk.Label(
            self.brand_frame, text="Marques Détectées:",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 10, 'bold')
        )
        brand_title.pack(anchor=tk.W, padx=20)
        
        self.brand_text = tk.Text(
            self.brand_frame, height=4, bg='#1e1e1e', fg='#ffffff',
            font=('Arial', 9), relief=tk.FLAT
        )
        self.brand_text.pack(fill=tk.BOTH, padx=20, pady=5)
        self.brand_text.config(state=tk.DISABLED)
    
    def _create_detection_toggles(self, parent):
        """Create detection enable/disable toggles"""
        toggles_frame = tk.LabelFrame(
            parent, text="Options de Détection",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 11, 'bold')
        )
        toggles_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Checkbutton(
            toggles_frame, text="Détecter Bouteilles",
            variable=self.enable_bottle_detection,
            bg='#2b2b2b', fg='#ffffff', selectcolor='#1e1e1e',
            font=('Arial', 10), activebackground='#2b2b2b'
        ).pack(anchor=tk.W, padx=20, pady=3)
        
        tk.Checkbutton(
            toggles_frame, text="Détecter Bouchons",
            variable=self.enable_cap_detection,
            bg='#2b2b2b', fg='#ffffff', selectcolor='#1e1e1e',
            font=('Arial', 10), activebackground='#2b2b2b'
        ).pack(anchor=tk.W, padx=20, pady=3)
        
        tk.Checkbutton(
            toggles_frame, text="Classifier Marques",
            variable=self.enable_brand_classification,
            bg='#2b2b2b', fg='#ffffff', selectcolor='#1e1e1e',
            font=('Arial', 10), activebackground='#2b2b2b'
        ).pack(anchor=tk.W, padx=20, pady=3)
    
    def _create_confidence_sliders(self, parent):
        """Create confidence threshold sliders"""
        sliders_frame = tk.LabelFrame(
            parent, text="Seuils de Confiance",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 11, 'bold')
        )
        sliders_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Bottle confidence
        tk.Label(
            sliders_frame, text="Bouteilles: 0.5",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 9)
        ).pack(anchor=tk.W, padx=20, pady=(5, 0))
        
        self.bottle_conf_slider = tk.Scale(
            sliders_frame, from_=0.1, to=0.9, resolution=0.05,
            orient=tk.HORIZONTAL, bg='#2b2b2b', fg='#ffffff',
            highlightthickness=0, troughcolor='#1e1e1e'
        )
        self.bottle_conf_slider.set(0.5)
        self.bottle_conf_slider.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        # Cap confidence
        tk.Label(
            sliders_frame, text="Bouchons: 0.6",
            bg='#2b2b2b', fg='#ffffff', font=('Arial', 9)
        ).pack(anchor=tk.W, padx=20)
        
        self.cap_conf_slider = tk.Scale(
            sliders_frame, from_=0.1, to=0.9, resolution=0.05,
            orient=tk.HORIZONTAL, bg='#2b2b2b', fg='#ffffff',
            highlightthickness=0, troughcolor='#1e1e1e'
        )
        self.cap_conf_slider.set(0.6)
        self.cap_conf_slider.pack(fill=tk.X, padx=20, pady=(0, 5))
    
    def _initialize_pipeline(self):
        """Initialize detection pipeline in background"""
        def init_thread():
            try:
                self.status_label.config(text="État: Initialisation des modèles...")
                self.pipeline = UnifiedDetectionPipeline(enable_gpu=ProcessingConfig.ENABLE_GPU)
                self.status_label.config(text="État: Prêt ✓")
            except Exception as e:
                self.status_label.config(text=f"État: Erreur - {str(e)}")
                messagebox.showerror("Erreur", f"Échec d'initialisation:\n{str(e)}")
        
        threading.Thread(target=init_thread, daemon=True).start()
    
    def _toggle_camera(self):
        """Start or stop camera"""
        if not self.is_running:
            self._start_camera()
        else:
            self._stop_camera()
    
    def _start_camera(self):
        """Start camera capture with automatic backend and ID detection"""
        if self.pipeline is None:
            messagebox.showwarning("Attention", "Pipeline non initialisé!")
            return

        # Try multiple backends and camera IDs
        backends = [None, cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2]
        max_id = 3
        found = False
        for backend in backends:
            for cam_id in range(max_id + 1):
                print(f"[DEBUG] Test caméra: ID={cam_id}, backend={backend}")
                if backend is not None:
                    cam = cv2.VideoCapture(cam_id, backend)
                else:
                    cam = cv2.VideoCapture(cam_id)
                cam.set(cv2.CAP_PROP_FRAME_WIDTH, CameraConfig.FRAME_WIDTH)
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraConfig.FRAME_HEIGHT)
                cam.set(cv2.CAP_PROP_FPS, CameraConfig.FPS)
                if cam.isOpened():
                    ret, _ = cam.read()
                    if ret:
                        self.camera = cam
                        CameraConfig.DEVICE_ID = cam_id
                        found = True
                        print(f"[INFO] Caméra trouvée: ID={cam_id}, backend={backend}")
                        break
                    else:
                        print(f"[ERROR] Caméra ID={cam_id} ouverte mais aucun flux (backend={backend})")
                        cam.release()
                else:
                    print(f"[ERROR] Impossible d'ouvrir la caméra ID={cam_id} (backend={backend})")
            if found:
                break

        if not found:
            error_msg = (
                "Aucune caméra fonctionnelle trouvée.\n\n"
                "Essayez de :\n- Vérifier les permissions Windows\n- Fermer les autres applications utilisant la caméra\n- Tester différents ports USB\n- Redémarrer l'ordinateur\n\n"
                "Vous pouvez aussi essayer de lancer :\npython main.py --camera-id 1\npython main.py --camera-id 2\n\n"
                "Si le problème persiste, vérifiez que la caméra n'est pas utilisée par une autre application (Teams, Zoom, etc.) ou que les pilotes sont à jour."
            )
            print("[FATAL] Caméra non trouvée après tous les essais.")
            messagebox.showerror("Erreur caméra", error_msg)
            self.status_label.config(text="État: Caméra introuvable")
            self._stop_camera()
            return

        self.is_running = True
        self.start_button.config(text="⏸ Arrêter Caméra", bg='#ff9800')
        self.screenshot_button.config(state=tk.NORMAL)
        self.record_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"État: Caméra Active (ID {CameraConfig.DEVICE_ID})")

        # Reset statistics
        self.statistics.reset()

        # Start video loop
        self._video_loop()
    
    def _stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        
        if self.is_recording:
            self._stop_recording()
        
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        self.start_button.config(text="▶ Démarrer Caméra", bg='#4a9eff')
        self.screenshot_button.config(state=tk.DISABLED)
        self.record_button.config(state=tk.DISABLED)
        self.status_label.config(text="État: Arrêté")
    
    def _video_loop(self):
        """Main video processing loop"""
        if not self.is_running or self.camera is None:
            return
        
        ret, frame = self.camera.read()
        
        if ret:
            # Update confidence thresholds
            self.pipeline.update_confidence_thresholds(
                bottle_conf=self.bottle_conf_slider.get(),
                cap_conf=self.cap_conf_slider.get()
            )
            
            # Process frame
            results = self.pipeline.process_frame(
                frame,
                enable_bottle=self.enable_bottle_detection.get(),
                enable_cap=self.enable_cap_detection.get(),
                enable_brand=self.enable_brand_classification.get()
            )
            
            # Draw detections
            annotated_frame = self._draw_detections(frame.copy(), results)
            
            # Update statistics
            counts = self.pipeline.get_detection_counts(results)
            brands = self.pipeline.get_detected_brands(results)
            self.statistics.update(
                bottles=counts['bottles'],
                with_cap=counts['with_cap'],
                without_cap=counts['without_cap'],
                brands=brands
            )
            
            # Update FPS
            fps = self.fps_counter.update()
            
            # Draw info overlay
            annotated_frame = draw_detection_info(
                annotated_frame, fps, counts, position='top-left'
            )
            
            # Update UI
            self._update_statistics_display(fps, counts, brands)
            
            # Display frame
            self._display_frame(annotated_frame)
            
            # Save to video if recording
            if self.is_recording and self.video_writer is not None:
                self.video_writer.write(annotated_frame)
        
        # Schedule next frame
        self.root.after(10, self._video_loop)
    
    def _draw_detections(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """Draw all detections on frame"""
        # Draw bottle detections (blue)
        from utils import draw_bounding_box_bottom
        for bottle in results.get('bottles', []):
            # Afficher la marque détectée en bas du box, sinon juste "Bouteille"
            label_top = "Bouteille"
            draw_bounding_box(
                frame, bottle['bbox'], label_top,
                bottle['confidence'], UIConfig.COLORS['bottle']
            )
            if 'brand' in bottle and 'brand_confidence' in bottle:
                label_bottom = f"{bottle['brand']} {bottle['brand_confidence']:.2f}"
                draw_bounding_box_bottom(
                    frame, bottle['bbox'], label_bottom,
                    bottle['confidence'], UIConfig.COLORS['bottle']
                )
        
        # Draw cap detections (vert/rouge/orange)
        for cap in results.get('caps', []):
            if cap['category'] == 'broken_cap':
                continue  # Ne pas afficher le box pour Broken Cap
            color = UIConfig.COLORS.get(cap['category'], (128, 128, 128))
            label = cap['cap_status']
            draw_bounding_box(
                frame, cap['bbox'], label,
                cap['confidence'], color
            )
        return frame
    
    def _display_frame(self, frame: np.ndarray):
        """Display frame in GUI"""
        # Resize for display
        display_frame = cv2.resize(
            frame, 
            (UIConfig.VIDEO_DISPLAY_WIDTH, UIConfig.VIDEO_DISPLAY_HEIGHT)
        )
        
        # Convert to ImageTk
        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
    
    def _update_statistics_display(self, fps: float, counts: Dict, brands: List[str]):
        """Update statistics display in UI"""
        self.fps_label.config(text=f"FPS: {fps:.1f}")
        self.bottle_label.config(text=f"🍶 Bouteilles: {counts['bottles']}")
        self.with_cap_label.config(text=f"✅ Avec Bouchon: {counts['with_cap']}")
        self.without_cap_label.config(text=f"❌ Sans Bouchon: {counts['without_cap']}")
        
        # Update brand list
        self.brand_text.config(state=tk.NORMAL)
        self.brand_text.delete('1.0', tk.END)
        
        if brands:
            brand_str = "\n".join([f"• {brand}" for brand in set(brands)])
            self.brand_text.insert('1.0', brand_str)
        else:
            self.brand_text.insert('1.0', "Aucune marque détectée")
        
        self.brand_text.config(state=tk.DISABLED)
    
    def _take_screenshot(self):
        """Take a screenshot"""
        if self.camera is not None and self.is_running:
            ret, frame = self.camera.read()
            if ret:
                filepath = save_screenshot(frame, SCREENSHOTS_DIR)
                messagebox.showinfo("Succès", f"Screenshot sauvegardé:\n{filepath}")
    
    def _toggle_recording(self):
        """Toggle video recording"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Start video recording"""
        if self.camera is None:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = VIDEOS_DIR / f"recording_{timestamp}.mp4"
        
        self.video_writer = create_video_writer(
            video_path,
            CameraConfig.FPS,
            (CameraConfig.FRAME_WIDTH, CameraConfig.FRAME_HEIGHT),
            CameraConfig.VIDEO_CODEC
        )
        
        self.is_recording = True
        self.record_button.config(text="⏹ Arrêter", bg='#9c27b0')
        self.status_label.config(text="État: 🔴 Enregistrement...")
    
    def _stop_recording(self):
        """Stop video recording"""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        
        self.is_recording = False
        self.record_button.config(text="⏺ Enregistrer", bg='#f44336')
        self.status_label.config(text="État: Caméra Active")
    
    def _on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
            self._stop_camera()
            self.root.destroy()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = DetectionInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
