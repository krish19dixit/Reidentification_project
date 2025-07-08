import cv2
import numpy as np
import json
import os
from src.detector import PlayerDetector
from src.feature_extractor import FeatureExtractor
from src.tracker import PlayerTracker

class PlayerReidentificationSystem:
    def __init__(self, model_path):
        print("Starting Player Re-identification System...")
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f" Model file not found: {model_path}")
            print("Please run: python3 download_model.py")
            return
        
        self.detector = PlayerDetector(model_path)
        self.feature_extractor = FeatureExtractor()
        self.tracker = PlayerTracker()
        
        # Colors for different players (up to 10 different colors)
        self.colors = [
            (255, 0, 0),    
            (0, 255, 0),    
            (0, 0, 255),    
            (255, 255, 0),  
            (255, 0, 255),  
            (0, 255, 255),  
            (128, 0, 128),  
            (255, 165, 0),  
            (0, 128, 128),  
            (128, 128, 0)   
        ]
        
        print("✅ System initialized successfully!")
    
    def process_video(self, video_path, output_path=None):
        """Process video for player re-identification"""
        print(f"📹 Processing video: {video_path}")
        
        # Check if video exists
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        
        # Check if video opened successfully
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Video info: {width}x{height}, {fps} FPS, {total_frames} frames")
        
        # Initialize video writer if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"💾 Will save result to: {output_path}")
        
        # Initialize tracking data
        tracking_data = []
        frame_count = 0
        
        print("Starting video processing...")
        print("Press 'q' to quit early, 's' to skip to next frame")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = self.detector.detect_players(frame)
            
            features_list = []
            for detection in detections:
                features = self.feature_extractor.extract_all_features(
                    frame, detection['bbox']
                )
                features_list.append(features)
            
            player_assignments = self.tracker.update(detections, features_list)
            
            # Draw results on frame
            result_frame = self.draw_results(frame, player_assignments)
            
            # Save tracking data
            frame_data = {
                'frame_id': frame_count,
                'timestamp': frame_count / fps,
                'players': {}
            }
            
            for player_id, detection in player_assignments.items():
                frame_data['players'][str(player_id)] = {
                    'bbox': detection['bbox'],
                    'confidence': detection['confidence']
                }
            
            tracking_data.append(frame_data)
            
            # Write frame if output specified
            if output_path:
                out.write(result_frame)
            
            # Display frame
            cv2.imshow('Player Re-identification (Press Q to quit)', result_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Stopped by user")
                break
            elif key == ord('s'):
                continue
            
            frame_count += 1
            
            # Print progress every 30 frames
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {frame_count}/{total_frames} frames ({progress:.1f}%)")
        
        # Cleanup
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        # Save tracking data
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        tracking_file = os.path.join(output_dir, 'tracking_data.json')
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)
        
        print(f"Processing complete!")
        print(f"Processed {frame_count} frames")
        print(f"Tracking data saved to: {tracking_file}")
        
        if output_path:
            print(f"🎥 Result video saved to: {output_path}")
        
        return tracking_data
    
    def draw_results(self, frame, player_assignments):
        """Draw tracking results on frame"""
        for player_id, detection in player_assignments.items():
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']

            color = self.colors[player_id % len(self.colors)]
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            
            cv2.rectangle(frame, (x1, y1-30), (x1+150, y1), color, -1)
            
            text = f"Player {player_id}: {confidence:.2f}"
            cv2.putText(frame, text, (x1+5, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        frame_info = f"Players detected: {len(player_assignments)}"
        cv2.putText(frame, frame_info, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame

def main():
    print("Player Re-identification System")
    print("=" * 50)
    
    # List available video files
    video_dir = 'data/videos/'
    if os.path.exists(video_dir):
        available_videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        print(f"📁 Available videos: {available_videos}")
    
    # Check if video file exists 
    video_path = 'data/videos/bodcast3.mp4'
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        
        # Try other video files
        for video_file in ['broadcast1.mp4', 'broadcast2.mp4']:
            alt_path = f'data/videos/{video_file}'
            if os.path.exists(alt_path):
                video_path = alt_path
                print(f" Using alternative video: {video_path}")
                break
        else:
            print(" No video files found in data/videos/ folder")
            print("Please place your video file in the data/videos/ folder")
            return
    
    # Initialize system
    model_path = 'data/models/yolov11_player_model.pt'
    system = PlayerReidentificationSystem(model_path)
    
    # Check if system initialized properly
    if not hasattr(system, 'detector'):
        print(" System initialization failed")
        return
    
    # Process video
    video_name = os.path.basename(video_path).replace('.mp4', '')
    output_path = f'output/{video_name}_result.mp4'
    tracking_data = system.process_video(video_path, output_path)
    
    print("\n Player re-identification complete!")
    print(" Check the 'output' folder for results")

if __name__ == "__main__":
    main()