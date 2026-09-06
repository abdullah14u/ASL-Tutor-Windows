import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRectF
from src.gui.styles import COLORS

class CameraFeedWidget(QLabel):
    """Displays the camera feed with optional glow/border based on state."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(640, 480)
        self.setStyleSheet(f"background-color: {COLORS['surface']}; border-radius: 12px;")

        self.current_state = None # "green", "red", "amber", None
        self.progress = 0.0

    def update_frame(self, rgb_frame, landmarks, state=None, progress=0.0):
        self.current_state = state
        self.progress = progress

        h, w, ch = rgb_frame.shape

        # Optionally draw skeletal overlay on the frame before conversion
        if landmarks:
            self._draw_landmarks(rgb_frame, landmarks, w, h)

        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Scale image to fit widget
        pixmap = QPixmap.fromImage(q_img).scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        self.setPixmap(pixmap)

    def _draw_landmarks(self, img, landmarks, w, h):
        """Draws skeletal hand connections."""
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4), # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8), # Index
            (5, 9), (9, 10), (10, 11), (11, 12), # Middle
            (9, 13), (13, 14), (14, 15), (15, 16), # Ring
            (13, 17), (17, 18), (18, 19), (19, 20), # Pinky
            (0, 17) # Palm base
        ]

        # Use cyan for the lines
        color = (212, 182, 6) # OpenCV uses BGR natively, but we get RGB. So (06B6D4 -> RGB -> BGR is not needed here as we are given RGB frame and mediapipe processed RGB)
        # Wait, if we are in RGB space (cv2.cvtColor was called), we should use RGB color.
        # Cyan #06B6D4 is R=6, G=182, B=212
        line_color = (6, 182, 212)
        point_color = (248, 250, 252) # Slate 50

        points = []
        for lm in landmarks:
            cx, cy = int(lm[0] * w), int(lm[1] * h)
            points.append((cx, cy))

        for connection in connections:
            p1 = points[connection[0]]
            p2 = points[connection[1]]
            cv2.line(img, p1, p2, line_color, 2, cv2.LINE_AA)

        for p in points:
            cv2.circle(img, p, 4, point_color, -1, cv2.LINE_AA)

    def paintEvent(self, event):
        super().paintEvent(event)

        # Draw feedback border
        if self.current_state:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            if self.current_state == "green":
                color_hex = COLORS['success']
            elif self.current_state == "red":
                color_hex = COLORS['error']
            else:
                color_hex = COLORS['warning']

            color = QColor(color_hex)

            # Glow effect approximation (draw thick slightly transparent border, then inner border)
            pen_glow = QPen(QColor(color.red(), color.green(), color.blue(), 100), 8)
            painter.setPen(pen_glow)
            painter.drawRoundedRect(4, 4, self.width() - 8, self.height() - 8, 12, 12)

            pen_solid = QPen(color, 4)
            painter.setPen(pen_solid)
            painter.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 12, 12)

            # Draw progress radial at the bottom center if holding
            if self.progress > 0 and self.progress < 1.0:
                rect = QRectF(self.width() / 2 - 30, self.height() - 80, 60, 60)

                # Background circle
                painter.setPen(QPen(QColor(COLORS['surface_light']), 6))
                painter.drawArc(rect, 0, 360 * 16)

                # Progress arc
                painter.setPen(QPen(color, 6))
                span_angle = int(-self.progress * 360 * 16) # Negative for clockwise
                painter.drawArc(rect, 90 * 16, span_angle)

class HUDOverlay(QFrame):
    """Displays FPS, latency, and system info."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SurfaceFrame")
        self.setFixedWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")

        self.latency_label = QLabel("Latency: -- ms")
        self.latency_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")

        self.confidence_label = QLabel("Confidence: --%")
        self.confidence_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")

        layout.addWidget(self.fps_label)
        layout.addWidget(self.latency_label)
        layout.addWidget(self.confidence_label)

    def update_stats(self, fps, latency, confidence=0.0):
        self.fps_label.setText(f"FPS: {int(fps)}")
        self.latency_label.setText(f"Latency: {latency:.1f} ms")
        self.confidence_label.setText(f"Confidence: {int(confidence*100)}%")
