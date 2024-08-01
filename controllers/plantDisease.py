import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from flask_restful import Resource
from flask import request, jsonify
import base64
import io
from PIL import Image
import os
print("Current working directory:", os.getcwd())


base_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(base_dir, 'model.h5')
model = load_model(filepath)
print("Model Loaded Successfully")

# Map of prediction indices to disease types
disease_classes = [
    "Tomato - Bacterial Spot Disease",
    "Tomato - Early Blight Disease",
    "Tomato - Healthy and Fresh",
    "Tomato - Late Blight Disease",
    "Tomato - Leaf Mold Disease",
    "Tomato - Septoria Leaf Spot Disease",
    "Tomato - Target Spot Disease",
    "Tomato - Tomato Yellow Leaf Curl Virus Disease",
    "Tomato - Tomato Mosaic Virus Disease",
    "Tomato - Two Spotted Spider Mite Disease"
]

class PlantDisease(Resource):
    def post(self):
        try:
            # Get the image data from the JSON request
            image_data = request.json.get("image_data")
            
            # Decode the base64 string to an image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Convert the image to an OpenCV format
            tomato_plant = np.array(image)
            test_image = cv2.resize(tomato_plant, (128, 128))  # Resize image

            # Preprocess the image
            test_image = img_to_array(test_image) / 255  # Normalize the image
            test_image = np.expand_dims(test_image, axis=0)  # 3D to 4D

            # Predict the result
            result = model.predict(test_image)
            pred = np.argmax(result, axis=1).item()

            # Get the disease name
            disease = disease_classes[pred]

            # Return the prediction and disease type
            return jsonify({"success": True, "prediction": pred, "disease": disease})
        
        except Exception as error:
            print("Error processing request:", error)
            return jsonify({"success": False, "message": "Internal Server Error"}), 500
