import os
import cv2
import numpy as np
from keras.models import load_model
from keras.losses import MeanSquaredError  # Import mse explicitly

# Define custom objects
custom_objects = {"mse": MeanSquaredError()}  # Register Mean Squared Error loss function

# Load the saved model
model_path = "custom_body_scanner_model.h5"
try:
    model = load_model(model_path, custom_objects=custom_objects)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading the model:", e)
    exit()

# Load a test image
test_image_path = "images/person1.jpg"  # Replace with the path to your test image
try:
    if os.path.exists(test_image_path):
        test_image = cv2.imread(test_image_path)
        test_image = cv2.resize(test_image, (128, 128)) / 255.0  # Resize and normalize
        test_image = np.expand_dims(test_image, axis=0)  # Add batch dimension
        print("Test image loaded successfully!")
    else:
        raise FileNotFoundError(f"Test image '{test_image_path}' not found!")
except Exception as e:
    print("Error loading the test image:", e)
    exit()

# Predict measurements
try:
    predictions = model.predict(test_image)
    print("Predicted Measurements (Height, Weight, Chest):", predictions[0])
except Exception as e:
    print("Error during prediction:", e)
