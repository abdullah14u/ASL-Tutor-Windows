import time
from PySide6.QtCore import QObject, Signal, QTimer
from src.curriculum.levels import GameState, CURRICULUM_TIERS

class CurriculumManager(QObject):
    # Signals to update UI
    # progress_updated: current_sign, progress_percentage, state_color (green/amber/red)
    progress_updated = Signal(str, float, str)
    score_updated = Signal(int, int) # score, streak
    tier_completed = Signal(str)

    HOLD_TIME = 1.5 # seconds required to hold the sign

    def __init__(self):
        super().__init__()
        self.state = GameState()
        self.hold_start_time = 0
        self.is_holding = False
        self.last_valid_prediction_time = 0
        self.grace_period = 0.5 # seconds

        self.total_attempts = 0
        self.successful_attempts = 0

    def process_prediction(self, predicted_sign):
        target_sign = self.state.get_current_sign()

        if target_sign is None:
            return # Tier complete

        current_time = time.time()

        if predicted_sign == target_sign:
            self.last_valid_prediction_time = current_time
            if not self.is_holding:
                self.is_holding = True
                self.hold_start_time = current_time
                self.progress_updated.emit(target_sign, 0.0, "amber")
            else:
                elapsed = current_time - self.hold_start_time
                progress = min(1.0, elapsed / self.HOLD_TIME)

                if progress >= 1.0:
                    self._sign_mastered()
                else:
                    self.progress_updated.emit(target_sign, progress, "green")
        else:
            # Check grace period
            if current_time - self.last_valid_prediction_time > self.grace_period:
                # Reset hold if wrong sign and grace period expired
                self.is_holding = False
                self.progress_updated.emit(target_sign, 0.0, "red" if predicted_sign else "amber")
            else:
                # Still within grace period, act like it's holding but don't advance timer much
                if self.is_holding:
                    elapsed = current_time - self.hold_start_time
                    progress = min(1.0, elapsed / self.HOLD_TIME)
                    self.progress_updated.emit(target_sign, progress, "amber")

    def _sign_mastered(self):
        self.is_holding = False
        self.state.score += 10 + (self.state.streak * 2)
        self.state.streak += 1

        self.successful_attempts += 1
        self.total_attempts += 1

        self.score_updated.emit(self.state.score, self.state.streak)
        self.progress_updated.emit(self.state.get_current_sign(), 1.0, "green")

        # Advance to next sign
        self.state.current_sign_index += 1
        tier = self.state.get_current_tier()

        if self.state.current_sign_index >= len(tier['signs']):
            self.tier_completed.emit(tier['name'])
            self._next_tier()

    def _next_tier(self):
        self.state.current_tier_index += 1
        self.state.current_sign_index = 0
        if self.state.current_tier_index >= len(CURRICULUM_TIERS):
             self.state.current_tier_index = 0 # Loop back or handle end of game

    def reset_streak(self):
        if self.state.streak > 0:
            self.state.streak = 0
            self.score_updated.emit(self.state.score, self.state.streak)

    def get_accuracy(self):
        if self.total_attempts == 0:
            return 100.0
        return (self.successful_attempts / self.total_attempts) * 100.0
