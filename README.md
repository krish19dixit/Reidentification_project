# ⚽ Soccer Player Re-identification System

> An intelligent computer vision system that automatically identifies, tracks, and re-identifies soccer players across video frames, maintaining consistent player IDs even when players temporarily leave the field of view.

## 🎯 What This System Does

- **🔍 Detects Players**: Automatically finds soccer players in video frames using YOLOv11
- **🏃 Tracks Movement**: Follows players as they move across the field
- **🔄 Re-identifies Players**: Recognizes the same player when they return to view
- **📹 Processes Videos**: Handles multiple video files with batch processing
- **📊 Generates Results**: Creates annotated videos with player IDs and tracking data

## 🌟 Features

- ✅ **Automatic Player Detection** with configurable confidence thresholds
- ✅ **Robust Re-identification** using deep learning features
- ✅ **Batch Processing** for multiple video files
- ✅ **Interactive Menu System** for easy video selection
- ✅ **Progress Tracking** with real-time processing updates
- ✅ **Flexible Output** with annotated videos and JSON metadata
- ✅ **Error Handling** with graceful failure recovery

## The Result output 
- https://drive.google.com/drive/folders/1KqF9XOy9P_WUYvAeVmaibPbjNz0-N1u1

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended)
- OpenCV compatible system
- Internet connection for initial model download

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd player-reidentification
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the detection model**
   ```bash
   python3 download_model.py
   ```

### Usage

1. **Place your video files** in the `data/videos/` folder
   ```
   data/videos/
   ├── your_match_1.mp4
   ├── your_match_2.mp4
   └── your_match_3.mp4
   ```

2. **Run the system**
   ```bash
   python3 main.py
   ```

3. **Choose processing option**:
   - **Option 1**: Process all videos automatically
   - **Option 2**: Select specific video to process
   - **Option 3**: Interactive processing with confirmations

4. **Find results** in the `output/` folder
   ```
   output/
   ├── your_match_1_result.mp4
   ├── your_match_2_result.mp4
   ├── your_match_3_result.mp4
   └── tracking_data.json
   ```

## 📁 Project Structure

```
player-reidentification/
├── src/                          # Source code modules
│   ├── __init__.py              # Package initialization
│   ├── detector.py              # Player detection using YOLOv11
│   ├── feature_extractor.py     # Feature extraction for re-identification
│   └── tracker.py               # Player tracking and ID management
├── data/                        # Data directory
│   ├── models/                  # Pre-trained models
│   │   └── yolov11_player_model.pt
│   └── videos/                  # Input video files
│       ├── bodcast3.mp4
│       ├── broadcast1.mp4
│       └── broadcast2.mp4
├── output/                      # Generated results
│   ├── processed_videos/        # Annotated output videos
│   └── tracking_data.json       # Tracking metadata
├── tests/                       # Test files
├── main.py                      # Main application entry point
├── download_model.py            # Model download utility
├── process_all.py               # Batch processing script
├── requirements.txt             # Python dependencies
├── PRD.md                       # Product Requirements Document
└── README.md                    # This file
```

## 🔧 Configuration

### System Parameters

You can modify these parameters in `main.py` or create a `config.py` file:

```python
# Detection settings
CONFIDENCE_THRESHOLD = 0.5      # Minimum confidence for player detection
MODEL_PATH = 'data/models/yolov11_player_model.pt'

# Tracking settings
MAX_DISAPPEARED_FRAMES = 30     # Frames before considering player lost
SIMILARITY_THRESHOLD = 0.5      # Threshold for feature matching

# Processing settings
OUTPUT_DIR = 'output/'          # Directory for results
BATCH_SIZE = 1                  # Number of videos to process simultaneously
```

### Video Requirements

- **Supported formats**: MP4, AVI, MOV
- **Recommended resolution**: 720p or higher
- **Frame rate**: 24-60 FPS
- **Content**: Clear soccer footage with visible players

## 📊 System Components

### 1. Player Detector (`src/detector.py`)
- Uses YOLOv11 for accurate player detection
- Configurable confidence thresholds
- Handles multiple players per frame
- Optimized for soccer field environments

### 2. Feature Extractor (`src/feature_extractor.py`)
- Extracts unique visual features from detected players
- Uses deep learning for robust identification
- Handles varying poses and orientations
- Normalized features for consistent comparison

### 3. Player Tracker (`src/tracker.py`)
- Assigns and maintains unique player IDs
- Tracks players across frames
- Re-identifies players after temporary absence
- Handles occlusions and partial visibility

## 🎮 Usage Examples

### Example 1: Process Single Video
```bash
python3 main.py
# Select option 2, then choose your video
```

### Example 2: Batch Process All Videos
```bash
python3 main.py
# Select option 1 to process all videos
```

### Example 3: Using the Alternative Batch Script
```bash
python3 process_all.py
# Automatically processes all videos in data/videos/
```

## 📈 Performance Expectations

| Video Resolution | Processing Speed | Memory Usage |
|------------------|------------------|--------------|
| 720p             | ~5 FPS          | 4-6 GB       |
| 1080p            | ~3 FPS          | 6-8 GB       |
| 4K               | ~1 FPS          | 8-12 GB      |

*Performance varies based on hardware capabilities and video complexity*

## 🛠️ Troubleshooting

### Common Issues

**1. "Video file not found" Error**
```bash
# Check if video is in correct location
ls data/videos/
# Ensure file has supported extension (.mp4, .avi, .mov)
```

**2. "Model not found" Error**
```bash
# Download the model
python3 download_model.py
# Check if model file exists
ls data/models/
```

**3. Out of Memory Error**
```bash
# Reduce video resolution or
# Process videos one at a time
# Close other applications to free memory
```

**4. Slow Processing**
```bash
# Check if GPU is available
python3 -c "import torch; print(torch.cuda.is_available())"
# Reduce confidence threshold for faster processing
# Use lower resolution videos
```

### Getting Help

1. **Check the logs**: Look for error messages in the console output
2. **Verify file formats**: Ensure videos are in supported formats
3. **Monitor resources**: Check available RAM and disk space
4. **Test with smaller videos**: Start with shorter clips to verify setup

## 🔄 Development & Testing

### Running Tests
```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_detector.py

# Run with coverage
python3 -m pytest tests/ --cov=src/
```

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**
3. **Implement your changes**
4. **Add tests for new functionality**
5. **Update documentation**
6. **Submit a pull request**

## 📋 Dependencies

### Core Dependencies
- `torch>=1.9.0` - Deep learning framework
- `torchvision>=0.10.0` - Computer vision models
- `opencv-python>=4.5.0` - Video processing
- `numpy>=1.21.0` - Numerical computations
- `scikit-learn>=1.0.0` - Machine learning utilities

### Additional Dependencies
- `matplotlib>=3.3.0` - Visualization
- `Pillow>=8.0.0` - Image processing
- `tqdm>=4.62.0` - Progress bars
- `tensorboard>=2.7.0` - Training visualization
- `albumentations>=1.1.0` - Data augmentation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Report bugs** by opening an issue
2. **Suggest features** through feature requests
3. **Submit pull requests** for bug fixes or new features
4. **Improve documentation** and examples
5. **Share your results** and use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **YOLOv11**: For providing excellent object detection capabilities
- **PyTorch**: For the deep learning framework
- **OpenCV**: For video processing utilities
- **Contributors**: Thanks to all who helped improve this system

## 📞 Support

- **Issues**: Report bugs and request features on GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Documentation**: Check the [PRD.md](PRD.md) for detailed requirements
- **Email**: Contact the maintainers for urgent issues

---

**Made with ❤️ for the soccer analytics community**

*Last updated: July 8, 2025*
