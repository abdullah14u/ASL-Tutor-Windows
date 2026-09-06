import PyInstaller.__main__
import os

if __name__ == "__main__":
    app_name = "ASLTutorPro"
    main_script = "main.py"

    PyInstaller.__main__.run([
        main_script,
        '--name=%s' % app_name,
        '--windowed', # Don't open console on Windows
        '--onefile', # Package into a single executable
        '--clean',
        f'--add-data=assets{os.pathsep}assets', # Include assets folder
        # mediapipe requires its data files
        '--collect-data=mediapipe',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
    ])
