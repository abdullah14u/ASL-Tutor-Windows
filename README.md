# ASL Tutor Pro

ASL Tutor Pro is a professional-grade American Sign Language (ASL) real-time interactive desktop tutor application designed for Windows 10/11.

## Features
- **Duolingo-Style UI/UX:** A highly polished, gamified learning path with sliding page transitions, bouncing micro-animations, and celebratory confetti pop-ups upon lesson completion.
- **Immersive Split-Screen Lessons:** Real-time MediaPipe skeletal overlay combined with dynamic hints to guide your hand positioning.
- **Machine Learning Engine:** Robust `scikit-learn` Support Vector Machine (SVM) for distance-invariant static gesture recognition and Dynamic Time Warping (DTW) for motion tracking.
- **Spaced-Repetition Curriculum:** A structured JSON-backed engine (`assets/curriculum.json`) that introduces new signs, tests them, and mixes in previously learned signs to reinforce memory.

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

## Developer Tools (Training Custom Models)
To guarantee near 100% accuracy, you can collect your own data and train a custom model:

1. **Collect Data:**
   Run the data collection tool to record 200 frames of your hand performing a specific sign.
   ```bash
   python tools/data_collector.py
   ```
   Follow the on-screen prompts to enter a label (e.g., "A", "HELLO") and press `r` to start recording. The data is saved to `dataset.csv`.

2. **Train Model:**
   Once you have collected enough data across different signs, train the SVM classifier:
   ```bash
   python tools/train_model.py
   ```
   This will output a `model.onnx` file. The main application (`main.py`) will automatically load this model if it exists in the root directory.

## Build Executable
To bundle the application into a standalone Windows `.exe`:
```bash
python build_exe.py
```
The resulting executable will be placed in the `dist/` directory.

## License
MIT License
