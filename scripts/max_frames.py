import cv2
import os
import sys

sys.stdout = open("duracio_videos.txt", "w")
directori = "/home/aleix/Escriptori/coses_tfg/videos/esquat/no-openpose/"

maxFr = 0
minFr = 200

for file in os.listdir(directori):
    if file.endswith(".avi"):
        path = os.path.join(directori, file)
        cap = cv2.VideoCapture(path)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        seconds = int(frames / fps)
        
        if minFr > frames:
        	minFr = frames
        
        if maxFr < frames:
        	maxFr = frames

        print("---------------------------------------")
        print("Vídeo: ", file)
        print("Frames: ", frames)
        print("FPS: ", fps)
        print("Temps: ", seconds)

print("---------------------------------------")
print("Vídeo amb menys frames: ", minFr)
print("Vídeo amb més frames: ", maxFr)

sys.stdout.close()