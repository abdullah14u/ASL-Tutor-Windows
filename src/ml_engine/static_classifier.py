import os
import numpy as np
import onnxruntime as ort

class StaticClassifier:
    def __init__(self, model_path='model.onnx'):
        self.session = None
        self.input_name = None
        self.classes = []

        if os.path.exists(model_path):
            try:
                self.session = ort.InferenceSession(model_path)
                self.input_name = self.session.get_inputs()[0].name
                # ONNX doesn't store classes inherently in a simple array like sklearn,
                # but if exported via skl2onnx without zipmap, the second output is probabilities.
                # Actually, the string labels are returned as the first output directly!
            except Exception as e:
                print(f"Failed to load ONNX model from {model_path}: {e}")
        else:
            print(f"Warning: Static model not found at {model_path}. Using fallback mode.")

    def predict(self, features):
        """
        Predict static sign from normalized features.

        Args:
            features: A flattened numpy array of 63 elements (from preprocessing).

        Returns:
            Tuple of (predicted_label, confidence_score)
        """
        if self.session is None or features is None:
            return None, 0.0

        try:
            # Reshape for single sample prediction and convert to float32 for ONNX
            X = features.reshape(1, -1).astype(np.float32)

            # Run inference
            # skl2onnx outputs: [label, probabilities]
            outputs = self.session.run(None, {self.input_name: X})

            # Extract label
            label = outputs[0][0]

            # Extract probability if available
            confidence = 1.0
            if len(outputs) > 1:
                # outputs[1] is a list containing a dict of probabilities
                probas_dict = outputs[1][0]
                if label in probas_dict:
                    confidence = float(probas_dict[label])

            # Confidence threshold
            if confidence > 0.6:  # Can be tuned
                return label, confidence
            return None, confidence

        except Exception as e:
            print(f"Prediction error: {e}")
            return None, 0.0
