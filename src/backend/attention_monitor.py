"""
Attention Monitoring Module
Uses OpenCV for face/eye detection to monitor student attention
"""

import cv2
import time
import logging
import threading
from typing import Dict, Optional, Callable, Tuple
import numpy as np
from dataclasses import dataclass
from collections import deque
import json
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AttentionMetrics:
    """Data class for attention tracking metrics"""
    focus_percentage: float
    eye_contact_duration: float
    face_detection_confidence: float
    total_monitoring_time: float
    attention_alerts: int
    timestamp: float

class AttentionMonitor:
    """Monitors student attention using webcam and OpenCV"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.cache_dir = self.data_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # OpenCV classifiers
        self.face_cascade = None
        self.eye_cascade = None
        self._load_opencv_classifiers()
        
        # Monitoring state
        self.is_monitoring = False
        self.camera = None
        self.monitoring_thread = None
        
        # Attention tracking
        self.attention_history = deque(maxlen=100)  # Last 100 measurements
        self.current_metrics = AttentionMetrics(0, 0, 0, 0, 0, time.time())
        
        # Thresholds
        self.face_detection_threshold = 0.5
        self.eye_detection_threshold = 0.3
        self.attention_alert_threshold = 5.0  # seconds of inactivity
        self.monitoring_fps = 10  # frames per second
        
        # Callbacks
        self.attention_callback: Optional[Callable] = None
        self.alert_callback: Optional[Callable] = None
        
        # Settings
        self.settings = self._load_settings()
    
    def _load_opencv_classifiers(self):
        """Load OpenCV Haar cascade classifiers"""
        try:
            # Try to load pre-trained classifiers
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            
            if self.face_cascade.empty() or self.eye_cascade.empty():
                logger.warning("Could not load OpenCV classifiers")
                self.face_cascade = None
                self.eye_cascade = None
            else:
                logger.info("Successfully loaded OpenCV classifiers")
                
        except Exception as e:
            logger.error(f"Failed to load OpenCV classifiers: {e}")
            self.face_cascade = None
            self.eye_cascade = None
    
    def _load_settings(self) -> Dict:
        """Load attention monitoring settings"""
        settings_path = self.cache_dir / "attention_settings.json"
        default_settings = {
            "webcam_enabled": True,
            "attention_alerts": True,
            "sensitivity": "medium",
            "alert_frequency": 30,  # seconds
            "privacy_mode": False
        }
        
        try:
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults
                    default_settings.update(settings)
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Save attention monitoring settings"""
        try:
            settings_path = self.cache_dir / "attention_settings.json"
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def start_monitoring(self, camera_index: int = 0) -> bool:
        """
        Start attention monitoring
        
        Args:
            camera_index: Camera device index (0 for default)
            
        Returns:
            Success status
        """
        if not self.settings.get("webcam_enabled", True):
            logger.info("Webcam monitoring disabled in settings")
            return False
        
        if self.is_monitoring:
            logger.warning("Monitoring already active")
            return True
        
        try:
            # Initialize camera
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                logger.error("Could not open camera")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, self.monitoring_fps)
            
            # Start monitoring thread
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("Started attention monitoring")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")
            self.stop_monitoring()
            return False
    
    def stop_monitoring(self):
        """Stop attention monitoring"""
        self.is_monitoring = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        logger.info("Stopped attention monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        last_face_time = time.time()
        last_alert_time = 0
        monitoring_start_time = time.time()
        
        while self.is_monitoring:
            try:
                # Capture frame
                ret, frame = self.camera.read()
                if not ret:
                    logger.warning("Failed to capture frame")
                    continue
                
                # Analyze attention
                attention_data = self._analyze_frame(frame)
                current_time = time.time()
                
                # Update metrics
                if attention_data['face_detected']:
                    last_face_time = current_time
                    face_duration = current_time - last_face_time if last_face_time else 0
                else:
                    face_duration = current_time - last_face_time
                
                # Calculate attention percentage
                inactivity_time = current_time - last_face_time
                attention_percentage = max(0, 100 - (inactivity_time * 20))  # Decrease 20% per second
                
                # Update current metrics
                self.current_metrics = AttentionMetrics(
                    focus_percentage=attention_percentage,
                    eye_contact_duration=face_duration,
                    face_detection_confidence=attention_data['confidence'],
                    total_monitoring_time=current_time - monitoring_start_time,
                    attention_alerts=self.current_metrics.attention_alerts,
                    timestamp=current_time
                )
                
                # Add to history
                self.attention_history.append(self.current_metrics)
                
                # Check for attention alerts
                if (inactivity_time > self.attention_alert_threshold and 
                    current_time - last_alert_time > self.settings.get("alert_frequency", 30)):
                    
                    if self.alert_callback:
                        self.alert_callback(inactivity_time)
                    
                    self.current_metrics.attention_alerts += 1
                    last_alert_time = current_time
                    logger.info(f"Attention alert: {inactivity_time:.1f}s inactivity")
                
                # Callback with current attention level
                if self.attention_callback:
                    self.attention_callback(attention_percentage)
                
                # Control loop timing
                time.sleep(1.0 / self.monitoring_fps)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def _analyze_frame(self, frame) -> Dict:
        """
        Analyze frame for attention indicators
        
        Returns:
            Dictionary with analysis results
        """
        result = {
            'face_detected': False,
            'eyes_detected': False,
            'confidence': 0.0,
            'face_count': 0,
            'eye_count': 0
        }
        
        if self.face_cascade is None:
            # Fallback: simple motion detection or random simulation
            return self._simulate_attention_detection()
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            result['face_count'] = len(faces)
            result['face_detected'] = len(faces) > 0
            
            if len(faces) > 0:
                # Calculate confidence based on face size and position
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                face_area = largest_face[2] * largest_face[3]
                frame_area = frame.shape[0] * frame.shape[1]
                
                # Face should be reasonable size (not too small/large)
                size_score = min(1.0, face_area / (frame_area * 0.01))
                size_score = min(size_score, frame_area * 0.1 / face_area)
                
                result['confidence'] = size_score
                
                # Detect eyes within face region
                if self.eye_cascade is not None:
                    x, y, w, h = largest_face
                    roi_gray = gray[y:y+h, x:x+w]
                    
                    eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                    result['eye_count'] = len(eyes)
                    result['eyes_detected'] = len(eyes) >= 2
                    
                    # Boost confidence if eyes detected
                    if result['eyes_detected']:
                        result['confidence'] = min(1.0, result['confidence'] * 1.5)
            
        except Exception as e:
            logger.error(f"Error analyzing frame: {e}")
        
        return result
    
    def _simulate_attention_detection(self) -> Dict:
        """Simulate attention detection when OpenCV not available"""
        import random
        
        # Simulate realistic attention patterns
        base_attention = 0.8
        noise = random.uniform(-0.3, 0.2)
        attention_level = max(0, min(1, base_attention + noise))
        
        return {
            'face_detected': attention_level > 0.3,
            'eyes_detected': attention_level > 0.5,
            'confidence': attention_level,
            'face_count': 1 if attention_level > 0.3 else 0,
            'eye_count': 2 if attention_level > 0.5 else 0
        }
    
    def get_attention_level(self) -> float:
        """
        Get current attention level (0-100)
        
        Returns:
            Attention percentage
        """
        if not self.attention_history:
            return 50.0  # Default neutral attention
        
        # Use weighted average of recent measurements
        recent_metrics = list(self.attention_history)[-10:]  # Last 10 measurements
        weights = np.linspace(0.1, 1.0, len(recent_metrics))  # More weight to recent
        
        weighted_attention = sum(m.focus_percentage * w for m, w in zip(recent_metrics, weights))
        total_weight = sum(weights)
        
        return weighted_attention / total_weight if total_weight > 0 else 50.0
    
    def get_attention_report(self) -> Dict:
        """
        Generate comprehensive attention report
        
        Returns:
            Dictionary with attention analytics
        """
        if not self.attention_history:
            return {
                'average_attention': 0,
                'peak_attention': 0,
                'low_attention_periods': 0,
                'total_alerts': 0,
                'monitoring_duration': 0,
                'recommendation': "No data available"
            }
        
        metrics = list(self.attention_history)
        attentions = [m.focus_percentage for m in metrics]
        
        average_attention = np.mean(attentions)
        peak_attention = np.max(attentions)
        low_periods = sum(1 for a in attentions if a < 50)
        total_alerts = self.current_metrics.attention_alerts
        duration = self.current_metrics.total_monitoring_time
        
        # Generate recommendation
        if average_attention >= 80:
            recommendation = "Excellent focus! Keep up the great work! 🌟"
        elif average_attention >= 60:
            recommendation = "Good attention. Try to minimize distractions. 👍"
        elif average_attention >= 40:
            recommendation = "Fair attention. Take breaks and check your environment. 📚"
        else:
            recommendation = "Low attention detected. Consider shorter study sessions. ⚠️"
        
        return {
            'average_attention': round(average_attention, 1),
            'peak_attention': round(peak_attention, 1),
            'low_attention_periods': low_periods,
            'total_alerts': total_alerts,
            'monitoring_duration': round(duration, 1),
            'recommendation': recommendation,
            'attention_trend': attentions[-20:] if len(attentions) >= 20 else attentions
        }
    
    def set_attention_callback(self, callback: Callable):
        """Set callback for attention level updates"""
        self.attention_callback = callback
    
    def set_alert_callback(self, callback: Callable):
        """Set callback for attention alerts"""
        self.alert_callback = callback
    
    def update_settings(self, **kwargs):
        """Update monitoring settings"""
        self.settings.update(kwargs)
        self.save_settings()
        logger.info(f"Updated settings: {kwargs}")
    
    def is_camera_available(self) -> bool:
        """Check if camera is available"""
        try:
            test_camera = cv2.VideoCapture(0)
            available = test_camera.isOpened()
            test_camera.release()
            return available
        except:
            return False

# Singleton instance for global access
_attention_monitor = None

def get_attention_monitor() -> AttentionMonitor:
    """Get global attention monitor instance"""
    global _attention_monitor
    if _attention_monitor is None:
        _attention_monitor = AttentionMonitor()
    return _attention_monitor

# Test function
def test_attention_monitor():
    """Test the attention monitor"""
    monitor = AttentionMonitor()
    
    # Test camera availability
    camera_available = monitor.is_camera_available()
    print(f"Camera available: {camera_available}")
    
    # Test monitoring (brief test)
    if camera_available:
        print("Starting 10-second attention monitoring test...")
        
        def attention_callback(level):
            print(f"Attention level: {level:.1f}%")
        
        def alert_callback(inactivity_time):
            print(f"ATTENTION ALERT: {inactivity_time:.1f}s inactivity")
        
        monitor.set_attention_callback(attention_callback)
        monitor.set_alert_callback(alert_callback)
        
        if monitor.start_monitoring():
            time.sleep(10)
            monitor.stop_monitoring()
            
            # Get report
            report = monitor.get_attention_report()
            print(f"Attention Report: {report}")
    else:
        print("No camera available, testing simulation mode...")
        # Test simulation
        for i in range(5):
            result = monitor._simulate_attention_detection()
            print(f"Simulated detection {i+1}: {result}")
            time.sleep(1)

if __name__ == "__main__":
    test_attention_monitor()