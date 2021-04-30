import cv2
import os
import sys

sys.stdout = open("duracio_videos.txt", "w")
directori = "/home/aleix/Escriptori/coses_tfg/videos/esquat/no-openpose/"

maxFr = 0
minFr = 200

for file in os.listdir(directori):
    if file.endswith(".avi"):
        cutFr = 0

        path = os.path.join(directori, file)
        cap = cv2.VideoCapture(path)
        # cv2.waitKey(100)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        seconds = int(frames / fps)

        if minFr > frames:
        	minFr = frames

        if maxFr < frames:
        	maxFr = frames

        if frames <= 75:
            target = 0
        elif frames > 75 and frames <= 150:
            target = 1
        elif frames > 150:
            target = 3
        
        counter = 0
        ret = True
        while(ret):
            if counter == target:
                ret, frame = cap.read()
                if ret == True:
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(10)

                counter = 0
                cutFr += 1
            else:
                ret = cap.grab()
                counter += 1
        	
        print("---------------------------------------")
        print("Vídeo: ", file)
        print("Frames originals: ", frames)
        print("FPS: ", fps)
        print("Temps: ", seconds)
        print("Frames resultants: ", cutFr)

print("---------------------------------------")
print("Vídeo amb menys frames: ", minFr)
print("Vídeo amb més frames: ", maxFr)

sys.stdout.close()
