# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import numpy as np
import pickle

import numpy as np
import eyed3
import math
from collections import Counter
import json
from model import createModel
from datasetTools import getDataset,createPreDatasetFromSlices
from config import slicesPath
from config import batchSize,rawPrePath
from config import filesPerGenre
from config import nbEpoch,DonePath
from config import validationRatio, testRatio
from config import sliceSize,datasetPrePath,rawPrePath

from songToData import createSlicesFromAudio, AudioToSlices

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice", "predict"])
args = parser.parse_args()   #处理输入参数

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validationRatio))
print("| Test ratio: {}".format(testRatio))
print("| Slices per genre: {}".format(filesPerGenre))
print("| Slice size: {}".format(sliceSize))
print("--------------------------")
#genres ={'(14)R&B':0,'中国风':1, '古典':2, '摇滚':3,'民谣':4, '爵士':5,'说唱':6}

#List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]

print("genresw:",genres)
nbClasses = len(genres)

total=0
genre_haven=[0,0,0,0,0,0,0]
right_haven=[0,0,0,0,0,0,0]
#Create model 
model = createModel(nbClasses, sliceSize) #生成模型（未填录数据）

if "train" in args.mode:

	#Create or load new dataset
	train_X, train_y, validation_X, validation_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

	#Define run id for graphs
	run_id = "MusicGenres - "+str(batchSize)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

	#Train the model
	print("[+] Training the model...")
	model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
	print("    Model trained! ✅")

	#Save trained model
	print("[+] Saving the weights...")
	model.save('musicDNN.tflearn')
	print("[+] Weights saved! ✅💾")

if "test" in args.mode:

	#Create or load new dataset
	test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")

	#Load weights	
	print("[+] Loading weights...")
	model.load('musicDNN.tflearn')
	print("    Weights loaded! ✅")

	res_y = model.predict_label(test_X)
	print(res_y)
	testAccuracy = model.evaluate(test_X, test_y)[0]
	print("[+] Test accuracy: {} ".format(testAccuracy))
										#path="/home/test/"  #待读取的文件夹
										#path_list=os.listdir(path)
										#path_list.sort() #对读取的路径进行排序
										#for filename in path_list:
										#	print(os.path.join(path,filename))

if "predict" in args.mode:
	files = os.listdir(rawPrePath)
    #path="/home/test/"  #待读取的文件夹	
	model.load('musicDNN.tflearn')
	for file in files:
		AudioToSlices(rawPrePath, file)
		createPreDatasetFromSlices(file)
		#print("[+] Loading preing dataset... ")
		audiofile=eyed3.load(DonePath+file)
		tag=audiofile.tag.genre
		tag=str(tag)
		#m=json.dumps(genres[tag], encoding="UTF-8", ensure_ascii=False)
		m=genres.index(tag)
		print("正确流派：",tag)
		genre_haven[m]+=1
		test_X = pickle.load(open("{}{}/{}.p".format(datasetPrePath,tag,file.replace(".mp3","")), "rb" ))
		#print("    Testing dataset loaded! ✅")
		res_y = model.predict_label(test_X)
		res_x=res_y[:,0]
		word_counts = Counter(res_x)
		top_one= word_counts.most_common(1)
		top_one=list(top_one[0])
		label=int(top_one[0])
		#print(type(top_one[0]))
		if(label==m):
			right_haven[m]+=1
			print("预测正确")
		else:
			print("预测错误")
		total+=1
		#print("total",total)
		print("right_haven",right_haven,"sum",sum(right_haven))
		print("genre_haven:",genre_haven,"sum",sum(genre_haven))
		print("total_rate",sum(right_haven)/sum(genre_haven))
		gener_rate=np.divide(np.array(right_haven),np.array(genre_haven))
		print ("genre_rate:",gener_rate)
		#print("total_rate:")
		print("------------------------------------\n")






