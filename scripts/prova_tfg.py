import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
import json

try:
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
    parser.add_argument("--video_path", default="../../../examples/media/sosi.avi",
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


    nom_fitxer = "result_provatfg_amb_noms.json"
    kplist = []                                 # Llista de keypoints
    kpdict = {}                                 # Diccionari de keypoints
    numLinia = 1                                # Indica el número de la línia en que està al fitxer
    vegada = 0                                  # Indica la a quin punt del cos està
    nextFrame = False                           # Indica quan passa a un altre frame

    try:

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.VideoCapture(args[0].video_path)

        while(imageToProcess.isOpened()):
            ret, frame = imageToProcess.read()
            if ret == True:
                datum.cvInputData = frame
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))

                # Display Image
                kpdict['body keypoint'] = np.array(datum.poseKeypoints).tolist()
                kplist.append(kpdict.copy())
                print("Body keypoints: \n" + str(datum.poseKeypoints))
                cv2.imshow("OpenPose 1.7.0 - Tutorial Python API",
                           datum.cvOutputData)
                cv2.waitKey(1)

            else:
                break

    except Exception as e:
        print(e)
        sys.exit(-1)

    f = open(nom_fitxer, "w+")
    json.dump(kplist, f, indent=4)
    f.close()

    with open(nom_fitxer) as fp:
        linies = fp.read().splitlines()
    with open(nom_fitxer, "w") as fp:
        for linia in linies:

            if nextFrame:
                print(linia, file=fp)
                if numLinia == 10:
                    nextFrame = False
                    numLinia = 5
                    vegada = 0

                else:
                    numLinia += 1

            elif numLinia % 5 == 0:
                if vegada == 0:
                    print(linia + "\n" + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Nas",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 1:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Clatell",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 2:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Espatlla dreta",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 3:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Colze dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 4:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Canell dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 5:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Espatlla esquerra",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 6:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Colze esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 7:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Canell esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 8:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Cadera centre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 9:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Cadera banda dreta",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 10:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Genoll dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 11:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Turmell dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 12:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Cadera banda esquerra",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 13:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Genoll esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 14:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Turmell esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 15:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Ull dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 16:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Ull esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 17:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Orella dreta",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 18:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Orella esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 19:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Dit gros esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 20:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Dit petit esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 21:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Taló esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 22:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Dit gros dret",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 23:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Dit petit esquerre",', file=fp)
                    vegada += 1
                    numLinia += 1

                elif vegada == 24:
                    print(linia + "\n"  + "\t" + "\t" + "\t" + "\t"  + "\t" + '"Taló esquerre",', file=fp)
                    numLinia = 1
                    nextFrame = True

            else:
                print(linia, file=fp)
                numLinia += 1

    fp.close()

except Exception as e:
    print(e)
    sys.exit(-1)
