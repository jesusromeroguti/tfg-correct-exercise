import os
import sys
import flask
import pandas as pd
import numpy as np
from tensorflow import keras

# import importlib.util
# spec = importlib.util.spec_from_file_location("toCsv", "/home/aleix/openpose/build/examples/tutorial_api_python/prova_csv.py")
# script_csv = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(script_csv)

app = flask.Flask(__name__)
model_gb = None
model_no90 = None
model_pesEndavant = None
model_torsoInclinat = None
model_desnivellPeus = None

# El codi serveix per a saber que retorna i poder-ho comunicar al frontend.
# Codi[0] = good
# Codi[1] = no90
# Codi[2] = pesEndavant
# Codi[3] = torsoInclinat
# Codi[4] = desnivellPeus
codi = [0, 0, 0, 0, 0]

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
def convert_video():
    comanda = "python3 -y /home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/scripts/converter.py -v " + video_path
    os.system(comanda)

# Passa el video per OpenPose i retorna un csv amb els keypoints
def get_keypoints():
    os.system("python3 /home/aleix/openpose/build/examples/tutorial_api_python/csvAPI.py")

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
    if 1 in predictions:
        codi[1] = 0
    else:
        codi[1] = 1

def pesEndavant():
    predictions = model_pesEndavant.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no tira el pes endavant
    if 1 in predictions:
        codi[2] = 0
    else:
        codi[2] = 1

def torsoInclinat():
    predictions = model_torsoInclinat.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no inclina el tors
    if 1 in predictions:
        codi[3] = 0
    else:
        codi[3] = 1

def desnivellPeus():
    predictions = model_desnivellPeus.predict_classes(samples)
    # Si 1 a la predicció, llavors vol dir que no hi ha desnivell de peus
    if 1 in predictions:
        codi[4] = 0
    else:
        codi[4] = 1

def good_bad():
    # Fem el predict
    # Si result == 1:
    #   Retorna codi good
    # Si no:
    #   Retorna cridar models bad
    predictions = model_gb.predict_classes(samples)
    # Cas good
    if 1 in predictions:
        codi[0] = 1
    # Cas bad
    else:
        codi[0] = 0

@app.route("/predict", methods=["POST"])
def predict():
    global videofile
    global video_path
    videofile = flask.request.files['videofile']
    video_path = "/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/api/files/" + videofile.filename
    videofile.save(video_path)
    
    num = ""
    global codi
    codi = [0, 0, 0, 0, 0, 0]

    if not ".avi" in videofile:
        convert_video()

    get_keypoints()
    read_csv()
    
    # Cridem els models
    good_bad()
    no90()
    pesEndavant()
    torsoInclinat()
    desnivellPeus()

    os.system("rm -f ./files/*.avi ./files/*.mp4 ./files/*.csv")

    for i in range(len(codi)):
        num += str(codi[i])

    data = {"Codi": num }
    # classification = flask.jsonify(data)
    classification = data
    return flask.render_template('index.html', prediction=classification["Codi"])

@app.route("/", methods=["GET"])
def home_page():
    return flask.render_template('index.html')

if __name__ == "__main__":
    load_models()
    app.run(port=3000)
    
