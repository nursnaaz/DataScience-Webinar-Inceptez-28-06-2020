from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

#Image utils
from tensorflow import keras
import cv2


# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model'

# Load your trained model
model = keras.models.load_model(MODEL_PATH)
print('Model loaded. Start serving...')

# Check https://keras.io/applications/
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image_con = image.reshape((1,224, 224,3))
    image_con = np.array(image_con) / 255.0
    predIdxs = model.predict(image_con)
    # for each image in the testing set we need to find the index of the
    # label with corresponding largest predicted probability
    predIdxs = np.argmax(predIdxs, axis=1)
    kv = {0:"Covid Positive",1:"Covid Negative"}
    l = dict((k,v) for k,v in kv.items())
    prednames = l[predIdxs[0]]
    print(prednames) 
    return prednames


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        model = keras.models.load_model("models/model")
        prednames = model_predict(file_path, model )
        return prednames
    return None


if __name__ == '__main__':
    app.run( debug = True, threaded = True)

    # Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()