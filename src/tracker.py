import numpy as np
from collections import defaultdict

class PlayerTracker:
    def __init__(self, max_disappeared=30, similarity_threshold=0.5):
        self.next_id = 0
        self.players = {}  
        self.disappeared = {}  
        self.max_disappeared = max_disappeared
        self.similarity_threshold = similarity_threshold
        print("✅ Player tracker initialized!")
        
    def register_player(self, features, bbox):
        """Register a new player"""
        player_id = self.next_id
        self.players[player_id] = {
            'features': features,
            'bbox': bbox,
            'track_history': [bbox]
        }
        self.disappeared[player_id] = 0
        self.next_id += 1
        print(f"📝 New player registered: Player {player_id}")
        return player_id
    
    def deregister_player(self, player_id):
        """Remove a player from tracking"""
        if player_id in self.players:
            del self.players[player_id]
            del self.disappeared[player_id]
            print(f"❌ Player {player_id} removed from tracking")
    
    def calculate_similarity(self, features1, features2):
        """Calculate similarity between two feature vectors"""
        # Normalize features
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        features1_norm = features1 / norm1
        features2_norm = features2 / norm2
        
        similarity = np.dot(features1_norm, features2_norm)
        return max(0, similarity)  
    
    def update(self, detections, features_list):
        """Update player tracking with new detections"""
        if len(detections) == 0:
            for player_id in list(self.disappeared.keys()):
                self.disappeared[player_id] += 1
                if self.disappeared[player_id] > self.max_disappeared:
                    self.deregister_player(player_id)
            return {}
        
        if len(self.players) == 0:
            player_assignments = {}
            for i, (detection, features) in enumerate(zip(detections, features_list)):
                player_id = self.register_player(features, detection['bbox'])
                player_assignments[player_id] = detection
            return player_assignments
        
        existing_ids = list(self.players.keys())
        similarity_matrix = np.zeros((len(existing_ids), len(detections)))
        
        for i, player_id in enumerate(existing_ids):
            for j, features in enumerate(features_list):
                similarity = self.calculate_similarity(
                    self.players[player_id]['features'], features
                )
                similarity_matrix[i, j] = similarity
        
        # Find best matches
        player_assignments = {}
        used_detection_indices = set()
        
        # Simple greedy matching
        for i, player_id in enumerate(existing_ids):
            best_match_idx = -1
            best_similarity = -1
            
            for j in range(len(detections)):
                if j in used_detection_indices:
                    continue
                
                if similarity_matrix[i, j] > best_similarity and similarity_matrix[i, j] > self.similarity_threshold:
                    best_similarity = similarity_matrix[i, j]
                    best_match_idx = j
            
            if best_match_idx != -1:
                # Update existing player
                detection = detections[best_match_idx]
                features = features_list[best_match_idx]
                
                # Update player info
                self.players[player_id]['features'] = features
                self.players[player_id]['bbox'] = detection['bbox']
                self.players[player_id]['track_history'].append(detection['bbox'])
                
                # Reset disappeared counter
                self.disappeared[player_id] = 0
                
                player_assignments[player_id] = detection
                used_detection_indices.add(best_match_idx)
            else:
                # Player not found, increment disappeared counter
                self.disappeared[player_id] += 1
        
        # Register new players for unmatched detections
        for j, (detection, features) in enumerate(zip(detections, features_list)):
            if j not in used_detection_indices:
                player_id = self.register_player(features, detection['bbox'])
                player_assignments[player_id] = detection
        
        # Remove players that have been gone too long
        for player_id in list(self.disappeared.keys()):
            if self.disappeared[player_id] > self.max_disappeared:
                self.deregister_player(player_id)
        
        return player_assignments