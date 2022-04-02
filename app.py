import math
from flask import Flask, app, request
from flask_cors import CORS
from feat import Detector
from feat.utils import read_feat
from google.cloud import storage
import pandas as pd
import os
from feat.tests.utils import get_test_data_path
from werkzeug.utils import secure_filename
import json

TESTING_AVERAGE = .44

UPLOAD_FOLDER = 'videos'
app = Flask(__name__)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./jsanz-thesis-backend-3ff842a86ceb.json"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})
if not os.path.exists('videos'):
    os.mkdir('videos')
print('current directory: ', os.listdir("."))

face_model = "retinaface"
landmark_model = "PFLD"
au_model = "rf"
emotion_model = "rf"
detector = Detector(face_model = face_model, landmark_model = landmark_model, au_model = au_model, emotion_model = emotion_model)

@app.route("/video", methods=['POST'])
def read_video():
    video = request.files['video']
    print('video gotten', video)
    filename = secure_filename(video.filename)
    print(filename, 'filename')
    print('directory: ', os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('after write to os')
    print('current directory: ', os.path.curdir)

    video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("file exists?", os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

    video_prediction = detector.detect_video(os.path.join(app.config['UPLOAD_FOLDER'], filename), skip_frames=24)
    print('emotions: ', video_prediction.emotions())
    emotions = {
    "happiness": video_prediction["happiness"],
    "anger": video_prediction["anger"], 
    "disgust": video_prediction["disgust"], 
    "fear": video_prediction["fear"], 
    "sadness": video_prediction["sadness"],
    "surprise": video_prediction["surprise"],
    "neutral": video_prediction["neutral"]
    }
    print(emotions)

    anger = video_prediction["anger"].mean()
    sadness = video_prediction["sadness"].mean()
    fear = video_prediction["fear"].mean()
    disgust = video_prediction["disgust"].mean()

    emotions = {"anger": anger, "sadness": sadness, "fear": fear, "disgust": disgust}
    
    return json.dumps(emotions, indent = 4)

@app.route('/')
def index():
    print('in index route')
    return "<h1>Welcome to our server !!</h1>"

@app.route('/test', methods=['POST'])
def test_routes():
    print('test')
    print('request: ', request)
    return "success"

@app.errorhandler(Exception)
def error_handler(error):
    print(error)
    return "!!!!" + repr(error)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
