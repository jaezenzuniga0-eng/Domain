"""
Domain Expansion Gesture Definitions
Maps hand gestures to Jujutsu Kaisen Domain Expansion techniques
"""

# Define all 6 Domain Expansion techniques and their hand sign requirements
DOMAIN_GESTURES = {
    "Unlimited Void": {
        "gesture": "open_palm",
        "description": "All fingers extended",
        "character": "Satoru Gojo",
        "power": "Infinite space creates a domain of nothing",
        "finger_requirements": {
            "thumb_extended": True,
            "index_extended": True,
            "middle_extended": True,
            "ring_extended": True,
            "pinky_extended": True,
        },
        "color": (255, 0, 255),  # Magenta in BGR
        "confidence_threshold": 0.80,
    },
    "Chimera Shadow Garden": {
        "gesture": "peace_sign",
        "description": "Index and middle extended, others closed",
        "character": "Yuji Itadori",
        "power": "Creates shadows to confuse and shadow box enemies",
        "finger_requirements": {
            "thumb_extended": False,
            "index_extended": True,
            "middle_extended": True,
            "ring_extended": False,
            "pinky_extended": False,
        },
        "color": (0, 255, 0),  # Green in BGR
        "confidence_threshold": 0.80,
    },
    "Malevolent Shrine": {
        "gesture": "thumbs_up",
        "description": "Only thumb extended",
        "character": "Ryomen Sukuna",
        "power": "Domain that cuts anything within its range",
        "finger_requirements": {
            "thumb_extended": True,
            "index_extended": False,
            "middle_extended": False,
            "ring_extended": False,
            "pinky_extended": False,
        },
        "color": (0, 0, 255),  # Red in BGR
        "confidence_threshold": 0.80,
    },
    "Idle Death Gamble": {
        "gesture": "closed_fist",
        "description": "All fingers closed",
        "character": "Satoru Gojo",
        "power": "A gamble domain dependent on probability",
        "finger_requirements": {
            "thumb_extended": False,
            "index_extended": False,
            "middle_extended": False,
            "ring_extended": False,
            "pinky_extended": False,
        },
        "color": (0, 165, 255),  # Orange in BGR
        "confidence_threshold": 0.75,
    },
    "Evolving Womb": {
        "gesture": "rocker_sign",
        "description": "Index and pinky extended, others closed",
        "character": "Mahito",
        "power": "Creates transfigured monsters within the domain",
        "finger_requirements": {
            "thumb_extended": False,
            "index_extended": True,
            "middle_extended": False,
            "ring_extended": False,
            "pinky_extended": True,
        },
        "color": (255, 255, 0),  # Cyan in BGR
        "confidence_threshold": 0.80,
    },
    "Cursed Speech Technique": {
        "gesture": "point",
        "description": "Only index finger extended",
        "character": "Yuji Itadori",
        "power": "Commands have absolute power over targets",
        "finger_requirements": {
            "thumb_extended": False,
            "index_extended": True,
            "middle_extended": False,
            "ring_extended": False,
            "pinky_extended": False,
        },
        "color": (0, 255, 255),  # Yellow in BGR
        "confidence_threshold": 0.80,
    },
}

# Reference guide text
GESTURE_REFERENCE = """
=== DOMAIN EXPANSION GESTURE REFERENCE ===

🌀 UNLIMITED VOID (Gojo)
   Hand: ALL FINGERS EXTENDED (Open Palm)
   Power: Infinite space domain

✌️  CHIMERA SHADOW GARDEN (Yuji)
   Hand: INDEX + MIDDLE UP (Peace Sign)
   Power: Shadow confusion domain

👍 MALEVOLENT SHRINE (Sukuna)
   Hand: THUMB UP (Thumbs Up)
   Power: Cutting domain

✊ IDLE DEATH GAMBLE (Gojo)
   Hand: ALL FINGERS CLOSED (Fist)
   Power: Probability gamble domain

🤘 EVOLVING WOMB (Mahito)
   Hand: INDEX + PINKY UP (Rocker)
   Power: Transfigured monsters domain

☝️  CURSED SPEECH (Yuji)
   Hand: INDEX ONLY (Point)
   Power: Absolute command domain

=== TIPS ===
• Keep hands visible to camera
• Hold gesture steady for 1-2 seconds
• Good lighting improves detection
• Max 2 hands detected simultaneously
"""


def get_gesture_info(gesture_name):
    """Get detailed information about a gesture"""
    if gesture_name in DOMAIN_GESTURES:
        return DOMAIN_GESTURES[gesture_name]
    return None


def get_gesture_color(gesture_name):
    """Get the color associated with a gesture"""
    gesture_info = get_gesture_info(gesture_name)
    if gesture_info:
        return gesture_info["color"]
    return (255, 255, 255)  # White default


def get_all_gestures():
    """Get all available gestures"""
    return list(DOMAIN_GESTURES.keys())


def get_gesture_by_id(gesture_id):
    """Get gesture by index"""
    gestures = get_all_gestures()
    if 0 <= gesture_id < len(gestures):
        return gestures[gesture_id]
    return None


def print_gesture_guide():
    """Print gesture reference guide to console"""
    print(GESTURE_REFERENCE)


def validate_gesture_requirements(finger_states, gesture_name):
    """
    Validate if hand state matches gesture requirements

    Args:
        finger_states: Dict of finger extension states
        gesture_name: Name of gesture to validate

    Returns:
        Tuple: (matches, confidence_score)
    """
    gesture_info = get_gesture_info(gesture_name)
    if not gesture_info:
        return False, 0.0

    requirements = gesture_info["finger_requirements"]
    threshold = gesture_info["confidence_threshold"]

    matches = 0
    total = len(requirements)

    for finger, should_extend in requirements.items():
        if finger_states.get(finger, False) == should_extend:
            matches += 1

    confidence = matches / total
    meets_threshold = confidence >= threshold

    return meets_threshold, confidence
