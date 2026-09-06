from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QPushButton
)
from PySide6.QtCore import Qt, QTimer
from src.gui.styles import MAIN_STYLE, COLORS
from src.gui.components import CameraFeedWidget, HUDOverlay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASL Tutor Pro")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(MAIN_STYLE)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout (HBox: Left for Camera, Right for Prompts/Score)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self._setup_left_panel()
        self._setup_right_panel()

    def _setup_left_panel(self):
        # Left side layout
        self.left_panel = QVBoxLayout()

        # Top bar with camera selection
        self.camera_selector = QComboBox()
        self.camera_selector.addItems(["Camera 0", "Camera 1", "Camera 2"])

        self.left_panel.addWidget(self.camera_selector)

        # Camera Feed Widget
        self.camera_feed = CameraFeedWidget()
        self.left_panel.addWidget(self.camera_feed, stretch=1)

        self.main_layout.addLayout(self.left_panel, stretch=2)

    def _setup_right_panel(self):
        # Right side layout
        self.right_panel = QVBoxLayout()

        # Dashboard Card
        self.dashboard_card = QFrame()
        self.dashboard_card.setObjectName("SurfaceFrame")
        dash_layout = QVBoxLayout(self.dashboard_card)

        # Tier Title
        self.tier_title = QLabel("Level 1: Static Basics")
        self.tier_title.setObjectName("TitleLabel")
        self.tier_title.setAlignment(Qt.AlignCenter)

        # Sign Prompt
        self.sign_prompt = QLabel("A")
        self.sign_prompt.setObjectName("SignPrompt")
        self.sign_prompt.setAlignment(Qt.AlignCenter)

        # Score & Streak
        score_layout = QHBoxLayout()
        self.score_label = QLabel("Score: 0")
        self.score_label.setStyleSheet(f"font-size: 18px; color: {COLORS['primary']};")

        self.streak_label = QLabel("Streak: 0")
        self.streak_label.setStyleSheet(f"font-size: 18px; color: {COLORS['warning']};")

        score_layout.addWidget(self.score_label)
        score_layout.addWidget(self.streak_label)

        # Accuracy
        self.accuracy_label = QLabel("Accuracy: 100%")
        self.accuracy_label.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
        self.accuracy_label.setAlignment(Qt.AlignCenter)

        # HUD Overlay (Performance)
        self.hud = HUDOverlay()

        dash_layout.addWidget(self.tier_title)
        dash_layout.addSpacing(20)
        dash_layout.addWidget(self.sign_prompt)
        dash_layout.addSpacing(20)
        dash_layout.addLayout(score_layout)
        dash_layout.addWidget(self.accuracy_label)
        dash_layout.addSpacing(20)
        dash_layout.addWidget(self.hud, alignment=Qt.AlignHCenter)

        self.right_panel.addWidget(self.dashboard_card)
        self.main_layout.addLayout(self.right_panel, stretch=1)

    def update_tier_info(self, tier_name):
        self.tier_title.setText(tier_name)

    def update_prompt(self, sign):
        if sign:
            self.sign_prompt.setText(sign)
        else:
            self.sign_prompt.setText("DONE")

    def update_score(self, score, streak):
        self.score_label.setText(f"Score: {score}")
        self.streak_label.setText(f"Streak: {streak}")

    def update_accuracy(self, accuracy):
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
