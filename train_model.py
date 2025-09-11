import os
import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

# Step 1: Load Images
image_folder = "images"  # Ensure your images folder is named 'images' and contains the images from the dataset
images = []
data = pd.read_csv("custom_anthropometric_dataset.csv")  # Load the custom dataset
for img_name in data["Image"]:  # Use the 'Image' column from the dataset
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)  # Read the image
    if img is not None:
        img = cv2.resize(img, (128, 128))  # Resize it to 128x128 pixels
        images.append(img)
    else:
        print(f"Warning: {img_name} not found!")

images = np.array(images) / 255.0  # Normalize the images

# Step 2: Load Measurements
measurements = data[["Height (cm)", "Weight (kg)", "Chest (cm)"]].to_numpy()  # Extract relevant columns and convert to numpy array

# Step 3: Split Data
X_train, X_test, y_train, y_test = train_test_split(images, measurements, test_size=0.2, random_state=42)

# Step 4: Build a Simple Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(y_train.shape[1], activation='linear')  # Output dimensions (Height, Weight, Chest)
])

# Step 5: Compile and Train the Model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.fit(X_train, y_train, epochs=5, batch_size=2)

# Step 6: Save the Model
model.save("custom_body_scanner_model.h5")  # Save with a unique name
print("Model saved successfully!")
