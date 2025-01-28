from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load the model when the application starts
model = load_model('plant_disease_model.keras')

# Class names dictionary
dic_class_names = {
    "0": "Apple___Apple_scab",
    "1": "Apple___Black_rot",
    "2": "Apple___Cedar_apple_rust",
    "3": "Apple___healthy",
    "4": "Blueberry___healthy",
    "5": "Cherry_(including_sour)___healthy",
    "6": "Cherry_(including_sour)___Powdery_mildew",
    "7": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "8": "Corn_(maize)___Common_rust_",
    "9": "Corn_(maize)___healthy",
    "10": "Corn_(maize)___Northern_Leaf_Blight",
    "11": "Grape___Black_rot",
    "12": "Grape___Esca_(Black_Measles)",
    "13": "Grape___healthy",
    "14": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "15": "Orange___Haunglongbing_(Citrus_greening)",
    "16": "Peach___Bacterial_spot",
    "17": "Peach___healthy",
    "18": "Pepper,_bell___Bacterial_spot",
    "19": "Pepper,_bell___healthy",
    "20": "Potato___Early_blight",
    "21": "Potato___healthy",
    "22": "Potato___Late_blight",
    "23": "Raspberry___healthy",
    "24": "Soybean___healthy",
    "25": "Squash___Powdery_mildew",
    "26": "Strawberry___healthy",
    "27": "Strawberry___Leaf_scorch",
    "28": "Tomato___Bacterial_spot",
    "29": "Tomato___Early_blight",
    "30": "Tomato___healthy",
    "31": "Tomato___Late_blight",
    "32": "Tomato___Leaf_Mold",
    "33": "Tomato___Septoria_leaf_spot",
    "34": "Tomato___Spider_mites Two-spotted_spider_mite",
    "35": "Tomato___Target_Spot",
    "36": "Tomato___Tomato_mosaic_virus",
    "37": "Tomato___Tomato_Yellow_Leaf_Curl_Virus"
}

def prepare_image(img_path, target_size):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'result': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'result': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img_array = prepare_image(file_path, target_size=(224, 224))  # Adjust target_size to match your model input
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_disease = dic_class_names[str(predicted_class)]

        return jsonify({'result': predicted_disease})

    return jsonify({'result': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)
