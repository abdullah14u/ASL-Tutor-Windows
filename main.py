import sys
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.vision.worker import CameraWorker
import time
from src.curriculum.manager import CurriculumManager

class ASLTutorApp(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

        self.vision_worker = CameraWorker()
        self.curriculum = CurriculumManager()

        self._connect_signals()

        # Initialize UI state
        if self.curriculum.curriculum.get('units'):
            unit = self.curriculum.curriculum['units'][self.curriculum.current_unit_idx]
            lesson = unit['lessons'][self.curriculum.current_lesson_idx]
            self.main_window.update_tier_info(f"{unit['name']} - {lesson['title']}")

            # Configure engine for first sign
            first_sign = self.curriculum.get_current_sign_info()
            self.vision_worker.set_expected_sign(first_sign)
            self.main_window.update_prompt(first_sign)

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
        self.curriculum.lesson_completed.connect(self._handle_lesson_completed)
        self.curriculum.unit_unlocked.connect(self.main_window.unlock_next_unit)

    def _handle_frame(self, rgb_frame, landmarks, latency, fps, handedness, predicted_sign, confidence):
        # 1. Update HUD
        self.main_window.hud.update_stats(fps, latency, confidence)

        # 3. Process game logic
        self.curriculum.process_prediction(predicted_sign)

        # 4. Draw frame
        state = self.main_window.camera_feed.current_state # Read back current state
        progress = self.main_window.camera_feed.progress
        self.main_window.camera_feed.update_frame(rgb_frame, landmarks, state, progress)

    def _handle_progress(self, sign_info, progress, state_color):
        self.main_window.update_prompt(sign_info)

        # Configure ML Engine for the expected sign type
        self.vision_worker.set_expected_sign(sign_info)

        self.main_window.camera_feed.current_state = state_color
        self.main_window.camera_feed.progress = progress
        self.main_window.update_accuracy(self.curriculum.get_accuracy())

    def _handle_lesson_completed(self, title, xp):
        self.main_window.show_lesson_completed(title, xp)
        self.main_window.show_path_page()

        # Reset visual state
        self.main_window.camera_feed.current_state = None
        self.main_window.camera_feed.progress = 0.0

        # Update UI for next lesson
        if self.curriculum.current_unit_idx < len(self.curriculum.curriculum['units']):
            unit = self.curriculum.curriculum['units'][self.curriculum.current_unit_idx]
            if self.curriculum.current_lesson_idx < len(unit['lessons']):
                lesson = unit['lessons'][self.curriculum.current_lesson_idx]
                self.main_window.update_tier_info(f"{unit['name']} - {lesson['title']}")

            # Configure engine for first sign of new lesson
            first_sign = self.curriculum.get_current_sign_info()
            self.vision_worker.set_expected_sign(first_sign)
            self.main_window.update_prompt(first_sign)
        else:
            self.main_window.update_tier_info("Curriculum Complete!")
            self.vision_worker.set_expected_sign(None)
            self.main_window.sign_prompt.setText("DONE")

    def _change_camera(self, index):
        self.vision_worker.stop()
        self.vision_worker = CameraWorker(camera_index=index)
        self.vision_worker.frame_processed.connect(self._handle_frame)
        self.vision_worker.error_occurred.connect(self._handle_camera_error)
        self.vision_worker.start()

    def _handle_camera_error(self, err_msg):
        print(f"Camera Error: {err_msg}")

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = ASLTutorApp()
    app.run()
