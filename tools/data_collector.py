import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import time
import sys

# Add project root to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml_engine.preprocessing import normalize_landmarks

class DataCollector:
    def __init__(self, output_file='dataset.csv'):
        self.output_file = output_file
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.is_recording = False
        self.current_label = ""
        self.frames_recorded = 0
        self.target_frames = 200

        # Initialize dataset file with headers if it doesn't exist
        if not os.path.exists(self.output_file):
            columns = ['label'] + [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]
            pd.DataFrame(columns=columns).to_csv(self.output_file, index=False)

    def run(self):
        cap = cv2.VideoCapture(0)

        print("Data Collector Mode")
        print("Press 'r' to start recording 200 frames.")
        print("Press 'q' to quit.")
        print("-------------------")

        self.current_label = input("Enter label to record (e.g., A, B, Hello): ").strip().upper()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Draw UI
            cv2.putText(frame, f"Label: {self.current_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if self.is_recording:
                cv2.putText(frame, f"Recording: {self.frames_recorded}/{self.target_frames}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Press 'r' to record", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if self.is_recording:
                    raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                    normalized_features = normalize_landmarks(raw_landmarks)

                    # Append to dataset
                    row = [self.current_label] + normalized_features.tolist()
                    pd.DataFrame([row]).to_csv(self.output_file, mode='a', header=False, index=False)

                    self.frames_recorded += 1
                    if self.frames_recorded >= self.target_frames:
                        self.is_recording = False
                        print(f"\nFinished recording {self.target_frames} frames for {self.current_label}.")

                        # Prompt for next label
                        new_label = input("Enter next label to record (or press enter to keep current, 'q' to quit): ").strip().upper()
                        if new_label.lower() == 'q':
                            break
                        elif new_label:
                            self.current_label = new_label

            cv2.imshow('Data Collector', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r') and not self.is_recording:
                self.is_recording = True
                self.frames_recorded = 0
                print(f"Recording started for {self.current_label}...")

        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()

if __name__ == "__main__":
    collector = DataCollector()
    collector.run()
