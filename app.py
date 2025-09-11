from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Resizing, Conv2D, MaxPooling2D, Flatten, Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import numpy as np
from PIL import Image

# Define a model that accepts any input size
def create_model():
    model = Sequential([
        Input(shape=(None, None, 3)),  # Accept any height and width, with 3 color channels
        Resizing(128, 128),  # Dynamically resize images to 128x128
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        GlobalAveragePooling2D(),  # Pool across spatial dimensions (flexible to input size)
        Dense(128, activation='relu'),
        Dense(3, activation='linear')  # Outputs height, weight, chest
    ])
    return model

# Create and compile the model
model = create_model()
model.compile(optimizer=Adam(), loss=MeanSquaredError(), metrics=['mae'])

print("Model created and compiled successfully!")

# Flask app
app = Flask(__name__)

# Save the model
model.save("custom_body_scanner_model.h5")

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# AI Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Process the uploaded image
        img = Image.open(file).convert('RGB')
        img_array = np.array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict using the model
        predictions = model.predict(img_array)
        height, weight, chest = predictions[0]
        return jsonify({
            "height": float(height),
            "weight": float(weight),
            "chest": float(chest)
        })
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
