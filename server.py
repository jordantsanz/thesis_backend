from flask import Flask, request
from flask_cors import CORS
from feat import Detector
from feat.utils import read_feat
import pandas as pd
import os
import cv2
from feat.tests.utils import get_test_data_path
from werkzeug.utils import secure_filename
import os, glob

UPLOAD_FOLDER = './videos'
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/video", methods=['POST'])
def read_video():
    video = request.files['video']
    filename = secure_filename(video.filename)
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    face_model = "retinaface"
    landmark_model = "mobilenet"
    au_model = "rf"
    emotion_model = "resmasknet"
    detector = Detector(face_model = face_model, landmark_model = landmark_model, au_model = au_model, emotion_model = emotion_model)
    print(filename)
    video_prediction = detector.detect_video("./videos/" + filename, skip_frames=24)
    print(video_prediction.emotions())
    # emotions = {
    # "happiness": video_prediction["happiness"],
    # "anger": video_prediction["anger"], 
    # "disgust": video_prediction["disgust"], 
    # "fear": video_prediction["fear"], 
    # "sadness": video_prediction["sadness"],
    # "surprise": video_prediction["surprise"],
    # "neutral": video_prediction["neutral"]
    # }
    # print(emotions)
    return video_prediction.emotions().to_json()
    

if __name__ == "__main__":
    app.run(debug=True)