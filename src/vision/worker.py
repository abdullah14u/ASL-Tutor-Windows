import cv2
import mediapipe as mp
import time
import numpy as np
from PySide6.QtCore import QThread, Signal
from src.vision.filters import EMAFilter
from src.ml_engine.engine import GestureEngine

class CameraWorker(QThread):
    # Signals to communicate with the main GUI thread
    # Emit frame (as numpy array), landmarks, latency, fps, hand_handedness, predicted_sign, confidence
    frame_processed = Signal(np.ndarray, list, float, float, str, object, float)
    error_occurred = Signal(str)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.running = True
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.filter = EMAFilter(alpha=0.4)
        self.gesture_engine = GestureEngine()

        # FPS calculation variables
        self.prev_time = 0

    def set_expected_sign(self, sign_info):
        self.gesture_engine.set_expected_sign(sign_info)

    def set_camera(self, index):
        self.camera_index = index

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        # Try to use DirectShow on Windows for low latency, fallback to default otherwise
        if hasattr(cv2, 'CAP_DSHOW') and (cap.getBackendName() if cap.isOpened() else '') != 'DSHOW':
             cap_dshow = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
             if cap_dshow.isOpened():
                 cap = cap_dshow

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)

        if not cap.isOpened():
            self.error_occurred.emit(f"Could not open camera {self.camera_index}")
            return

        while self.running:
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                continue

            # Flip the frame horizontally for a selfie-view display
            frame = cv2.flip(frame, 1)

            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False

            # Inference latency start
            inf_start = time.time()
            results = self.hands.process(rgb_frame)
            inf_latency = (time.time() - inf_start) * 1000  # ms

            rgb_frame.flags.writeable = True

            landmarks = []
            handedness_label = ""

            if results.multi_hand_landmarks:
                # We only process the first hand
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness = results.multi_handedness[0].classification[0].label
                handedness_label = handedness # "Left" or "Right"

                # Extract normalized coordinates (x, y, z)
                raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                # Apply smoothing filter
                landmarks = self.filter.process(raw_landmarks)
            else:
                self.filter.reset()

            # Run ML inference on background thread
            predicted_sign, confidence = self.gesture_engine.classify(landmarks)

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - self.prev_time) if self.prev_time > 0 else 0
            self.prev_time = curr_time

            self.frame_processed.emit(rgb_frame, landmarks, inf_latency, fps, handedness_label, predicted_sign, confidence)

            # Sleep slightly to avoid hogging the CPU, maintain ~60 FPS
            time.sleep(0.005)

        cap.release()
        self.hands.close()

    def stop(self):
        self.running = False
        self.wait()
