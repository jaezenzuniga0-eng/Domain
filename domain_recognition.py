"""
Domain Expansion Gesture Recognition System
Real-time hand gesture recognition connected to Jujutsu Kaisen Domain Expansion techniques
"""

import cv2
import numpy as np
from hand_detector import HandDetector
from domain_gestures import (
    DOMAIN_GESTURES,
    GESTURE_REFERENCE,
    get_gesture_info,
    get_gesture_color,
)
import time


class DomainRecognizer:
    """Main application for Domain Expansion gesture recognition"""

    def __init__(self, camera_index=0, fps=30):
        """
        Initialize the Domain Recognizer

        Args:
            camera_index: Webcam index (0 for default)
            fps: Target frames per second
        """
        self.camera_index = camera_index
        self.fps = fps
        self.frame_time = 1.0 / fps

        # Initialize components
        self.detector = HandDetector(max_hands=2)
        self.cap = cv2.VideoCapture(camera_index)

        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        # UI state
        self.show_reference = False
        self.detected_gestures = {}
        self.last_detection_time = 0
        self.detection_cooldown = 0.5  # seconds

    def match_gesture(self, finger_states):
        """
        Match hand gesture to a Domain Expansion technique

        Args:
            finger_states: Dict of finger extension states

        Returns:
            Tuple: (gesture_name, confidence_score)
        """
        best_match = None
        best_score = 0.0

        for gesture_name, gesture_info in DOMAIN_GESTURES.items():
            requirements = gesture_info["finger_requirements"]
            threshold = gesture_info["confidence_threshold"]

            # Count matching fingers
            matches = 0
            total = len(requirements)

            for finger, should_extend in requirements.items():
                if finger_states.get(finger, False) == should_extend:
                    matches += 1

            # Calculate confidence as percentage of matching fingers
            confidence = matches / total

            # Check if this is the best match and meets threshold
            if confidence >= threshold and confidence > best_score:
                best_match = gesture_name
                best_score = confidence

        return best_match, best_score

    def draw_gesture_info(self, img, gesture_name, confidence, hand_index=0):
        """Draw gesture information on frame"""
        if not gesture_name:
            return img

        gesture_info = get_gesture_info(gesture_name)
        color = get_gesture_color(gesture_name)

        h, w, c = img.shape
        y_offset = 100 + (hand_index * 150)

        # Draw semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (20, y_offset - 40), (400, y_offset + 100), color, -1)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

        # Draw text
        cv2.putText(
            img,
            f"Domain: {gesture_name}",
            (30, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color,
            3,
        )
        cv2.putText(
            img,
            f"Confidence: {confidence:.1%}",
            (30, y_offset + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
        )
        cv2.putText(
            img,
            f"Character: {gesture_info['character']}",
            (30, y_offset + 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        return img

    def draw_reference_guide(self, img):
        """Draw gesture reference guide on image"""
        h, w, c = img.shape

        # Draw semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (20, 20), (w - 20, h - 20), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

        # Draw reference text
        reference_lines = GESTURE_REFERENCE.split("\n")
        y_pos = 50

        for line in reference_lines:
            cv2.putText(
                img,
                line,
                (40, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
            )
            y_pos += 25

        return img

    def draw_ui(self, img):
        """Draw UI elements"""
        h, w, c = img.shape

        # Draw FPS
        cv2.putText(
            img,
            "Press 'i' for reference | 's' for screenshot | 'q' to quit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        return img

    def run(self):
        """Main loop - run the application"""
        print("🔮 Domain Expansion Gesture Recognition Started!")
        print("Press 'i' for reference guide")
        print("Press 's' to save screenshot")
        print("Press 'q' to quit\n")

        frame_count = 0
        start_time = time.time()

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)

            # Detect hands
            frame, hands_data = self.detector.find_hands(frame, draw=True)

            # Process each detected hand
            for hand_index, hand_info in enumerate(hands_data):
                finger_states = hand_info["finger_states"]

                # Match gesture
                gesture_name, confidence = self.match_gesture(finger_states)

                # Draw gesture info
                if gesture_name:
                    frame = self.draw_gesture_info(frame, gesture_name, confidence, hand_index)

            # Draw reference guide if needed
            if self.show_reference:
                frame = self.draw_reference_guide(frame)

            # Draw UI
            frame = self.draw_ui(frame)

            # Display frame
            cv2.imshow("🔮 Domain Expansion Recognition", frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("\nQuitting... 👋")
                break
            elif key == ord("i"):
                self.show_reference = not self.show_reference
                print(f"Reference guide {'ON' if self.show_reference else 'OFF'}")
            elif key == ord("s"):
                filename = f"domain_expansion_{frame_count}.png"
                cv2.imwrite(filename, frame)
                print(f"✅ Screenshot saved: {filename}")

            frame_count += 1

        # Calculate and print stats
        elapsed_time = time.time() - start_time
        avg_fps = frame_count / elapsed_time

        print(f"\nStats:")
        print(f"  Total frames: {frame_count}")
        print(f"  Elapsed time: {elapsed_time:.1f}s")
        print(f"  Average FPS: {avg_fps:.1f}")

        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("\nResources cleaned up. See you soon! 🔮")


def main():
    """Main entry point"""
    try:
        recognizer = DomainRecognizer(camera_index=0, fps=30)
        recognizer.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
