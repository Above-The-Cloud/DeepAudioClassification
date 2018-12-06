#Define paths for files
base = ""
spectrogramsPath = base+"Data/Spectrograms/" #每首歌的频谱图_切割前_已分类
slicesPath = base+"Data/Slices/"  #切割后频谱图_已分类
slicesPrePath=base+"Data/SlicesPath/"
datasetPath = base+"Data/Dataset/" #打包后的训练集，测试集和验证集_p文件
datasetPrePath=base+"Data/DataPreset/"
rawDataPath = base+"Data/Raw/"
rawPrePath=base+"Music/"
DonePath=base+"Music/"

#Spectrogram resolution
pixelPerSecond = 50  #每秒50像素

#Slice parameters
sliceSize = 128  #每个图片段像素大小

#Dataset parameters
filesPerGenre = 1000 #每个流派文件数量
validationRatio = 0.3  #验证集比率
testRatio = 0.1  #测试集比率

#Model parameters
batchSize = 128  #批量大小
learningRate = 0.001 #学习速率
nbEpoch = 20 #训练次数
