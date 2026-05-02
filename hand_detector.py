"""
Hand Detection Module using MediaPipe
Detects hands and analyzes finger extension states for gesture recognition
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Tuple


class HandDetector:
    """Hand detection and tracking using MediaPipe"""

    def __init__(self, max_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        """
        Initialize hand detector

        Args:
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum detection confidence (0.0-1.0)
            tracking_confidence: Minimum tracking confidence (0.0-1.0)
        """
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

        # Hand landmark indices
        self.HAND_LANDMARKS = {
            "wrist": 0,
            "thumb_cmc": 1,
            "thumb_pip": 2,
            "thumb_ip": 3,
            "thumb_tip": 4,
            "index_mcp": 5,
            "index_pip": 6,
            "index_dip": 7,
            "index_tip": 8,
            "middle_mcp": 9,
            "middle_pip": 10,
            "middle_dip": 11,
            "middle_tip": 12,
            "ring_mcp": 13,
            "ring_pip": 14,
            "ring_dip": 15,
            "ring_tip": 16,
            "pinky_mcp": 17,
            "pinky_pip": 18,
            "pinky_dip": 19,
            "pinky_tip": 20,
        }

    def find_hands(self, img, draw=True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Detect hands in image and extract landmark information

        Args:
            img: Input image (numpy array)
            draw: Whether to draw landmarks on image

        Returns:
            Tuple of (image_with_landmarks, hands_data)
            hands_data: List of dicts with hand information and finger states
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        hands_data = []
        h, w, c = img.shape

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness_info in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                # Extract landmarks
                landmarks = []
                for landmark in hand_landmarks.landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    z = landmark.z
                    landmarks.append({"x": x, "y": y, "z": z})

                # Analyze finger states
                finger_states = self._analyze_finger_states(landmarks)

                # Get handedness (Left or Right)
                hand_side = handedness_info.classification[0].label

                hand_info = {
                    "landmarks": landmarks,
                    "finger_states": finger_states,
                    "handedness": hand_side,
                    "confidence": handedness_info.classification[0].score,
                }

                hands_data.append(hand_info)

                # Draw landmarks if requested
                if draw:
                    self._draw_landmarks(img, landmarks, hand_side)

        return img, hands_data

    def _analyze_finger_states(self, landmarks: List[Dict]) -> Dict[str, bool]:
        """
        Analyze which fingers are extended based on landmarks

        Args:
            landmarks: List of 21 hand landmarks

        Returns:
            Dict indicating which fingers are extended
        """
        # Define finger tip and pip indices
        finger_tips = {
            "thumb_tip": 4,
            "index_tip": 8,
            "middle_tip": 12,
            "ring_tip": 16,
            "pinky_tip": 20,
        }

        finger_pips = {
            "thumb_pip": 2,
            "index_pip": 6,
            "middle_pip": 10,
            "ring_pip": 14,
            "pinky_pip": 18,
        }

        # Wrist landmark for reference
        wrist = landmarks[0]

        finger_states = {}

        # Check each finger
        for finger_name in ["thumb", "index", "middle", "ring", "pinky"]:
            tip_idx = finger_tips[f"{finger_name}_tip"]
            pip_idx = finger_pips[f"{finger_name}_pip"]

            tip = landmarks[tip_idx]
            pip = landmarks[pip_idx]

            # Finger is extended if tip is above (lower y value) pip
            # For thumb, check horizontal distance instead
            if finger_name == "thumb":
                is_extended = tip["x"] < pip["x"]  # Thumb extends outward
            else:
                is_extended = tip["y"] < pip["y"]  # Other fingers extend upward

            finger_states[f"{finger_name}_extended"] = is_extended

        return finger_states

    def _draw_landmarks(self, img: np.ndarray, landmarks: List[Dict], hand_side: str):
        """
        Draw hand landmarks and connections on image

        Args:
            img: Image to draw on
            landmarks: List of landmark positions
            hand_side: "Left" or "Right"
        """
        # Draw circles at landmark positions
        for i, landmark in enumerate(landmarks):
            x, y = landmark["x"], landmark["y"]
            cv2.circle(img, (x, y), 4, (0, 255, 0), -1)

            # Draw landmark index for debugging (optional)
            # cv2.putText(img, str(i), (x+5, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0))

        # Draw connections between landmarks
        connections = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),  # Thumb
            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),  # Index
            (0, 9),
            (9, 10),
            (10, 11),
            (11, 12),  # Middle
            (0, 13),
            (13, 14),
            (14, 15),
            (15, 16),  # Ring
            (0, 17),
            (17, 18),
            (18, 19),
            (19, 20),  # Pinky
            (5, 9),
            (9, 13),
            (13, 17),  # Palm connections
        ]

        for connection in connections:
            start_idx, end_idx = connection
            start = landmarks[start_idx]
            end = landmarks[end_idx]
            cv2.line(
                img, (start["x"], start["y"]), (end["x"], end["y"]), (255, 0, 0), 2
            )

    def get_finger_positions(self, landmarks: List[Dict]) -> Dict:
        """
        Get positions of all finger tips

        Args:
            landmarks: List of 21 hand landmarks

        Returns:
            Dict with finger tip positions
        """
        finger_tips = {
            "thumb": landmarks[4],
            "index": landmarks[8],
            "middle": landmarks[12],
            "ring": landmarks[16],
            "pinky": landmarks[20],
        }
        return finger_tips

    def calculate_hand_size(self, landmarks: List[Dict]) -> float:
        """
        Calculate approximate hand size

        Args:
            landmarks: List of 21 hand landmarks

        Returns:
            Hand size (distance from wrist to middle finger tip)
        """
        wrist = landmarks[0]
        middle_tip = landmarks[12]

        distance = np.sqrt((wrist["x"] - middle_tip["x"]) ** 2 + (wrist["y"] - middle_tip["y"]) ** 2)
        return distance

    def is_hand_open(self, landmarks: List[Dict]) -> bool:
        """
        Check if hand is open (most fingers extended)

        Args:
            landmarks: List of 21 hand landmarks

        Returns:
            True if hand appears open, False otherwise
        """
        finger_states = self._analyze_finger_states(landmarks)
        extended_count = sum(1 for is_extended in finger_states.values() if is_extended)
        return extended_count >= 4  # At least 4 fingers extended

    def is_hand_closed(self, landmarks: List[Dict]) -> bool:
        """
        Check if hand is closed (fist)

        Args:
            landmarks: List of 21 hand landmarks

        Returns:
            True if hand appears closed, False otherwise
        """
        finger_states = self._analyze_finger_states(landmarks)
        extended_count = sum(1 for is_extended in finger_states.values() if is_extended)
        return extended_count <= 1  # Less than 2 fingers extended

    def release(self):
        """Release resources"""
        self.hands.close()
