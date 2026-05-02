"""
Mobile-Assisted Domain Expansion Server
Flask web server for remote gesture recognition
"""

from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
import cv2
import threading
import time
from collections import deque
from datetime import datetime
import base64
import io

from hand_detector import HandDetector
from domain_gestures import DOMAIN_GESTURES, get_gesture_info, get_all_gestures


class MobileServer:
    """Flask server for mobile gesture recognition"""

    def __init__(self, camera_index=0, port=5000, debug=False):
        """
        Initialize mobile server

        Args:
            camera_index: Webcam index
            port: Port to run Flask app on
            debug: Debug mode
        """
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        CORS(self.app)

        self.camera_index = camera_index
        self.port = port
        self.debug = debug

        # Initialize detector
        self.detector = HandDetector(max_hands=2)
        self.cap = cv2.VideoCapture(camera_index)

        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # State tracking
        self.current_gestures = {}
        self.detection_history = deque(maxlen=100)  # Keep last 100 detections
        self.frame_lock = threading.Lock()
        self.current_frame = None
        self.server_start_time = datetime.now()

        # Set up routes
        self._setup_routes()

        # Start capture thread
        self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.capture_thread.start()

    def _setup_routes(self):
        """Set up Flask routes"""

        @self.app.route('/')
        def index():
            """Main web interface"""
            return render_template('index.html')

        @self.app.route('/video_feed')
        def video_feed():
            """Stream video with landmarks"""
            return Response(
                self._generate_frames(),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )

        @self.app.route('/api/gestures')
        def get_gestures():
            """Get currently detected gestures"""
            return jsonify(self.current_gestures)

        @self.app.route('/api/gesture-reference')
        def get_reference():
            """Get all available gestures"""
            reference = {}
            for gesture_name in get_all_gestures():
                info = get_gesture_info(gesture_name)
                reference[gesture_name] = {
                    'gesture': info['gesture'],
                    'description': info['description'],
                    'character': info['character'],
                    'power': info['power'],
                }
            return jsonify(reference)

        @self.app.route('/api/history')
        def get_history():
            """Get detection history"""
            return jsonify(list(self.detection_history))

        @self.app.route('/api/stats')
        def get_stats():
            """Get detection statistics"""
            technique_counts = {}
            for detection in self.detection_history:
                technique = detection['technique']
                technique_counts[technique] = technique_counts.get(technique, 0) + 1

            most_detected = max(technique_counts, key=technique_counts.get) if technique_counts else None

            return jsonify({
                'total_detections': len(self.detection_history),
                'technique_counts': technique_counts,
                'most_detected': most_detected,
                'techniques_available': get_all_gestures(),
                'server_uptime': str(datetime.now() - self.server_start_time).split('.')[0],
            })

        @self.app.route('/api/capture', methods=['POST'])
        def capture():
            """Capture current frame"""
            with self.frame_lock:
                if self.current_frame is not None:
                    _, buffer = cv2.imencode('.png', self.current_frame)
                    img_bytes = buffer.tobytes()
                    return Response(img_bytes, mimetype='image/png')
            return Response('No frame available', status=500)

        @self.app.route('/api/clear-history', methods=['POST'])
        def clear_history():
            """Clear detection history"""
            self.detection_history.clear()
            return jsonify({'status': 'cleared'})

        @self.app.route('/health')
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'server_uptime': str(datetime.now() - self.server_start_time).split('.')[0],
                'camera_active': self.cap.isOpened(),
                'detections_count': len(self.detection_history),
            })

    def _capture_frames(self):
        """Capture frames in background thread"""
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to grab frame")
                time.sleep(0.1)
                continue

            # Flip for selfie view
            frame = cv2.flip(frame, 1)

            # Detect hands
            frame_with_landmarks, hands_data = self.detector.find_hands(frame, draw=True)

            # Process detections
            self.current_gestures = {}
            for hand_index, hand_info in enumerate(hands_data):
                gesture_name, confidence = self._match_gesture(hand_info['finger_states'])

                if gesture_name:
                    self.current_gestures[f'hand_{hand_index}'] = {
                        'technique': gesture_name,
                        'confidence': confidence,
                        'character': get_gesture_info(gesture_name)['character'],
                        'handedness': hand_info['handedness'],
                    }

                    # Add to history
                    self.detection_history.append({
                        'technique': gesture_name,
                        'character': get_gesture_info(gesture_name)['character'],
                        'confidence': confidence,
                        'handedness': hand_info['handedness'],
                        'timestamp': datetime.now().isoformat(),
                    })

            # Store current frame
            with self.frame_lock:
                self.current_frame = frame_with_landmarks

            time.sleep(1/30)  # ~30 FPS

    def _match_gesture(self, finger_states):
        """Match gesture to Domain Expansion technique"""
        best_match = None
        best_score = 0.0

        for gesture_name, gesture_info in DOMAIN_GESTURES.items():
            requirements = gesture_info['finger_requirements']
            threshold = gesture_info['confidence_threshold']

            matches = 0
            total = len(requirements)

            for finger, should_extend in requirements.items():
                if finger_states.get(finger, False) == should_extend:
                    matches += 1

            confidence = matches / total

            if confidence >= threshold and confidence > best_score:
                best_match = gesture_name
                best_score = confidence

        return best_match, best_score

    def _generate_frames(self):
        """Generate MJPEG frames for streaming"""
        while True:
            with self.frame_lock:
                if self.current_frame is None:
                    continue

                frame = self.current_frame.copy()

            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Yield frame in MJPEG format
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n'
                b'Content-Length: ' + str(len(frame_bytes)).encode() + b'\r\n\r\n'
                + frame_bytes + b'\r\n'
            )

            time.sleep(1/30)  # ~30 FPS

    def run(self):
        """Start the Flask server"""
        print("\n" + "="*60)
        print("🔮 Domain Expansion Mobile Server Starting...")
        print("="*60)
        print(f"📱 Access the app at: http://localhost:{self.port}")
        print(f"🌐 API endpoints available at: http://localhost:{self.port}/api/*")
        print("\nAccess from other devices on your network:")
        print(f"   http://<YOUR_COMPUTER_IP>:{self.port}")
        print("\nPress Ctrl+C to stop the server")
        print("="*60 + "\n")

        try:
            self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=self.debug,
                threaded=True,
                use_reloader=False
            )
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        self.detector.release()
        print("✅ Server stopped. See you soon! 🔮")


def main():
    """Main entry point"""
    import os

    port = int(os.getenv('PORT', 5000))

    try:
        server = MobileServer(camera_index=0, port=port, debug=False)
        server.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
