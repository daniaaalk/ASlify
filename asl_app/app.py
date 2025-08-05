from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="asl_model.tflite")
interpreter.allocate_tensors()

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Classes A-Z
CLASSES = [chr(i) for i in range(65, 91)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img_bytes = file.read()
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (64, 64))
    img = np.expand_dims(img.astype(np.float32) / 255.0, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_idx = np.argmax(output_data)
    predicted_class = CLASSES[predicted_idx]

    return jsonify({'prediction': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
