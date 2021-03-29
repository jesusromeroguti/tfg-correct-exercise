import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import csv

def normValues(arrayFrame):
	# mitja_X = 0
 #    mitja_Y  = 0
 #  	# Arrays de coordenades
 #  	v_x = []
 #  	v_y = []

	# for p in data:
	#   v_x.append(p[1])
	#   v_y.append(p[2])

	# # Transformo les llistes en numpy arrays
	# v_x = np.array(v_x)
	# v_y = np.array(v_y)

	# mitja_X = np.mean(v_x)
	# mitja_Y = np.mean(v_y)

	# dv_x = np.std(v_x)
	# dv_y = np.std(v_y)

	# dv = np.array([dv_x, dv_y])
	# dv = np.mean(dv)

	# norm_x = []
	# norm_y = []

	# for p in v_x:
	#   x = (p - mitja_X) / dv 
	#   norm_x.append(x)

	# for p in v_y:
	#   y = (p - mitja_Y) / dv 
	#   norm_y.append(y)
	
	return arrayFrame


def toCsv(file_path):
	 # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default=file_path,
        help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()
    
    try:

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.VideoCapture(args[0].video_path)
        totalFrames = 0


        # 1. Guardem totes les posicions del vídeo en una array.
        while(imageToProcess.isOpened()):
        	ret, frame = imageToProcess.read()
            if ret == True:
            	datum.cvInputData = frame
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))

                totalFrames += 1

                # Display Image
                kp_array = np.array(datum.poseKeypoints)
                arrayNoNorm = np.append(arrayNoNorm, kp_array)

                # print("Body keypoints: \n" + str(datum.poseKeypoints))
                cv2.imshow("OpenPose 1.7.0 - Tutorial Python API",
                	datum.cvOutputData)
                cv2.waitKey(1)

            else:
            	break

        pos = 0
        for i in range(totalFrames):
        	# 2. Normalitzem dades frame per frame (cada 25 posicions)
        	pos += 25
        	arrayFrame = array[:pos]
        	arrayFrame = normValues(arrayFrame)
        
        	# 3. Les guardem en un csv
        	with open('/home/aleix/Escriptori/coses_tfg/training/train_dataset.csv', 'w', newline='') as file:
        		writer = csv.writer(file)
        		writer.writerows(arrayFrame)


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


with open('/home/aleix/Escriptori/coses_tfg/training/train_dataset.csv', mode='w') as file:
    file_writer = csv.DictWriter(file, fieldnames=fieldnames)
    file_writer.writeheader()


directori = "/home/aleix/Escriptori/coses_tfg/videos/esquat/no-openpose/"

for file in os.listdir(directori):
    if file.endswith(".avi"):
        path=os.path.join(directori, file)
        toCsv(path)