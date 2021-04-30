import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import csv

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
            sys.path.append('../../python')
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
                    cv2.imshow("OpenPose 1.7.0 - Tutorial Python API",
                        datum.cvOutputData)
                    cv2.waitKey(1)
                    counter = 0
                    framesRet += 1
                else:
                    break
            else:
                imageToProcess.grab()
                counter += 1

        label = file_path.split('/')[8]
        label = label.split('_')
        labels = []
        for i in range(len(label)-1):
            labels.append(label[i])
        
        print(labels)
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
            arrayFrame = normValues(arrayFrame, labels)
            
        	# 3. Les guardem en un csv
            with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/dataset/train_baddataset1.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(arrayFrame)

        # Fem padding fins a 75, ja que és el màxim de frames.
        padding = [labels]
        for i in range(38):
            padding.append(-1000.0)
        while(framesRet != 75):
            with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/dataset/train_baddataset1.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(padding)
            framesRet += 1

    except Exception as e:
        print(e)
        sys.exit(-1)


fieldnames = ['Labels',
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


with open('/home/aleix/Escriptori/coses_tfg/tfg-correct-exercise/dataset/train_baddataset1.csv', mode='w') as file:
    file_writer = csv.DictWriter(file, fieldnames=fieldnames)
    file_writer.writeheader()


directori = "/home/aleix/Escriptori/coses_tfg/videos/esquat/baddataset/"

# toCsv("/home/aleix/Escriptori/coses_tfg/videos/esquat/no-openpose/front_bad1.avi")

numVideo = 0
numVideos = len(os.listdir(directori))
for file in os.listdir(directori):
   if file.endswith(".avi"):
       numVideo += 1
       print("Vídeo número " + str(numVideo) + " de " + str(numVideos))
       path = os.path.join(directori, file)
       toCsv(path)
