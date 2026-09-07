import json
import time
import random
import os
from PySide6.QtCore import QObject, Signal

class CurriculumManager(QObject):
    # Signals to update UI
    # progress_updated: sign_info(dict), progress_percentage, state_color (green/amber/red)
    progress_updated = Signal(dict, float, str)
    score_updated = Signal(int, int) # score, streak
    lesson_completed = Signal(str, int) # lesson title, xp gained
    unit_unlocked = Signal(str)

    HOLD_TIME = 1.5 # seconds required to hold static signs
    DYNAMIC_HOLD_TIME = 0.5 # faster validation for dynamic gestures

    def __init__(self, curriculum_path='assets/curriculum.json'):
        super().__init__()
        self.curriculum = self._load_curriculum(curriculum_path)

        self.current_unit_idx = 0
        self.current_lesson_idx = 0

        # Spaced repetition / Lesson generation state
        self.active_queue = [] # Queue of sign_info dicts
        self.learned_signs = [] # Pool of previously learned signs for mix-in

        self.score = 0
        self.streak = 0

        # Evaluation state
        self.hold_start_time = 0
        self.is_holding = False
        self.last_valid_prediction_time = 0
        self.grace_period = 0.5

        self.total_attempts = 0
        self.successful_attempts = 0

        # Initialize first lesson if curriculum loaded
        if self.curriculum and self.curriculum.get('units'):
            self._start_lesson()

    def _load_curriculum(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"units": []}

    def _start_lesson(self):
        """Generates the queue for the current lesson with spaced repetition logic."""
        if self.current_unit_idx >= len(self.curriculum['units']):
            return # All units complete

        unit = self.curriculum['units'][self.current_unit_idx]
        if self.current_lesson_idx >= len(unit['lessons']):
            # Advance to next unit
            self.current_unit_idx += 1
            self.current_lesson_idx = 0
            if self.current_unit_idx < len(self.curriculum['units']):
                next_unit = self.curriculum['units'][self.current_unit_idx]
                self.unit_unlocked.emit(next_unit['name'])
                self._start_lesson()
            return

        lesson = unit['lessons'][self.current_lesson_idx]
        new_signs = lesson['signs']

        self.active_queue = []

        # 1. Introduce new signs (usually 3)
        for sign in new_signs:
            self.active_queue.append(sign)

        # 2. Mix in 1 old sign if available (Spaced Repetition)
        if self.learned_signs:
            old_sign = random.choice(self.learned_signs)
            self.active_queue.insert(random.randint(1, len(self.active_queue)), old_sign)

        # 3. Boss level / Review (shuffle them all again)
        review_signs = self.active_queue.copy()
        random.shuffle(review_signs)
        self.active_queue.extend(review_signs)

        # Add new signs to learned pool for future lessons
        for sign in new_signs:
            if sign not in self.learned_signs:
                self.learned_signs.append(sign)

    def get_current_sign_info(self):
        if not self.active_queue:
            return None
        return self.active_queue[0]

    def process_prediction(self, predicted_label):
        current_sign_info = self.get_current_sign_info()

        if current_sign_info is None:
            return # Lesson complete

        target_label = current_sign_info['label']
        is_dynamic = current_sign_info.get('type') == 'dynamic'
        required_hold = self.DYNAMIC_HOLD_TIME if is_dynamic else self.HOLD_TIME

        current_time = time.time()

        if predicted_label == target_label:
            self.last_valid_prediction_time = current_time
            if not self.is_holding:
                self.is_holding = True
                self.hold_start_time = current_time
                self.progress_updated.emit(current_sign_info, 0.0, "amber")
            else:
                elapsed = current_time - self.hold_start_time
                progress = min(1.0, elapsed / required_hold)

                if progress >= 1.0:
                    self._sign_mastered()
                else:
                    self.progress_updated.emit(current_sign_info, progress, "green")
        else:
            if current_time - self.last_valid_prediction_time > self.grace_period:
                self.is_holding = False
                self.progress_updated.emit(current_sign_info, 0.0, "red" if predicted_label else "amber")
            else:
                if self.is_holding:
                    elapsed = current_time - self.hold_start_time
                    progress = min(1.0, elapsed / required_hold)
                    self.progress_updated.emit(current_sign_info, progress, "amber")

    def _sign_mastered(self):
        self.is_holding = False

        # XP calculation
        base_xp = 10
        combo_bonus = self.streak * 2
        xp_gained = base_xp + combo_bonus

        self.score += xp_gained
        self.streak += 1

        self.successful_attempts += 1
        self.total_attempts += 1

        self.score_updated.emit(self.score, self.streak)

        # Emit 1.0 progress to UI for green flash
        current_info = self.get_current_sign_info()
        self.progress_updated.emit(current_info, 1.0, "green")

        # Advance queue
        if self.active_queue:
            self.active_queue.pop(0)

        if not self.active_queue:
            self._lesson_complete(xp_gained)

    def _lesson_complete(self, final_xp):
        unit = self.curriculum['units'][self.current_unit_idx]
        lesson = unit['lessons'][self.current_lesson_idx]

        title = lesson['title']

        # Increment internal state before emitting signal so UI pulls correct next state
        self.current_lesson_idx += 1

        # Must populate the queue for the next lesson before the UI updates
        self._start_lesson()

        self.lesson_completed.emit(title, final_xp)

    def reset_streak(self):
        if self.streak > 0:
            self.streak = 0
            self.score_updated.emit(self.score, self.streak)

    def get_accuracy(self):
        if self.total_attempts == 0:
            return 100.0
        return (self.successful_attempts / self.total_attempts) * 100.0
