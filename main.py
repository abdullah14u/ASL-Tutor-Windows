import sys
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.vision.worker import CameraWorker
from src.classifier.engine import GestureEngine
import time
from src.curriculum.manager import CurriculumManager

class ASLTutorApp(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

        self.vision_worker = CameraWorker()
        self.gesture_engine = GestureEngine()
        self.curriculum = CurriculumManager()

        self._connect_signals()

        # Initialize UI state
        tier = self.curriculum.state.get_current_tier()
        self.main_window.update_tier_info(tier['name'])
        self.main_window.update_prompt(self.curriculum.state.get_current_sign())

        self.vision_worker.start()

    def _connect_signals(self):
        # Vision -> UI & Engine
        self.vision_worker.frame_processed.connect(self._handle_frame)
        self.vision_worker.error_occurred.connect(self._handle_camera_error)

        # UI -> Vision
        self.main_window.camera_selector.currentIndexChanged.connect(self._change_camera)

        # Curriculum -> UI
        self.curriculum.progress_updated.connect(self._handle_progress)
        self.curriculum.score_updated.connect(self.main_window.update_score)
        self.curriculum.tier_completed.connect(self.main_window.update_tier_info)

    def _handle_frame(self, rgb_frame, landmarks, latency, fps, handedness):
        # 1. Classify gesture
        predicted_sign, confidence = self.gesture_engine.classify(landmarks)

        # 2. Update HUD
        self.main_window.hud.update_stats(fps, latency, confidence)

        # 3. Process game logic (if handedness is right or left, simplified here we just pass prediction)
        self.curriculum.process_prediction(predicted_sign)

        # Reset streak happens inside process_prediction indirectly now, or if totally dropped for a while
        if not predicted_sign and time.time() - self.curriculum.last_valid_prediction_time > self.curriculum.grace_period:
            self.curriculum.reset_streak()

        # 4. Draw frame (the actual visual update is handled via progress_updated signal for state,
        # but we need to push the image to the widget)
        state = self.main_window.camera_feed.current_state # Read back current state
        progress = self.main_window.camera_feed.progress
        self.main_window.camera_feed.update_frame(rgb_frame, landmarks, state, progress)

    def _handle_progress(self, target_sign, progress, state_color):
        self.main_window.update_prompt(target_sign)
        self.main_window.camera_feed.current_state = state_color
        self.main_window.camera_feed.progress = progress
        self.main_window.update_accuracy(self.curriculum.get_accuracy())

    def _change_camera(self, index):
        self.vision_worker.stop()
        self.vision_worker = CameraWorker(camera_index=index)
        self.vision_worker.frame_processed.connect(self._handle_frame)
        self.vision_worker.error_occurred.connect(self._handle_camera_error)
        self.vision_worker.start()

    def _handle_camera_error(self, err_msg):
        print(f"Camera Error: {err_msg}")
        # Could show a QMessageBox here

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = ASLTutorApp()
    app.run()
