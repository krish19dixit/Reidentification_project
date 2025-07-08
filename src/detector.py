import cv2
import numpy as np
from ultralytics import YOLO

class PlayerDetector:
    def __init__(self, model_path):
        """Initialize the player detector with YOLOv11 model"""
        print(f"Loading AI model from: {model_path}")
        self.model = YOLO(model_path)
        self.confidence_threshold = 0.5
        print("✅ AI model loaded successfully!")
    
    def detect_players(self, frame):
        """Detect players in a single frame"""
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    if confidence > self.confidence_threshold:
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(confidence),
                            'class_id': class_id
                        })
        
        return detections
    
    def visualize_detections(self, frame, detections):
        """Draw bounding boxes on frame"""
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            text = f"Player: {confidence:.2f}"
            cv2.putText(frame, text, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame