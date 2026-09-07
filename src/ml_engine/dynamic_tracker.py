import collections
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

class DynamicTracker:
    def __init__(self, buffer_size=30):
        # We track the trajectory of the wrist (0) and index finger tip (8)
        self.buffer_size = buffer_size
        self.wrist_buffer = collections.deque(maxlen=buffer_size)
        self.index_buffer = collections.deque(maxlen=buffer_size)

        # In a real app, this would load from a JSON/Pickle of recorded trajectories
        self.templates = self._load_templates()

    def _load_templates(self):
        # Mock templates for basic phrases
        # Each template is a sequence of relative (x, y) coordinates
        # Real implementation would load saved numpy arrays of ideal trajectories
        return {
            "THANK_YOU": {
                # Moving forward and down from chin
                "wrist": np.array([[0, 0], [0, 0.1], [0, 0.2], [0, 0.3]]),
                "index": np.array([[0, 0], [0, 0.1], [0, 0.2], [0, 0.3]])
            },
            "SORRY": {
                # Circular motion over chest
                "wrist": np.array([[0,0], [0.1,-0.1], [0.2,0], [0.1,0.1], [0,0]]),
                "index": np.array([[0,0], [0.1,-0.1], [0.2,0], [0.1,0.1], [0,0]])
            }
        }

    def update_buffer(self, landmarks):
        """Add current frame's key points to the rolling buffer."""
        if not landmarks or len(landmarks) < 21:
            return

        # Extract raw coordinates (not normalized, as we care about motion)
        if hasattr(landmarks[0], 'x'):
            wrist = [landmarks[0].x, landmarks[0].y]
            index = [landmarks[8].x, landmarks[8].y]
        else:
            wrist = [landmarks[0][0], landmarks[0][1]]
            index = [landmarks[8][0], landmarks[8][1]]

        self.wrist_buffer.append(wrist)
        self.index_buffer.append(index)

    def _normalize_trajectory(self, trajectory):
        """Make trajectory invariant to starting position."""
        if not trajectory or len(trajectory) < 2:
            return np.array([])
        traj = np.array(trajectory)
        return traj - traj[0]

    def predict(self):
        """
        Use DTW to match the current buffer against templates.
        Returns: (predicted_label, confidence)
        """
        if len(self.wrist_buffer) < 10:  # Need minimum frames
            return None, 0.0

        current_wrist_traj = self._normalize_trajectory(self.wrist_buffer)

        best_match = None
        min_distance = float('inf')

        for label, template in self.templates.items():
            template_wrist = template['wrist']

            # Dynamic Time Warping distance
            distance, path = fastdtw(current_wrist_traj, template_wrist, dist=euclidean)

            # Normalize distance by path length
            normalized_dist = distance / len(path)

            if normalized_dist < min_distance:
                min_distance = normalized_dist
                best_match = label

        # Threshold to ensure it's a confident match
        if min_distance < 0.15: # Threshold requires tuning with real data
            # Map distance to a confidence score 0.0 - 1.0
            confidence = max(0.0, 1.0 - (min_distance / 0.15))
            return best_match, confidence

        return None, 0.0
