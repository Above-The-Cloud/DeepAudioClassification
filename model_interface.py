from subprocess import Popen, PIPE, STDOUT
import random
import string
import os
import sys
import numpy as np
import pickle
from random import shuffle
from imageFilesTools import getImageData
from model import createModel
import numpy as np
import eyed3

from PIL import Image
from model import createModel
from audioFilesTools import isMono, getGenre
#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 
pixelPerSecond = 50  #每秒50像素
desiredSize = 128
sliceSize = 128  #每个图片段像素大小

piece=20


genres = ['R&B', '中国风', '古典', '摇滚', '民谣', '爵士', '说唱']
genres = [filename for filename in genres if os.path.isdir('Data/Slices/'+filename)]
print(genres)

def predict(filename):
	print("predict...", filename)
	command = "rm -rf ./single"
	shell_runner(command)
	command = "mkdir single"
	shell_runner(command)
	command = "cp "+filename+" single/"
	print(command)
	shell_runner(command)
	name = os.listdir("./single")[0]
	command = "mkdir single/dan"
	shell_runner(command)
	AudioToSlices(name)
	createPreDatasetFromSlices(name)
	#Create model 
	model = createModel(7, sliceSize)
	test_X = pickle.load(open("single/p/"+name.replace(".mp3",".p"), "rb" ))
	model.load('musicDNN.tflearn')
	res_y = model.predict_label(test_X)
	print(res_y)
	counter=[0 for i in range(7)]
	for row in res_y:
		counter[row[0]]+=1
	res=(np.array(counter)).argmax()
	print(res)
	command = "rm -rf ./single"
	#shell_runner(command)
	return genres[res]



def shell_runner(command):
	output, errors="",""
	try:
		p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
		output, errors = p.communicate()
	except:
		print("cmd:",command)
		if errors:
			print (errors)


def AudioToSlices(audiofilename):
	newFilename = audiofilename.replace(".mp3", "")+"_dan"
	if isMono("single/" + audiofilename):
		command = "cp 'single/{}' 'single/{}.mp3'".format(audiofilename,newFilename)
	else:
		command = "sox 'single/{}' 'single/{}.mp3' remix 1,2".format(audiofilename,newFilename)#转成单声道
	shell_runner(command)
	command = "sox 'single/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o 'single/{}.png'".format(newFilename,pixelPerSecond,newFilename)
	shell_runner(command)	
	
	png2slices(newFilename)

def png2slices(picfilename):
	# sliceSpectrogram(filename, desiredSize)
	img = Image.open("single/"+picfilename + '.png')
	width, height = img.size
	nbSamples = int(width/desiredSize)

	for i in range(nbSamples):
		#print ("Creating slice: ", (i+1), "/", nbSamples, "for", picfilename)
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save("single/dan/"+"{}_{}.png".format(picfilename, i))
	# pangs=os.listdir("single/dan")
	# num =len(pangs)
	# save_png=[j*(num//piece) for j in range(piece)]
	# for f in pangs:
	# 	num = int((f.split("_")[-1]).split(".")[0])
	# 	if num in save_png:
	# 		continue;
	# 	os.remove("single/dan/"+f)


def createPreDatasetFromSlices(songname):
    data = []
    filenames = os.listdir("single/dan/")
    filenames = [filename for filename in filenames if filename.endswith('.png')]
    #Randomize file selection for this genre
    shuffle(filenames)

    #Add data (X,y)
    for filename in filenames:
        imgData = getImageData("single/dan/"+"/"+filename, sliceSize)
        label = [0,0,0,0,0,0,0]
        data.append((imgData,label))


    #Shuffle data
    shuffle(data)

    X,y = zip(*data)

    #Prepare for Tflearn at the same time
    train_X = np.array(X[:]).reshape([-1, sliceSize, sliceSize, 1])

    
    print("    DataPreset created! ✅")
        
    #Save
    saveDataPreset(train_X,songname)

    
def saveDataPreset(train_X,songname):
     #Create path for dataset if not existing
    if not os.path.exists(os.path.dirname("single/p/")):
        try:
            os.makedirs(os.path.dirname("single/p/"))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    print("[+] Saving Predataset... ")
    pickle.dump(train_X, open("{}/{}.p".format("single/p/",songname.replace(".mp3","")), "wb" ))
    print("    DataPreset saved! ✅💾")


if __name__=="__main__":
	print(predict("/Users/vector/Desktop/DeepAudioClassification/Data/RAW/林俊杰-醉赤壁.mp3"))

