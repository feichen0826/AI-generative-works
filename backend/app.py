# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import io
import base64
from image_utils import load_image, show_n, crop_center

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ai-generative-works.onrender.com"}})

hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def preprocess_image(image, image_size=(256, 256)):
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, image_size)
    image = image[tf.newaxis, :]
    return image

@app.route('/')
def home():
    return "Server is up and running!"

@app.route('/stylize', methods=['POST'])
def stylize_image():
    content_image = request.files['content_image']
    style_image = request.files['style_image']

    content_image = preprocess_image(np.array(Image.open(content_image)))
    style_image = preprocess_image(np.array(Image.open(style_image)))

    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0][0]

    image = tf.image.convert_image_dtype(stylized_image, dtype=tf.uint8)
    image = Image.fromarray(image.numpy())
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({'stylized_image': img_str})


if __name__ == '__main__':
    app.run(debug=True)
