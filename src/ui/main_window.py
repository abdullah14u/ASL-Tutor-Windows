from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint
from src.ui.styles import MAIN_STYLE, COLORS
from src.ui.components import CameraFeedWidget, HUDOverlay, ConfettiWidget, AnimatedButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASL Tutor Pro - Duolingo Style")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(MAIN_STYLE)

        # Central Widget & Stacked Widget for Page Transitions
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Pages
        self.path_page = QWidget()
        self.lesson_page = QWidget()

        self.stacked_widget.addWidget(self.path_page)
        self.stacked_widget.addWidget(self.lesson_page)

        # Build Pages
        self._setup_path_page()
        self._setup_lesson_page()

        # Confetti Overlay
        self.confetti = ConfettiWidget(self)
        self.confetti.resize(self.size())
        self.confetti.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'confetti'):
            self.confetti.resize(self.size())

    def _setup_path_page(self):
        layout = QVBoxLayout(self.path_page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Learning Path")
        title.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(40)

        # Mock Path Nodes
        self.nodes = []
        node_names = ["Unit 1: Alphabet", "Unit 2: Greetings", "Unit 3: Phrases"]

        for i, name in enumerate(node_names):
            btn = AnimatedButton(name)
            btn.setFixedSize(200, 80)
            if i > 0:
                btn.setEnabled(False) # Locked initially
                btn.setStyleSheet(btn.styleSheet() + "background-color: #555;")
            else:
                btn.clicked.connect(self.start_lesson)

            layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.nodes.append(btn)

            if i < len(node_names) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFixedSize(4, 40)
                line.setStyleSheet(f"background-color: {COLORS['surface_light']};")
                layout.addWidget(line, alignment=Qt.AlignCenter)

    def _setup_lesson_page(self):
        # Main Layout (HBox: Left for Camera, Right for Prompts/Score)
        layout = QHBoxLayout(self.lesson_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self._setup_left_panel(layout)
        self._setup_right_panel(layout)

    def _setup_left_panel(self, parent_layout):
        self.left_panel = QVBoxLayout()

        # Header (Back button + Camera)
        header_layout = QHBoxLayout()
        self.back_btn = AnimatedButton("Quit Lesson")
        self.back_btn.clicked.connect(self.show_path_page)
        header_layout.addWidget(self.back_btn)

        self.camera_selector = QComboBox()
        self.camera_selector.addItems(["Camera 0", "Camera 1", "Camera 2"])
        header_layout.addWidget(self.camera_selector)

        self.left_panel.addLayout(header_layout)

        # Camera Feed Widget
        self.camera_feed = CameraFeedWidget()
        self.left_panel.addWidget(self.camera_feed, stretch=1)

        # Dynamic Hint Label
        self.hint_label = QLabel("Hint: Keep your thumb tucked in!")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet(f"font-size: 18px; color: {COLORS['warning']}; padding: 10px; background-color: {COLORS['surface']}; border-radius: 8px;")
        self.left_panel.addWidget(self.hint_label)

        parent_layout.addLayout(self.left_panel, stretch=2)

    def _setup_right_panel(self, parent_layout):
        self.right_panel = QVBoxLayout()

        self.dashboard_card = QFrame()
        self.dashboard_card.setObjectName("SurfaceFrame")
        dash_layout = QVBoxLayout(self.dashboard_card)

        self.tier_title = QLabel("Unit 1: The Alphabet")
        self.tier_title.setObjectName("TitleLabel")
        self.tier_title.setAlignment(Qt.AlignCenter)

        # Top Right Panel: Reference Animation (Placeholder for now)
        self.reference_anim = QLabel("Reference Animation\n(GIF/WebP here)")
        self.reference_anim.setAlignment(Qt.AlignCenter)
        self.reference_anim.setStyleSheet(f"background-color: {COLORS['surface_light']}; border-radius: 12px; font-size: 14px; color: #888;")
        self.reference_anim.setMinimumHeight(200)

        self.sign_prompt = QLabel("A")
        self.sign_prompt.setObjectName("SignPrompt")
        self.sign_prompt.setAlignment(Qt.AlignCenter)

        score_layout = QHBoxLayout()
        self.score_label = QLabel("XP: 0")
        self.score_label.setStyleSheet(f"font-size: 18px; color: {COLORS['primary']}; font-weight: bold;")

        self.streak_label = QLabel("Combo: 0")
        self.streak_label.setStyleSheet(f"font-size: 18px; color: {COLORS['warning']}; font-weight: bold;")

        score_layout.addWidget(self.score_label)
        score_layout.addWidget(self.streak_label)

        self.accuracy_label = QLabel("Accuracy: 100%")
        self.accuracy_label.setStyleSheet(f"font-size: 16px; color: {COLORS['text_muted']};")
        self.accuracy_label.setAlignment(Qt.AlignCenter)

        self.hud = HUDOverlay()

        dash_layout.addWidget(self.tier_title)
        dash_layout.addSpacing(10)
        dash_layout.addWidget(self.reference_anim, stretch=1)
        dash_layout.addSpacing(10)
        dash_layout.addWidget(self.sign_prompt)
        dash_layout.addSpacing(20)
        dash_layout.addLayout(score_layout)
        dash_layout.addWidget(self.accuracy_label)
        dash_layout.addSpacing(20)
        dash_layout.addWidget(self.hud, alignment=Qt.AlignHCenter)

        self.right_panel.addWidget(self.dashboard_card)
        parent_layout.addLayout(self.right_panel, stretch=1)

    def show_lesson_completed(self, title, xp):
        self.confetti.start()
        # Optionally show a popup dialog here
        print(f"Lesson Completed: {title}! Gained {xp} XP.")

    def unlock_next_unit(self, unit_name):
        # Simple logic to unlock the next button in the list
        for btn in self.nodes:
            if not btn.isEnabled():
                btn.setEnabled(True)
                btn.setStyleSheet("") # Reset to default animated button style
                btn.clicked.connect(self.start_lesson)
                print(f"Unlocked {unit_name}!")
                break

    def _slide_transition(self, index):
        """Implement sliding page transitions using QPropertyAnimation."""
        current_index = self.stacked_widget.currentIndex()
        if current_index == index:
            return

        current_widget = self.stacked_widget.widget(current_index)
        next_widget = self.stacked_widget.widget(index)

        offset = self.width() if index > current_index else -self.width()

        next_widget.setGeometry(0, 0, self.width(), self.height())

        self.anim_group = QPropertyAnimation(current_widget, b"pos")
        self.anim_group.setDuration(300)
        self.anim_group.setStartValue(current_widget.pos())
        self.anim_group.setEndValue(current_widget.pos() + QPoint(-offset, 0))
        self.anim_group.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim_group2 = QPropertyAnimation(next_widget, b"pos")
        self.anim_group2.setDuration(300)
        self.anim_group2.setStartValue(QPoint(offset, 0))
        self.anim_group2.setEndValue(QPoint(0, 0))
        self.anim_group2.setEasingCurve(QEasingCurve.InOutQuad)

        next_widget.show()
        next_widget.raise_()

        self.anim_group.start()
        self.anim_group2.start()

        # Change index after animation (simplified here)
        QTimer.singleShot(300, lambda: self.stacked_widget.setCurrentIndex(index))

    def start_lesson(self):
        self._slide_transition(1)

    def show_path_page(self):
        self._slide_transition(0)

    def update_tier_info(self, tier_name):
        self.tier_title.setText(tier_name)

    def update_prompt(self, sign_info):
        if sign_info:
            self.sign_prompt.setText(sign_info['label'])
            self.hint_label.setText(f"Hint: {sign_info.get('hint', '')}")

            # Update reference animation based on type
            if sign_info.get('type') == 'dynamic':
                self.reference_anim.setText(f"Motion: {sign_info['label']}\n(GIF Placeholder)")
            else:
                self.reference_anim.setText(f"Static: {sign_info['label']}\n(Image Placeholder)")

        else:
            self.sign_prompt.setText("DONE")
            self.hint_label.setText("Lesson Complete!")

    def update_score(self, score, streak):
        self.score_label.setText(f"XP: {score}")
        self.streak_label.setText(f"Combo: {streak}")

    def update_accuracy(self, accuracy):
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
