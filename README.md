````markdown name=README.md url=https://github.com/jaezenzuniga0-eng/Domain/blob/main/README.md
# 🔮 Domain Expansion Hand Gesture Recognition

A real-time hand gesture recognition system that detects Jujutsu Kaisen Domain Expansion techniques from webcam input using MediaPipe and OpenCV.

## Features

✨ **Real-time Hand Detection** - Detects hands and 21 landmark points using MediaPipe  
🎯 **6 Domain Expansion Gestures** - Recognizes different hand signs mapped to JJK techniques  
📊 **Confidence Scoring** - Shows detection confidence for each gesture  
🎥 **Live Webcam Feed** - Process video stream at ~30 FPS  
📸 **Screenshot Capture** - Save frames with detected gestures  
📖 **Reference Guide** - Built-in gesture reference display  

## Domain Expansion Techniques

| Gesture | Description | Technique |
|---------|-------------|-----------|
| 🌀 Open Palm | All fingers extended | **Unlimited Void** (Gojo) |
| ✌️ Peace Sign | Index & middle finger up | **Chimera Shadow Garden** (Yuji) |
| 👍 Thumbs Up | Thumb extended only | **Malevolent Shrine** (Sukuna) |
| ✊ Closed Fist | All fingers closed | **Idle Death Gamble** (Gojo) |
| 🤘 Rocker Sign | Index & pinky extended | **Evolving Womb** (Mahito) |
| ☝️ Point | Index finger only | **Cursed Speech Technique** (Yuji) |

## Installation

### Prerequisites
- Python 3.8+
- Webcam
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/jaezenzuniga0-eng/Domain.git
cd Domain

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
python domain_recognition.py
```

### Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `i` | Show/hide gesture reference guide |
| `s` | Save screenshot of current frame |

### Example

1. Start the program
2. Show your hands to the webcam
3. Make a gesture (e.g., open your palm)
4. Watch the detected technique appear on screen with confidence score

## Project Structure

```
Domain/
├── requirements.txt          # Project dependencies
├── domain_recognition.py     # Main application (run this)
├── hand_detector.py          # Hand detection module
├── domain_gestures.py        # Gesture definitions
└── README.md                 # This file
```

## How It Works

### 1. Hand Detection (`hand_detector.py`)
- Uses MediaPipe to detect hands in video frames
- Extracts 21 landmark points for each hand
- Tracks finger positions and orientations

### 2. Gesture Recognition
- Analyzes which fingers are extended/closed
- Matches current hand state to gesture requirements
- Calculates confidence score based on match accuracy

### 3. Domain Mapping (`domain_gestures.py`)
- Defines 6 Domain Expansion techniques
- Each gesture has specific finger requirements
- Color-coded UI for visual feedback

## Customization

### Add New Gestures

Edit `domain_gestures.py`:

```python
DOMAIN_GESTURES = {
    "Your Technique Name": {
        "gesture": "gesture_type",
        "description": "Description of the hand sign",
        "finger_requirements": {
            "thumb_extended": True/False,
            "index_extended": True/False,
            "middle_extended": True/False,
            "ring_extended": True/False,
            "pinky_extended": True/False,
        },
        "color": (B, G, R),  # OpenCV color format
        "confidence_threshold": 0.75,  # 0.0 to 1.0
    },
}
```

### Adjust Detection Sensitivity

In `hand_detector.py`, modify the `HandDetector` initialization:

```python
self.hands = self.mp_hands.Hands(
    min_detection_confidence=0.7,  # Lower = more sensitive
    max_num_hands=2,               # Max hands to detect
)
```

## Tips for Better Recognition

- 🎥 **Lighting**: Ensure good lighting on your hands
- 📏 **Distance**: Keep hands 30-100cm from camera
- ✋ **Clarity**: Make distinct, clear hand gestures
- 🔄 **Consistency**: Hold gestures steady for 1-2 seconds
- 🎯 **Angle**: Show full hand to camera, avoid extreme angles

## Performance

- **FPS**: ~25-30 FPS on most modern computers
- **Latency**: <100ms gesture detection
- **Memory**: ~200-300MB RAM usage
- **GPU**: Optional (runs on CPU)

## Dependencies

- **opencv-python**: Video capture and rendering
- **mediapipe**: Hand pose detection
- **numpy**: Numerical computations

## Troubleshooting

### Camera Not Detected
```python
# Try different camera index in domain_recognition.py
recognizer = DomainRecognizer(camera_index=1)  # Change 0 to 1, 2, etc.
```

### Low Detection Accuracy
- Ensure good lighting
- Move closer to camera
- Check that hands are clearly visible
- Increase `confidence_threshold` in gesture definitions

### High CPU Usage
- Reduce resolution: `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)`
- Reduce max hands: `max_num_hands=1`

## Future Enhancements

🚀 Add more Domain Expansion techniques  
🚀 Add multi-hand gesture combinations  
🚀 Implement gesture recording and playback  
🚀 Add sound effects for techniques  
🚀 GPU acceleration with CUDA  
🚀 Mobile app integration  

## References

- [MediaPipe Hand Pose](https://mediapipe.dev/solutions/hands)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Jujutsu Kaisen Techniques](https://jujutsu-kaisen.fandom.com/)

## License

MIT License - Feel free to use and modify!

## Author

Created by **jaezenzuniga0-eng**

---

**Ready to activate your Domain Expansion? 🔮✨**
````
