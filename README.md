# ASL Tutor Pro

ASL Tutor Pro is a professional-grade American Sign Language (ASL) real-time interactive desktop tutor application designed for Windows 10/11.

## Features
- **Real-Time Tracking & Skeletal Overlay:** Smooth, jitter-free hand tracking via MediaPipe and OpenCV, enhanced with an Exponential Moving Average (EMA) filter.
- **Gesture Recognition Engine:** A deterministic geometric classifier that analyzes finger curls and relative positions to identify ASL letters and numbers.
- **Gamified Curriculum:** Structured learning tiers (Level 1 to Level 3) with a Hold-to-Score mechanism requiring a 1.5-second hold. Includes scoring and combo streaks.
- **Professional Windows UI:** A sleek, Fluent-inspired dark theme using PySide6. Split-panel design showing live tracking and active prompts with diagnostic overlays (FPS, Latency).

## Architecture
The application uses a multi-threaded producer-consumer pattern. A background `QThread` captures video and runs inference using MediaPipe, emitting signals (processed frames and landmarks) to the main GUI thread. This guarantees an uninterrupted UI experience.

## Setup & Execution

### Prerequisites
- Python 3.10+
- A working webcam

### Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Execute the main application script:
```bash
python main.py
```

## Build Executable
To bundle the application into a standalone Windows `.exe`:
```bash
python build_exe.py
```
The resulting executable will be placed in the `dist/` directory.

## License
MIT License
