import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self):
        print("✅ Feature extractor initialized!")
    
    def extract_color_features(self, frame, bbox):
        """Extract color features from player region"""
        x1, y1, x2, y2 = bbox
        
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
        
        player_region = frame[y1:y2, x1:x2]
        
        if player_region.size == 0:
            return np.zeros(24)  
        
        try:
            player_region = cv2.resize(player_region, (64, 128))
        except:
            return np.zeros(24)
        
        # Convert to HSV color space (better for color analysis)
        hsv = cv2.cvtColor(player_region, cv2.COLOR_BGR2HSV)
        
        # Calculate color histograms
        hist_h = cv2.calcHist([hsv], [0], None, [8], [0, 180])  # Hue
        hist_s = cv2.calcHist([hsv], [1], None, [8], [0, 256])  # Saturation
        hist_v = cv2.calcHist([hsv], [2], None, [8], [0, 256])  # Value
        
        # Normalize histograms
        hist_h = hist_h.flatten() / (hist_h.sum() + 1e-7)
        hist_s = hist_s.flatten() / (hist_s.sum() + 1e-7)
        hist_v = hist_v.flatten() / (hist_v.sum() + 1e-7)
        
        return np.concatenate([hist_h, hist_s, hist_v])
    
    def extract_shape_features(self, bbox):
        """Extract shape features (height, width, aspect ratio)"""
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / (height + 1e-7)
        area = width * height
        
        return np.array([width, height, aspect_ratio, area])
    
    def extract_position_features(self, bbox, frame_shape):
        """Extract position features (relative to frame)"""
        x1, y1, x2, y2 = bbox
        frame_h, frame_w = frame_shape[:2]
        
        center_x = (x1 + x2) / 2 / frame_w
        center_y = (y1 + y2) / 2 / frame_h
        
        return np.array([center_x, center_y])
    
    def extract_all_features(self, frame, bbox):
        """Extract all features for a player"""
        color_features = self.extract_color_features(frame, bbox)
        shape_features = self.extract_shape_features(bbox)
        position_features = self.extract_position_features(bbox, frame.shape)
        
        # Combine all features into one vector
        all_features = np.concatenate([
            color_features,
            shape_features,
            position_features
        ])
        
        return all_features