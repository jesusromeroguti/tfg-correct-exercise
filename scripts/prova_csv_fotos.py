import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import csv

def normValues(arrayFrame):
    mitja_X = 0
    mitja_Y = 0
    # Arrays de coordenades
    v_x = []
    v_y = []

    for i in range(len(arrayFrame[0])):
      v_x.append(arrayFrame[0][i][0])
      v_y.append(arrayFrame[0][i][1])
      
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
    arrayFrame = []

    # Ajuntem x's i y's
    for i in range(len(norm_x)):
        aux = []
        aux.append(norm_x[i])
        aux.append(norm_y[i])
        arrayFrame.append(aux)

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
            sys.path.append('../../python')
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e
    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default=file_path,
                        help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"

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
        imageToProcess = cv2.imread(args[0].image_path)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # Display Image
        kp_array = np.array(datum.poseKeypoints)

        # 1. Guardem totes les posicions del vídeo en una array.

        arrayFrame = normValues(kp_array)

        # print(arrayFrame)
        with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/dataset/train_dataset.csv', 'a') as file:
          writer = csv.writer(file)
          writer.writerow(arrayFrame)

    except Exception as e:
        print(e)
        sys.exit(-1)



fieldnames = ['Nas',
              'Clatell',
              'Espatlla dreta',
              'Colze dret',
              'Canell dret',
              'Espatlla esquerra',
              'Colze esquerre',
              'Canell esquerre',
              'Cadera centre',
              'Cadera banda dreta',
              'Genoll dret',
              'Turmell dret',
              'Cadera banda esquerra',
              'Genoll esquerre',
              'Turmell esquerre',
              'Ull dret',
              'Ull esquerre',
              'Orella dreta',
              'Orella esquerre',
              'Dit gros esquerre',
              'Dit petit esquerre',
              'Taló esquerre',
              'Dit gros dret',
              'Dit petit dret',
              'Taló dret']


with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/dataset/train_dataset.csv', mode='w') as file:
    file_writer = csv.DictWriter(file, fieldnames=fieldnames)
    file_writer.writeheader()


directori = "/home/aleix/Escriptori/coses_tfg/videos/esquat/no-openpose/"

toCsv('/home/aleix/Escriptori/coses_tfg/fotos/esquat/centrat.png')