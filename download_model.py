import gdown
import os

os.makedirs('data/models', exist_ok=True)

print("Downloading AI model... This may take a few minutes.")
url = "https://drive.google.com/file/d/1-5fOSHOSB9UXyP_enOoZNAMScrePVcMD/view"
output = "data/models/yolov11_player_model.pt"

try:
    gdown.download(url, output, quiet=False, fuzzy=True)
    print("Model downloaded successfully!")
except Exception as e:
    print(f"Error downloading model: {e}")
    print("Please check your internet connection and try again.")