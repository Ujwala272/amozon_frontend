from transformers import pipeline

# Create an object detection pipeline
object_detection = pipeline("object-detection", model="ciasimbaya/ObjectDetection")

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

def allowed_file(filename):
    # Check if the file extension is allowed
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
@app.route("/",methods=["GET"])
def hello():
    return jsonify({"message": "hellowordl"})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Check if the POST request has the file part
        if 'image' not in request.files:
            raise ValueError('No image file in the request')

        file = request.files['image']

        # Check if the file is empty
        if file.filename == '':
            raise ValueError('No selected file')

        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            raise ValueError('Invalid file extension')

        # Generate a unique filename using the current timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}.{'.'.join(file.filename.split('.')[1:])}"

        # Save the file to the current working directory
        file.save(filename)
        results = object_detection(filename)

        response_result = {
            'label': results[0]['label'],
            'confidence': results[0]['score'],
            'bbox': results[0]['box']
        }
        return jsonify(response_result)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }

        return jsonify(response)

if __name__ == '__main__':
    app.run()