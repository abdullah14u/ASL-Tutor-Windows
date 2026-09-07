import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import os

def train_model(dataset_path='dataset.csv', model_output_path='model.onnx'):
    print(f"Loading dataset from {dataset_path}...")
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found. Please run data_collector.py first.")
        return

    df = pd.read_csv(dataset_path)

    if df.empty:
        print("Error: Dataset is empty.")
        return

    # Assuming the first column is 'label' and the rest are features
    X = df.drop('label', axis=1)
    y = df['label']

    print(f"Dataset shape: {df.shape}")
    print(f"Classes: {y.unique()}")

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training SVM model...")
    # Initialize and train the SVM classifier
    # Using probability=True to get confidence scores later
    clf = SVC(kernel='rbf', probability=True, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the model
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Export the model using skl2onnx
    print(f"Exporting model to {model_output_path}...")

    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    # Define the initial types for the ONNX model based on input features (63 floats)
    initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]

    # Convert and save (removing zipmap: False so it outputs dictionaries of probabilities)
    onx = convert_sklearn(clf, initial_types=initial_type)
    with open(model_output_path, "wb") as f:
        f.write(onx.SerializeToString())

    print("Training complete.")

if __name__ == "__main__":
    train_model()
