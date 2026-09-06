import numpy as np

class EMAFilter:
    """
    Exponential Moving Average (EMA) filter for landmark smoothing.
    Helps to eliminate camera jitter in real-time tracking.
    """
    def __init__(self, alpha=0.5):
        """
        Initialize the EMA Filter.
        :param alpha: Smoothing factor between 0 and 1.
                      Higher values are more responsive (less smoothing),
                      lower values are smoother (more lag).
        """
        self.alpha = alpha
        self.state = None

    def process(self, current_landmarks):
        """
        Process the current landmarks and apply EMA.
        :param current_landmarks: List or array of coordinates.
        :return: Smoothed landmarks.
        """
        if current_landmarks is None or len(current_landmarks) == 0:
            self.state = None
            return current_landmarks

        current_array = np.array(current_landmarks, dtype=np.float32)

        if self.state is None or self.state.shape != current_array.shape:
            self.state = current_array
            return self.state.tolist()

        # Apply EMA: S_t = alpha * Y_t + (1 - alpha) * S_{t-1}
        self.state = self.alpha * current_array + (1 - self.alpha) * self.state
        return self.state.tolist()

    def reset(self):
        """Reset the filter state."""
        self.state = None
