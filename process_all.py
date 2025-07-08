import os
from main import PlayerReidentificationSystem

def process_all_videos():
    """Process all videos in the data/videos folder"""
    print("Batch Processing All Videos")
    print("=" * 50)
    
    video_dir = 'data/videos/'
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    
    if not video_files:
        print("No video files found!")
        return
    
    print(f"Found {len(video_files)} videos: {video_files}")
    
    model_path = 'data/models/yolov11_player_model.pt'
    system = PlayerReidentificationSystem(model_path)
    
    results = {}
    for i, video_file in enumerate(video_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(video_files)}: {video_file}")
        print(f"{'='*60}")
        
        video_path = os.path.join(video_dir, video_file)
        video_name = video_file.replace('.mp4', '')
        output_path = f'output/{video_name}_result.mp4'
        
        try:
            tracking_data = system.process_video(video_path, output_path)
            results[video_file] = "✅ Success"
            print(f"✅ Completed: {video_file}")
        except Exception as e:
            results[video_file] = f"Error: {str(e)}"
            print(f"Error processing {video_file}: {str(e)}")
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    for video, status in results.items():
        print(f"{video}: {status}")
    
    print(f"\n Batch processing complete!")
    print(f" Check the 'output' folder for results")

if __name__ == "__main__":
    process_all_videos()