# -*- coding: utf-8 -*-
import os,sys
import pickle
import numpy as np
import pandas as pd
from math import sqrt
from model_interface import predict


def recommendation(filename,category):
	print("filenameeeeeeeeeeeeeeeeeE:",filename)
	# category = 'test'
	print(category)
	# category = predict(filename)
	datasetPath = "./Data/Recodataset/"+category
	dirs = os.listdir(datasetPath)
	goalfile = os.listdir("single/p/")
	#print(type(goalfile[0]))
	goal = pickle.load(open("single/p/"+goalfile[0],"rb"))
	minlen = 20
	songset = []
	#get the empty file and the min length of all files
	for filename in dirs:
		if os.path.getsize("{}/{}".format(datasetPath,filename)) > 0: 
			try:     
				train_X = pickle.load(open("{}/{}".format(datasetPath,filename), "rb" ))
				train_X = np.concatenate(train_X)
				train_X = np.concatenate(train_X)
				train_X = np.concatenate(train_X)
				# dimensionality reduce and use the middle part of the song to evaluate similarity
				train_X = train_X.tolist()

				songset.append(train_X)
				if minlen > len(train_X):
					minlen = len(train_X)
			except EOFError:
				#this file is empty
				print(filename)
	if minlen > len(goal):
		minlen = len(goal)
		for i in range(songset):
			songset[i] = songset[i][len(songset)//2-minlen//2*128*128:len(songset)//2+minlen//2*128*128]
	print("minlenth:",minlen)
	#print(len(dirs))
	#print("aaafaefafae",type(songset))
	#print("aaaaaaaaa",type(songset[0]))
	#print("bbbbbbbbb",songset[0])

	#print("songset[0]",songset[0])
	goal = np.concatenate(goal)
	goal = np.concatenate(goal)
	goal = np.concatenate(goal)
	goal = goal[len(goal)//2-minlen//2*128*128:len(goal)//2+minlen//2*128*128]
	print(goal.shape,len(songset),len(songset[0]))
	a = cosine_similarity(goal.tolist(),songset)
	#sort the most similar song of the first song in 20 songs
	b = a[:]
	b.sort(reverse = True)
	#print(b)
	return (dirs[a.index(b[0])])[0:-2],(dirs[a.index(b[1])])[0:-2],(dirs[a.index(b[2])])[0:-2]
	#return dirs[(np.argsort(np.array(a)))[-3:]]

def cosine_similarity(goal,dataset):
	res = []
	for j in range(len(dataset)):
		sum0 = 0
		sumx = 0
		sumy = 0
		for i in range(len(goal)):
			#print("faefaef",goal[i],dataset[j][i])
			sum0 += goal[i]*dataset[j][i]
			sumx += goal[i]*goal[i]
			sumy += dataset[j][i]*dataset[j][i]
		res.append(sum0/(sqrt(sumx)*sqrt(sumy)))
		#print(sum0/(sqrt(sumx)*sqrt(sumy)))
	return res

if __name__=="__main__":
	print(recommendation("/home/qjchen/Desktop/train/test_Music/刘小天-风车.mp3", "民谣"))
 	#print(cosine_similarity([0.1,1.2],[[1.3,3.1],[1.2,2.1]]))
	


