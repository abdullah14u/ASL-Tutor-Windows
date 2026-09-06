import math
from src.classifier.dictionary import ASL_DICTIONARY, ASL_NUMBERS, FINGER_STATE_EXTENDED, FINGER_STATE_CURLED, FINGER_STATE_HALF_CURLED

class GestureEngine:
    def __init__(self):
        # Merge dictionaries for a unified lookup
        self.dictionary = {**ASL_DICTIONARY, **ASL_NUMBERS}

    def _calculate_distance(self, p1, p2):
        """Euclidean distance between two 3D points."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

    def _get_finger_states(self, landmarks):
        """
        Analyze the landmarks and return the state of each finger.
        Landmarks index (MediaPipe standard):
        0: Wrist, 1-4: Thumb, 5-8: Index, 9-12: Middle, 13-16: Ring, 17-20: Pinky
        """
        states = {}

        wrist = landmarks[0]

        # Calculate palm size for relative thresholding
        palm_size = self._calculate_distance(wrist, landmarks[9])

        # Finger tip and pip indices
        fingers = {
            'index': (8, 6, 5),
            'middle': (12, 10, 9),
            'ring': (16, 14, 13),
            'pinky': (20, 18, 17)
        }

        for name, (tip_idx, pip_idx, mcp_idx) in fingers.items():
            tip = landmarks[tip_idx]
            pip = landmarks[pip_idx]
            mcp = landmarks[mcp_idx]

            # Simple heuristic: distance from wrist to tip vs wrist to pip/mcp
            dist_tip_wrist = self._calculate_distance(tip, wrist)
            dist_mcp_wrist = self._calculate_distance(mcp, wrist)

            # Distance from tip to mcp
            dist_tip_mcp = self._calculate_distance(tip, mcp)

            if dist_tip_wrist > dist_mcp_wrist + palm_size * 0.2:
                states[name] = FINGER_STATE_EXTENDED
            elif dist_tip_mcp > palm_size * 0.4:
                states[name] = FINGER_STATE_HALF_CURLED
            else:
                states[name] = FINGER_STATE_CURLED

        # Thumb logic (different axis of movement)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        pinky_mcp = landmarks[17]

        # If thumb tip is further from pinky mcp than thumb mcp, it's extended
        dist_thumb_tip_pinky = self._calculate_distance(thumb_tip, pinky_mcp)
        dist_thumb_mcp_pinky = self._calculate_distance(thumb_mcp, pinky_mcp)

        if dist_thumb_tip_pinky > dist_thumb_mcp_pinky + palm_size * 0.1:
            states['thumb'] = FINGER_STATE_EXTENDED
        elif dist_thumb_tip_pinky > dist_thumb_mcp_pinky - palm_size * 0.1:
             states['thumb'] = FINGER_STATE_HALF_CURLED
        else:
            states['thumb'] = FINGER_STATE_CURLED

        return states

    def classify(self, landmarks):
        """
        Classifies the given hand landmarks into an ASL sign.
        Returns (predicted_sign, confidence)
        """
        if not landmarks or len(landmarks) < 21:
            return None, 0.0

        current_states = self._get_finger_states(landmarks)

        best_match = None
        highest_score = -1

        for sign, expected_states in self.dictionary.items():
            score = 0
            total_fingers = 5

            for finger, expected in expected_states.items():
                if current_states[finger] == expected:
                    score += 1
                elif abs(current_states[finger] - expected) == 1:
                    # Partial match (e.g., curled vs half-curled)
                    score += 0.5

            confidence = score / total_fingers
            if confidence > highest_score:
                highest_score = confidence
                best_match = sign

        # Only return a match if confidence is above a threshold
        if highest_score >= 0.8:
             return best_match, highest_score

        return None, 0.0
