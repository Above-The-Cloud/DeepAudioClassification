# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3

from sliceSpectrogram import createSlicesFromSpectrograms
from audioFilesTools import isMono, getGenre
from config import rawDataPath,rawPrePath
from config import spectrogramsPath
from config import pixelPerSecond
from config import slicesPrePath

#Tweakable parameters
desiredSize = 128

piece=60
#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(filename,newFilename):
	#Create temporary mono track if needed
	if isMono(rawDataPath+filename):
		command = "cp '{}' './tmp/{}.mp3'".format(rawDataPath+filename,newFilename)
	else:
		command = "sox '{}' './tmp/{}.mp3' remix 1,2".format(rawDataPath+filename,newFilename)
	print(command)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	#Create spectrogram
	filename.replace(".mp3","")
	command = "sudo sox './tmp/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(newFilename,pixelPerSecond,spectrogramsPath+newFilename)
	print(command)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	#Remove tmp mono track
	os.remove("./tmp/{}.mp3".format(newFilename))

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():
	genresID = dict()
	files = os.listdir(rawDataPath)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(spectrogramsPath)):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#Rename files according to genre
	for index,filename in enumerate(files):
		print ("Creating spectrogram for file {}/{}...".format(index+1,nbFiles))
		fileGenre = getGenre(rawDataPath+filename)
		# fileGenre = str(fileGenre)
		fileGenre = str(fileGenre, encoding='utf-8')
		# print(fileGenre)
		genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
		fileID = genresID[fileGenre]
		newFilename = str(fileGenre)+"_"+str(fileID)#重命名
		# print(newFilename)
		createSpectrogram(filename,newFilename)

#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio():
	print ("Creating spectrograms...")
	createSpectrogramsFromAudio()
	print ("Spectrograms created!")

	print ("Creating slices...")
	createSlicesFromSpectrograms(desiredSize)
	print ("Slices created!")

def AudioToSlices(Path, audiofilename):
	#print ("Creating spectrograms...")
	#print ("Creating spectrogram for file {}".format(audiofilename))
	# fileGenre = getGenre(Path + audiofilename)
	# # fileGenre = str(fileGenre)
	# fileGenre = str(fileGenre, encoding='utf-8')
	# # print(fileGenre)
	# genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
	# fileID = genresID[fileGenre]
	

	newFilename = audiofilename.replace(".mp3", "")+"_dan"
	if isMono(Path + audiofilename):
		command = "cp '{}' 'Music_single/{}.mp3'".format(Path+audiofilename,newFilename)
	else:
		command = "sox '{}' 'Music_single/{}.mp3' remix 1,2".format(Path+audiofilename,newFilename)#转成单声道
	#print(command)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)
	#filename.replace(".mp3","")
	command = "sox 'Music_single/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o 'Music_single/{}.png'".format(newFilename,pixelPerSecond,newFilename)

	#print(command)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)
	

	#Remove tmp mono track
	#os.remove("./{}.mp3".format(newFilename))#删除单声道文件
	#os.remove(rawPrePath+audiofilename)#删除源文件
	#print ("Spectrograms created!")

	#print ("Creating slices...")
	#print(newFilename)
	png2slices(Path, newFilename)
	#print ("Slices created!")

def png2slices(Path, picfilename):
	# sliceSpectrogram(filename, desiredSize)
	img = Image.open("Music_single/"+picfilename + '.png')
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize
	#command = "mkdir {}{}".format(slicesPrePath,picfilename)
	#print(command)
	#p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	#output, errors = p.communicate()
	#if errors:
	#	print (errors)
	for i in range(nbSamples):
		#print ("Creating slice: ", (i+1), "/", nbSamples, "for", picfilename)
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(slicesPrePath+"Pingpu/"+"{}_{}.png".format(picfilename, i))
	#pangs=os.listdir(slicesPrePath+"Pingpu/")
	#print(pangs[:-10])
	#num =len(pangs)
	#save_png=[j*(num//piece) for j in range(piece)]
	#print(num)
	#print(save_png)
	#for f in pangs:
		#num = int((f.split("_")[-1]).split(".")[0])
		#if num in save_png:
			#continue;
		#os.remove(slicesPrePath+"Pingpu/"+f)

		

