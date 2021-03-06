#!/usr/bin/env python
import numpy as np
from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array, array_to_img
from PIL import Image


MODEL_PATH = './results/models/model.13-0.79.h5'
IMAGE_SIZE = (224, 224)
MEAN = 51.43062
STD = 44.75102
LABEL_DICT = {0:'Bone Fracture Negative', 1:'Bone Fracture Positive'}

model = load_model(MODEL_PATH)
app = Flask(__name__)


def preprocess(file_path):
	img = load_img(file_path, color_mode='grayscale', target_size=IMAGE_SIZE)
	img = img_to_array(img)
	img = np.asarray(img).astype('float32')
	img = np.squeeze(img, axis=-1)
	img = np.repeat(img[..., np.newaxis], 3, -1)
	img = img[np.newaxis, ...]
	img = (img - MEAN) / STD

	return img


def decode_label(y_pred):
	return 1 if y_pred > 0.5 else 0


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route("/predict", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
	    # Get the file from post request
	    f = request.files['file']

	    # Save the file to ./uploads
	    basepath = os.path.dirname(__file__)
	    file_path = os.path.join(
	        basepath, 'uploads', secure_filename(f.filename))
	    f.save(file_path)

	    img = preprocess(file_path)
	    # Make prediction
	    y_pred = model.predict(img)
	    label = decode_label(y_pred[0][0])
	    result = LABEL_DICT[label]

	    return result
    return None


if __name__ == '__main__':
	app.run(debug=True)
