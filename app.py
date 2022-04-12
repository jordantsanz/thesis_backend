# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import math
from flask import Flask, app, request
from flask_cors import CORS
from feat import Detector
import os
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = './videos'
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})

face_model = "retinaface"
landmark_model = "mobilenet"
au_model = "rf"
emotion_model = "resmasknet"
#logging.warning("Right before detector load")
detector = Detector(face_model = face_model, landmark_model = landmark_model, au_model = au_model, emotion_model = emotion_model)
#logging.warning('LOADED. READY TO LISTEN.')
print("LOADED AND LISTENING")

TESTING_AVERAGE = .44
IS_RENDER_COM = False
if IS_RENDER_COM:
    UPLOAD_FOLDER = '/opt/render/project/src/videos'
else:
    UPLOAD_FOLDER = './videos'

if not os.path.exists(UPLOAD_FOLDER):
    print('making upload folder')
    # logging.warning('having to make upload folder...')
    os.mkdir(UPLOAD_FOLDER)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/video', methods=['POST'])
def read_video():
    print("read video path hit")
    video = request.files['video']
    filename = secure_filename(video.filename)
    print(filename, 'filename')
    print('directory: ', os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('after write to os')
    print('current directory: ', os.path.curdir)

    video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("file exists?", os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    video_prediction = detector.detect_video(os.path.join(app.config['UPLOAD_FOLDER'], filename), skip_frames=96)
    print("after video prediction")
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



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    HOST = '0.0.0.0'
    PORT = 8080
    app.run(host=HOST, port=PORT, debug=True)
# [END gae_flex_quickstart]