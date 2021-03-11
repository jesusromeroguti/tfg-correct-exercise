from pytube import YouTube, Stream
from datetime import datetime

import subprocess
import sys
import os

try:
	data = datetime.now().strftime("%d%m%Y_%H%M%S") # La data serà el títol del vídeo

	link = str(sys.argv)

	# Link del video que vols descarregar
	yt = YouTube(link)

	# Qualitat del video
	video = yt.streams.first()

	# Descarregar el video
	print("Descarregant video...")
	video.download(filename=data)
	# video.download(/path/descarregar)

	# Informació del video
	print("##Informació del video##")
	print("-------------------------")
	print(yt.length)
	print(yt.title)
	print(yt.metadata)

	# Convertim el vídeo a .avi
	print("Convertint a .avi...")
	comanda = "python3 converter.py -v " + data + ".mp4"
	os.system(comanda)

except:
	print("Alguna cosa ha anat malament. Recorda posar el link tot seguit de la comanda i que aquest sigui correcte.")
