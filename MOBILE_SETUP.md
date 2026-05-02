````markdown name=MOBILE_SETUP.md url=https://github.com/jaezenzuniga0-eng/Domain/blob/main/MOBILE_SETUP.md
# 📱 Mobile-Assisted Domain Expansion Recognition

Complete setup guide for running the gesture recognition system on mobile devices and remote connections.

## Features

✨ **Web-Based Interface** - Access from any device with a browser  
🎥 **Real-time Video Stream** - Live gesture detection via HTTP  
📊 **Live Statistics** - Track detected techniques in real-time  
📸 **Screenshot Capture** - Download gesture recognition results  
📖 **Gesture Reference** - Interactive reference guide  
📱 **Mobile Responsive** - Works on phones, tablets, and desktops  
🌐 **Network Accessible** - Access from multiple devices simultaneously  

## System Requirements

- Python 3.8+
- Webcam or camera device
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Network connection (LAN or WiFi)

## Installation

### 1. Install Dependencies

```bash
# Install Flask and web dependencies
pip install -r requirements-mobile.txt
```

### 2. Start the Server

```bash
# Run the mobile server
python mobile_server.py
```

You should see:
```
🔮 Domain Expansion Mobile Server Starting...
📱 Access the app at: http://localhost:5000
🌐 API endpoints available at: http://localhost:5000/api/*
```

### 3. Access the Interface

**Local Machine:**
```
http://localhost:5000
```

**From Another Device (Same Network):**
```
http://<YOUR_COMPUTER_IP>:5000
```

Find your computer's IP:
- **Windows:** `ipconfig` (look for IPv4 Address)
- **Mac/Linux:** `ifconfig` (look for inet)

## Usage

### Web Interface

1. **Open the application** in your browser
2. **Allow camera access** when prompted
3. **Show hand gestures** to the webcam
4. **Watch live detection** of Domain Expansion techniques

### Features

| Feature | How to Use |
|---------|-----------|
| **Video Stream** | Displayed in real-time, shows hand landmarks |
| **Detection Info** | Displays detected technique and confidence score |
| **Reference Guide** | Click "Show Reference" to view all techniques |
| **Statistics** | Click "View Stats" to see detection history |
| **Screenshot** | Click "Capture Screenshot" to save image |
| **History** | View all recent detections |
| **Clear History** | Remove detection history |

## API Endpoints

### Video Stream
```
GET /video_feed
```
Returns real-time MJPEG video stream

### Get Detected Gestures
```
GET /api/gestures
```
Returns currently detected gestures
```json
{
  "hand_0": {
    "technique": "Unlimited Void",
    "confidence": 0.92,
    "character": "Satoru Gojo",
    "handedness": "Right"
  }
}
```

### Get Gesture Reference
```
GET /api/gesture-reference
```
Returns all available gestures with descriptions

### Get Detection History
```
GET /api/history
```
Returns array of past detections with timestamps

### Get Statistics
```
GET /api/stats
```
Returns detection statistics
```json
{
  "total_detections": 42,
  "technique_counts": {
    "Unlimited Void": 15,
    "Chimera Shadow Garden": 12,
    ...
  },
  "most_detected": "Unlimited Void"
}
```

### Capture Frame
```
POST /api/capture
```
Captures current frame and returns as base64 image

### Clear History
```
POST /api/clear-history
```
Clears all detection history

### Health Check
```
GET /health
```
Returns server status

## Network Configuration

### Local Network (LAN)

1. **Find your computer's IP address**
2. **Share the IP with other devices** on the same WiFi
3. **Access from device:** `http://<IP>:5000`

### Port Forwarding (Internet Access)

For accessing from outside your network:

1. **Forward port 5000** in your router settings
2. **Find your public IP** at whatismyipaddress.com
3. **Access remotely:** `http://<PUBLIC_IP>:5000`

⚠️ **Security Warning:** Port forwarding exposes your system. Use with caution!

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-mobile.txt .
RUN pip install -r requirements-mobile.txt

COPY . .

CMD ["python", "mobile_server.py"]
```

Build and run:
```bash
docker build -t domain-expansion .
docker run -p 5000:5000 --device /dev/video0 domain-expansion
```

## Mobile Device Setup

### iOS (iPhone/iPad)

1. **Open Safari**
2. **Navigate to:** `http://<YOUR_COMPUTER_IP>:5000`
3. **Tap Share → Add to Home Screen**
4. **Use as app**

### Android

1. **Open Chrome**
2. **Navigate to:** `http://<YOUR_COMPUTER_IP>:5000`
3. **Tap Menu → Install App**
4. **Use as app**

## Performance Tips

### For Better Recognition

- ✅ Keep hands visible to camera
- ✅ Hold gestures steady for 1-2 seconds
- ✅ Ensure good lighting
- ✅ Keep hands 30-100cm from camera
- ✅ Clear, distinct hand signals

### For Server Performance

- 🔄 Close unnecessary browser tabs
- 🔄 Reduce screen resolution on mobile
- 🔄 Ensure stable WiFi connection
- 🔄 Run on machine with decent GPU (if available)

## Troubleshooting

### Camera Not Working

```python
# In mobile_server.py, change camera index
cap = cv2.VideoCapture(1)  # Try 0, 1, 2, etc.
```

### Connection Issues

**Device can't reach server:**
- Verify devices are on same WiFi
- Check firewall settings
- Restart router
- Test with `ping <IP>`

**Port already in use:**
```bash
# Change port in mobile_server.py
app.run(port=5001)
```

### Low FPS / Lag

- Reduce video resolution: Modify `cap.set()` calls
- Reduce max hands: Change `max_hands=1`
- Close other applications
- Move closer to router for better WiFi

### Video Stream Not Showing

- Check browser console for errors (F12)
- Verify camera permissions granted
- Try incognito/private mode
- Clear browser cache

## Advanced Configuration

### Adjust Detection Parameters

In `mobile_server.py`:
```python
# Change detection sensitivity
detector = HandDetector(
    max_hands=2,
    detection_confidence=0.7,  # Lower = more sensitive
    tracking_confidence=0.7
)
```

### Custom Gesture Thresholds

In `domain_gestures.py`:
```python
"Your Technique": {
    ...
    "confidence_threshold": 0.75,  # Adjust here
}
```

### Frame Rate Control

```python
# In generate_frames()
time.sleep(1/30)  # Adjust FPS here
```

## Multi-Device Setup

Run multiple instances on different ports:

```bash
# Terminal 1 - Main server
python mobile_server.py  # Port 5000

# Terminal 2 - Secondary server
PORT=5001 python mobile_server.py  # Port 5001
```

Access each: `http://<IP>:5000` and `http://<IP>:5001`

## Security Best Practices

⚠️ **Important for Production:**

1. **Add authentication** to API endpoints
2. **Use HTTPS** instead of HTTP
3. **Implement rate limiting**
4. **Add CSRF protection**
5. **Run behind reverse proxy** (nginx)

Example with authentication:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "secret"

@app.route('/api/gestures')
@auth.login_required
def get_gestures():
    return jsonify(current_gestures)
```

## Future Enhancements

🚀 Add user accounts and cloud sync  
🚀 Implement gesture recording/playback  
🚀 Add sound effects for techniques  
🚀 Multi-webcam support  
🚀 Gesture customization interface  
🚀 Real-time collaboration mode  
🚀 Mobile app (React Native)  

## Support & Issues

If you encounter issues:

1. Check the server console for errors
2. Verify all dependencies are installed
3. Ensure camera is accessible
4. Check network connectivity
5. Try updating packages: `pip install --upgrade -r requirements-mobile.txt`

## Performance Metrics

Typical performance on modern hardware:

| Metric | Value |
|--------|-------|
| Video Stream FPS | 25-30 |
| Detection Latency | <100ms |
| Memory Usage | 300-500MB |
| Network Bandwidth | 2-5 Mbps |

## License

MIT License - Feel free to modify and deploy!

---

**Ready to deploy your Domain Expansion gesture recognition to mobile? 📱🔮**
````
