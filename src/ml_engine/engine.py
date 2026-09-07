from src.ml_engine.preprocessing import normalize_landmarks
from src.ml_engine.static_classifier import StaticClassifier
from src.ml_engine.dynamic_tracker import DynamicTracker

class GestureEngine:
    def __init__(self, model_path='model.onnx'):
        self.static_classifier = StaticClassifier(model_path=model_path)
        self.dynamic_tracker = DynamicTracker()

        # Set expected mode (None = both, 'STATIC' or 'DYNAMIC')
        self.mode = None
        self.expected_sign = None

    def set_expected_sign(self, sign_info):
        """
        Configure the engine based on what sign the curriculum expects next.
        sign_info: dict with 'type' ('static'/'dynamic') and 'label'.
        """
        if sign_info:
            self.mode = sign_info.get('type', 'static').upper()
            self.expected_sign = sign_info.get('label')

            # Reset buffers when switching to dynamic
            if self.mode == 'DYNAMIC':
                self.dynamic_tracker.wrist_buffer.clear()
                self.dynamic_tracker.index_buffer.clear()
        else:
            self.mode = None
            self.expected_sign = None

    def classify(self, landmarks):
        """
        Main entry point for processing a frame's landmarks.
        Routes to the appropriate sub-engine based on current mode.

        Returns: (predicted_sign, confidence)
        """
        if not landmarks:
            return None, 0.0

        if self.mode == 'DYNAMIC':
            self.dynamic_tracker.update_buffer(landmarks)
            return self.dynamic_tracker.predict()

        else:
            # Default to STATIC processing
            normalized_features = normalize_landmarks(landmarks)

            # Fallback to older geometric engine if ML model isn't trained
            if self.static_classifier.session is None:
                # We can import and use the old engine here if needed,
                # but for this rewrite we'll just return None, 0 if no model
                # To keep it completely independent
                pass

            return self.static_classifier.predict(normalized_features)
