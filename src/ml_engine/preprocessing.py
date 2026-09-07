import numpy as np

def normalize_landmarks(landmarks):
    """
    Normalize 21 3D landmarks relative to the wrist (Point 0).
    Makes the detection distance-invariant and hand-size invariant.

    Args:
        landmarks: List of [x, y, z] lists or dicts with x,y,z attributes for 21 points.

    Returns:
        A flattened numpy array of 63 elements.
    """
    if not landmarks or len(landmarks) < 21:
        return None

    # Handle both list of lists and list of objects with x, y, z
    if isinstance(landmarks[0], (list, tuple, np.ndarray)):
        wrist = np.array(landmarks[0])
        coords = np.array(landmarks)
    else:
        # Assuming objects with x, y, z attributes
        wrist = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])
        coords = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

    # 1. Translate relative to wrist
    normalized = coords - wrist

    # 2. Normalize by hand size (e.g., distance from wrist to middle finger MCP)
    # Using index 9 for Middle Finger MCP
    hand_size = np.linalg.norm(normalized[9])

    if hand_size > 0:
        normalized = normalized / hand_size

    return normalized.flatten()
