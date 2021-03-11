from pytube import YouTube, Stream

# Link del video que vols descarregar
yt = YouTube('https://www.youtube.com/watch?v=YaXPRqUwItQ&t=102s')

# Qualitat del video
video = yt.streams.first()

# Descarregar el video
print("Descarreguant video...")
video.download()
#video.download(/path/descarregar)

#Informació del video
print("##Informació del video##")
print("-------------------------")
print(yt.length)
print(yt.title)
print(yt.metadata)
  
