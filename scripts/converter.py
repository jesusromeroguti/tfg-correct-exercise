'''
Script per a convertir qualsevol format de video a avi
'''
import argparse
import os 
import sys
import subprocess


def convertVideo(path):
    name = path.split('.')[0] + ".avi"
    print(name)
    subprocess.call(['ffmpeg', '-i', path, name])     

def convertDirectory(path):
    for root, dirs, filenames in os.walk(path, topdown=False):
        for file in filenames:
            input = root + "/" + file
            ouput = root + "/" + file.split('.')[0] + ".avi"
            subprocess.call(['ffmpeg', '-i', input, ouput])     

parser = argparse.ArgumentParser(description='Script per convertir videos a format avi')

parser.add_argument('-v', '--video', type=convertVideo, default=None)
parser.add_argument('-d', '--directory', type=convertDirectory, default=None)

options = parser.parse_args()
