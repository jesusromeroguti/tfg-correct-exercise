import os
import sys
from sys import flags, platform
import cv2
import subprocess
import flask
import ffmpeg
import argparse
from flask.scaffold import F
import numpy as np
import csv
import datetime
from werkzeug.wrappers import request
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from tensorflow import keras
from pymediainfo import MediaInfo

# import importlib.util
# spec = importlib.util.spec_from_file_location("toCsv", "/home/aleix/openpose/build/examples/tutorial_api_python/prova_csv.py")
# script_csv = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(script_csv)

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model_gb = None
model_no90 = None
model_pesEndavant = None
model_torsoInclinat = None
model_desnivellPeus = None

res = []

def cutFps(frames):
    target = 0
    if frames > 75 and frames <= 150:
        target = 1
    elif frames > 150:
        target = 3
    return target

def normValues(arrayFrame, label):
    mitja_X = 0
    mitja_Y = 0
    # Arrays de coordenades
    v_x = []
    v_y = []
    pos = 0

    while(pos != len(arrayFrame)):
        v_x.append(arrayFrame[pos])
        pos += 1
        v_y.append(arrayFrame[pos])

        if pos == len(arrayFrame) - 1:
            pos = len(arrayFrame)
        else:
            pos += 2
    
    # Transformo les llistes en numpy arrays
    v_x = np.array(v_x)
    v_y = np.array(v_y)
 
    mitja_X = np.mean(v_x)
    mitja_Y = np.mean(v_y)

    dv_x = np.std(v_x)
    dv_y = np.std(v_y)

    dv = np.array([dv_x, dv_y])
    dv = np.mean(dv)

    norm_x = []
    norm_y = []

    for p in v_x:
        x = (p - mitja_X) / dv
        norm_x.append(x)

    for p in v_y:
        y = (p - mitja_Y) / dv
        norm_y.append(y)
    
    # Netejem l'array donada
    arrayFrame = [label]

    # Ajuntem x's i y's
    for i in range(len(norm_x)):
        arrayFrame.append(norm_x[i])
        arrayFrame.append(norm_y[i])

    return arrayFrame

def toCsv(file_path):
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release')
            os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + \
                '/../../x64/Release;' + dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/home/aleix/openpose/build/python')
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e
    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default=file_path,
                        help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/home/aleix/openpose/models/"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1:
            next_item = args[1][i+1]
        else:
            next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-', '')
            if key not in params:
                params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-', '')
            if key not in params:
                params[key] = next_item

    try:

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.VideoCapture(args[0].video_path)
        arrayNoNorm = np.array(0)
        totalFrames = int(imageToProcess.get(cv2.CAP_PROP_FRAME_COUNT))
        target = cutFps(totalFrames)
        counter = 0
        framesRet = 0

        # 1. Guardem totes les posicions del vídeo en una array.
        while(imageToProcess.isOpened()):
            if counter == target:
                ret, frame = imageToProcess.read()
                if ret == True:
                    datum.cvInputData = frame
                    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

                    # Display Image
                    kp_array = np.array(datum.poseKeypoints)
                    
                    # Treiem els outliers
                    nou_array = np.delete(kp_array[0], [3, 4, 15, 17, 22, 23], 0)
                    
                    arrayNoNorm = np.append(arrayNoNorm, nou_array)

                    # print("Body keypoints: \n" + str(datum.poseKeypoints))
                    # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API",
                    #     datum.cvOutputData)
                    cv2.waitKey(1)
                    counter = 0
                    framesRet += 1
                else:
                    break
            else:
                imageToProcess.grab()
                counter += 1
        
        label = file_path.split('/')[7]
        label = label.split('_')[0]
        label = label.split('.')[0]
        print(label)
        #label = label.join([c for c in label if c.isalpha()])
        pos = 0
        
        # print("Frames sencers: ",totalFrames)
        # print("Frames retallats: ", framesRet)
        for i in range(framesRet):
        	# 2. Normalitzem dades frame per frame (cada 75 posicions ja que te x, y i accuracy)
            posini = pos
            pos += 57
            arrayFrame = arrayNoNorm[posini:pos]
            # print(len(arrayFrame))
            # if len(arrayFrame) == 1:
            #     print(arrayFrame)
            arrayFrame = normValues(arrayFrame, label)
            
        	# 3. Les guardem en un csv
            with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/keypoints.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(arrayFrame)

        # Fem padding fins a 75, ja que és el màxim de frames.
        padding = [label]
        for i in range(38):
            padding.append(-1000.0)
        while(framesRet != 75):
            with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/keypoints.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(padding)
            framesRet += 1

    except Exception as e:
        print(e)
        sys.exit(-1)


def load_models():
   global model_gb
   global model_no90
   global model_pesEndavant
   global model_torsoInclinat
   global model_desnivellPeus
   
   model_gb = keras.models.load_model("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/models/model_layers5_96acc_reetiquetat.h5")
   model_no90 = keras.models.load_model("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/models/model_layers5_no90_test2_acc96.h5")
   model_pesEndavant = keras.models.load_model("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/models/model_layers5_pesEndavant_test2_acc100.h5")
   model_torsoInclinat = keras.models.load_model("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/models/model_layers5_torsoInclinat_test1_acc92.h5")
   model_desnivellPeus = keras.models.load_model("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/models/model_layers5_desnivellPeus_test1_acc100.h5")

# Fa la conversió a avi dels videos
def convert_video(video_path):
    name = video_path.split('.')[0] + ".avi"
    flags = "-i -y"
    subprocess.call(['ffmpeg', flags, video_path, name])
  

# Passa el video per OpenPose i retorna un csv amb els keypoints
def get_keypoints(filename):
    # os.system("python3 /home/aleix/openpose/build/examples/tutorial_api_python/csvAPI.py")
    fieldnames = ['Label',
              'NasX',
              'NasY',
              'ClatellX',
              'ClatellY',
              'Espatlla dretaX',
              'Espatlla dretaY',
              'Espatlla esquerraX',
              'Espatlla esquerraY',
              'Colze esquerreX',
              'Colze esquerreY',
              'Canell esquerreX',
              'Canell esquerreY',
              'Cadera centreX',
              'Cadera centreY',
              'Cadera banda dretaX',
              'Cadera banda dretaY',
              'Genoll dretX',
              'Genoll dretY',
              'Turmell dretX',
              'Turmell dretY',
              'Cadera banda esquerraX',
              'Cadera banda esquerraY',
              'Genoll esquerreX',
              'Genoll esquerreY',
              'Turmell esquerreX',
              'Turmell esquerreY',
              'Ull esquerreX',
              'Ull esquerreY',
              'Orella esquerreX',
              'Orella esquerreY',
              'Dit gros esquerreX',
              'Dit gros esquerreY',
              'Dit petit esquerreX',
              'Dit petit esquerreY',
              'Taló esquerreX',
              'Taló esquerreY',
              'Taló dretX',
              'Taló dretY']


    with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/keypoints.csv', mode='w') as file:
        file_writer = csv.DictWriter(file, fieldnames=fieldnames)
        file_writer.writeheader()

    directori = "/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/"
    # for file in os.listdir(directori):
    #     if file.endswith(".avi"):
    #         filename = file
    # toCsv("/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/" + filename)
    toCsv(filename)

def read_csv():
    path = '/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/keypoints.csv'
    final = pd.read_csv(path) 

    coords = final.drop(labels="Label", axis=1)

    coords = np.array(coords)

    global samples
    samples = []

    video = []
    index = 0
    for i in coords:
        # Cada 75 frames és un vídeo
        if index == 74:
            video.append(i)
            samples.append(video)
            video = []
            index = 0
        else:
            video.append(i)
            index += 1


    samples = np.array(samples)


def no90():
    # Si result == 1:
    #   Retonra codi si90
    # Si no:
    #   Retorna codi no90
    predictions = model_no90.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que si que es passen els 90 graus
    if 0 in predictions:
        res.append("no90")

def pesEndavant():
    predictions = model_pesEndavant.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no tira el pes endavant
    if 0 in predictions:
        res.append("pesEndavant")

def torsoInclinat():
    predictions = model_torsoInclinat.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no inclina el tors
    if 0 in predictions:
        res.append("torsoInclinat")

def desnivellPeus():
    predictions = model_desnivellPeus.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no hi ha desnivell de peus
    if 0 in predictions:
        res.append("desnivellPeus")

def good_bad():
    # Fem el predict
    # Si result == 1:
    #   Retorna codi good
    # Si no:
    #   Retorna cridar models bad
    predictions = model_gb.predict_classes(samples)
    # Cas good
    if 1 in predictions:
        res.append("good")
    # Cas bad
    else:
        res.append("bad")

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    global videofile
    global video_path

    #videofile = flask.request.data
    videofile = flask.request.files['videofile']

    video_path = "/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/" + videofile.filename
    videofile.save(video_path)

    global res
    res = []
    notVideo = True

    video_info = MediaInfo.parse(video_path)

    for track in video_info.tracks:
        if track.track_type == "Video":
            notVideo = False
    
    if notVideo:
        os.system("rm -f ./files/*")
        res.append("noVideo")

    else:
        
        data = cv2.VideoCapture(video_path)
  
        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(data.get(cv2.CAP_PROP_FPS))
        
        # calculate dusration of the video
        seconds = int(frames / fps)
        video_time = str(datetime.timedelta(seconds=seconds))
        if seconds > 5:
            res.append("errorDuracio")
            
        else:
            convert_video(video_path)
            get_keypoints(video_path)
            read_csv()
            
            # Cridem els models
            good_bad()
            no90()
            pesEndavant()
            torsoInclinat()
            desnivellPeus()

    os.system("rm -f ./files/*")        

    data = {"Resultat": res}
    print(data)
    return flask.jsonify(data)

if __name__ == "__main__":
    load_models()
    app.run(port=3000)
    
