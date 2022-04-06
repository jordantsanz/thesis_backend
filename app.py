import math
from flask import Flask, app, request
from flask_cors import CORS
from feat import Detector
import os
from werkzeug.utils import secure_filename
import json
# Imports the Cloud Logging client library


TESTING_AVERAGE = .44
IS_RENDER_COM = True
if IS_RENDER_COM:
    UPLOAD_FOLDER = '/opt/render/project/src/videos'
else:
    UPLOAD_FOLDER = './videos'
    # import google.cloud.logging
    # import logging

    # # Instantiates a client
    # client = google.cloud.logging.Client()

    # # Retrieves a Cloud Logging handler based on the environment
    # # you're running in and integrates the handler with the
    # # Python logging module. By default this captures all logs
    # # at INFO level and higher
    # client.setup_logging()

app = Flask(__name__)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./jsanz-thesis-backend-3ff842a86ceb.json"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})
if not os.path.exists(UPLOAD_FOLDER):
    print('making upload folder')
    # logging.warning('having to make upload folder...')
    os.mkdir(UPLOAD_FOLDER)
logging.warning('current directory: ', os.listdir("."))

face_model = "retinaface"
landmark_model = "PFLD"
au_model = "rf"
emotion_model = "rf"
#logging.warning("Right before detector load")
detector = Detector(face_model = face_model, landmark_model = landmark_model, au_model = au_model, emotion_model = emotion_model)
#logging.warning('LOADED. READY TO LISTEN.')

@app.route("/video", methods=['POST'])
def read_video():
    print("read video path hit")
    #logging.warning('READ VIDEO PATH HIT')
    video = request.files['video']
    #logging.warning('video gotten', video)
    filename = secure_filename(video.filename)
    print(filename, 'filename')
    print('directory: ', os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('after write to os')
    print('current directory: ', os.path.curdir)

    video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("file exists?", os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

    video_prediction = detector.detect_video(os.path.join(app.config['UPLOAD_FOLDER'], filename), skip_frames=500)
    print("after video prediction")
    # print('emotions: ', video_prediction.emotions())
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

    # anger = video_prediction["anger"].mean()
    # sadness = video_prediction["sadness"].mean()
    # fear = video_prediction["fear"].mean()
    # disgust = video_prediction["disgust"].mean()

    # emotions = {"anger": anger, "sadness": sadness, "fear": fear, "disgust": disgust}
    
    # return json.dumps(emotions, indent = 4)
    return 'hello'

@app.route('/')
def index():
    #logging.warning('in index route')
    return "<h1>Welcome to our server !!</h1>"

@app.route('/test', methods=['POST'])
def test_routes():
    #logging.warning('test')
    print('request: ', request)
    return "success"

@app.errorhandler(Exception)
def error_handler(error):
    #logging.warning(error)
    print(error)
    return "!!!!" + repr(error)


if __name__ == "__main__":
    app.run(port=int(os.getenv('PORT')), debug=True)
