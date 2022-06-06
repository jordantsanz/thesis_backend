# Name: Jordan Sanz
# Title: Drumming Notation Study main app
# Purpose: Holds the main app for the backend

import math
from flask import Flask, app, request
from flask_cors import CORS
from feat import Detector
import os
import numpy as np
from werkzeug.utils import secure_filename
import json

# configuration
UPLOAD_FOLDER = './videos'
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# import models
face_model = "faceboxes"
landmark_model = "mobilenet"
au_model = "rf"
emotion_model = "resmasknet"
detector = Detector(face_model = face_model, landmark_model = landmark_model, emotion_model = emotion_model)
print("LOADED AND LISTENING")

# constants
TESTING_AVERAGE = .44
IS_RENDER_COM = False
UPLOAD_FOLDER = './videos'

# create upload folder on deployed server
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


# default
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


# post route for video upload
@app.route('/video', methods=['POST'])
def read_video():

    # get video
    video = request.files['video']
    filename = secure_filename(video.filename)
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # create video prediction
    video_prediction = detector.detect_video(os.path.join(app.config['UPLOAD_FOLDER'], filename), skip_frames=98, verbose=True)

    # get emotion json
    emotions = {
    "happiness": video_prediction["happiness"].to_json(orient='values'),
    "anger": video_prediction["anger"].to_json(orient='values'), 
    "disgust": video_prediction["disgust"].to_json(orient='values'), 
    "fear": video_prediction["fear"].to_json(orient='values'),
    "sadness": video_prediction["sadness"].to_json(orient='values'),
    "surprise": video_prediction["surprise"].to_json(orient='values'),
    "neutral": video_prediction["neutral"].to_json(orient='values'),
    }

    # find means of each emotion
    anger = video_prediction["anger"].mean()
    sadness = video_prediction["sadness"].mean()
    fear = video_prediction["fear"].mean()
    disgust = video_prediction["disgust"].mean()
    happiness = video_prediction["happiness"].mean()
    neutral = video_prediction["neutral"].mean()
    surprise = video_prediction["surprise"].mean()

    # get means in json form with raw dataframe
    means = {
        "anger": np.float64(anger),
        "sadness": np.float64(sadness),
        "fear": np.float64(fear),
        "disgust": np.float64(disgust),
        "happiness": np.float64(happiness),
        "neutral": np.float64(neutral),
        "surprise": np.float64(surprise),
        "dataframe": emotions,
    }

    # return calculated versions back
    return json.dumps(means, indent = 4)



if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    app.run(host=HOST, port=PORT, debug=True)