# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QFileInfo, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pydub import AudioSegment
from mutagen import File
import model_interface
import eyed3
from PIL import Image
import numpy as np
import threading
import wave
import pyaudio
from recommendation import recommendation

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

class PredictThread(QThread):
    signal = pyqtSignal()  # 括号里填写信号传递的参数

    def __init__(self, ui, filename):
        super().__init__()
        self.filename = filename
        self.ui = ui
        print(filename)
    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.signal.emit()  # 发射信号
        self.predictMusic(self.filename)

    def predictMusic(self, filename):
        print('I am predicting')
        self.ui.PredictButton.setText('预测中...')
        label = model_interface.predict(filename)
        if(label[0] == 'R'):
            label = "RnB"
        #     self.ui.Type = '(14)R&B'
        # else:
        #     self.ui.Type = label
        self.ui.PredictButton.setText('预测成功!'+label)
        print("i am recommending")
        if(label[0] == 'R'):
            label = "(14)R&B"
        self.ui.might_like_label.setText("Recommending...")
        RecoList = recommendation(filename, label)

        print(RecoList)

        tempPath = '/Users/vector/Desktop/DeepAudioClassification/Data/RAW/'
        self.ui.song1 = tempPath + RecoList[0] + '.mp3'
        self.ui.song2 = tempPath + RecoList[1] + '.mp3'
        self.ui.song3 = tempPath + RecoList[2] + '.mp3'
        self.ui.progressBar_1.setText(self.ui.solveSongInfo(self.ui.song1)['Title :'])
        self.ui.addSongInfo(self.ui.ListWidget_1, self.ui.solveSongInfo(self.ui.song1))
        self.ui.progressBar_2.setText(self.ui.solveSongInfo(self.ui.song2)['Title :'])
        self.ui.addSongInfo(self.ui.ListWidget_2, self.ui.solveSongInfo(self.ui.song2))
        self.ui.progressBar_3.setText(self.ui.solveSongInfo(self.ui.song3)['Title :'])
        self.ui.addSongInfo(self.ui.ListWidget_3, self.ui.solveSongInfo(self.ui.song3))  # 把歌曲信息分别append到对应的listWidget上
        self.ui.convert2wav(self.ui.song1, 'song1')  # 将文件从源mp3文件转位wav文件并保存在当前工作路径下
        self.ui.song1 = './song1.wav'  # 并且分别命名为song1.song2.song3
        self.ui.convert2wav(self.ui.song2, 'song2')
        self.ui.song2 = './song2.wav'
        self.ui.convert2wav(self.ui.song3, 'song3')
        self.ui.song3 = './song3.wav'
        self.ui.might_like_label.setText("You might also like...")
        # 多线程、创建一个线程进行预测
class RecoThread(QThread):
    signal = pyqtSignal()  # 括号里填写信号传递的参数

    def __init__(self, ui, filename):
        super().__init__()
        self.filename = filename
        self.ui = ui
        print(filename)
    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.signal.emit()  # 发射信号
        self.Recommand(self.filename)
    def Recommand(self, filename):
        print("i am recommending")
        self.ui.might_like_label.setText("Recommending...")
        RecoList = recommendation(filename, self.ui.Type)

        print(RecoList)

        tempPath = '/Users/vector/Desktop/DeepAudioClassification/Data/RAW/'
        self.ui.song1 = tempPath + RecoList[0] + '.mp3'
        self.ui.song2 = tempPath + RecoList[1] + '.mp3'
        self.ui.song3 = tempPath + RecoList[2] + '.mp3'
        self.ui.addSongInfo(self.ui.ListWidget_1, self.ui.solveSongInfo(self.ui.song1))
        self.ui.addSongInfo(self.ui.ListWidget_2, self.ui.solveSongInfo(self.ui.song2))
        self.ui.addSongInfo(self.ui.ListWidget_3, self.ui.solveSongInfo(self.ui.song3))#把歌曲信息分别append到对应的listWidget上
        self.ui.convert2wav(self.ui.song1, 'song1')#将文件从源mp3文件转位wav文件并保存在当前工作路径下
        self.ui.song1 = './song1.wav'#并且分别命名为song1.song2.song3
        self.ui.convert2wav(self.ui.song2, 'song2')
        self.ui.song2 = './song2.wav'
        self.ui.convert2wav(self.ui.song3, 'song3')
        self.ui.song3 = './song3.wav'
        self.ui.might_like_label.setText("You might also like...")
class MyThread(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        print(filename)

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.signal.emit()    # 发射信号
        self.playMusic(self.filename)

    def playMusic(self, filename):

            # 多线程、创建一个线程来播放音乐，当前主线程用来接收用户操作
            # global playing
            # playing = True
            # t = threading.Thread(target=loop)

            # t.start()
        # print(self.filename)
        CHUNK = 1024

        wf = wave.open(self.filename, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cursong0 =''#表明当前是否有打开歌曲
        self.ButtonStatus = [0, 0, 0, 0]
        self.song1 = ''
        self.song2 = ''
        self.song3 = ''
        self.Type = ''
        self.status = 'stop'
        self.playAuthor = 0
        self.cursonginfo = {}
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.songImage = QtWidgets.QLabel(self.centralwidget)
        self.songImage.setGeometry(QtCore.QRect(70, 50, 300, 300))
        self.songImage.setObjectName("songImage")
        self.MainPlayButton = QtWidgets.QPushButton(self.centralwidget)
        self.MainPlayButton.setGeometry(QtCore.QRect(80, 315, 30, 30))
        self.MainPlayButton.setObjectName("MainPlayButton")
        self.MainPlayButton.clicked.connect(lambda: self.mainButtonClick(MainWindow))


        self.toPlay = QIcon('播放.png')
        self.MainPlayButton.setIcon(self.toPlay)
        self.MainPlayButton.setIconSize(QSize(20, 20))
        self.MainPlayButton.setFlat(True)

        self.Stop = QIcon('停止.png')

        self.mainProgressBar = QtWidgets.QLabel(self.centralwidget)
        self.mainProgressBar.setGeometry(QtCore.QRect(150, 320, 300, 23))
        # self.mainProgressBar.setProperty("value", 0)
        self.mainProgressBar.setObjectName("mainProgressBar")

        self.select_song_label = QtWidgets.QPushButton(self.centralwidget)
        self.select_song_label.setGeometry(QtCore.QRect(70, 10, 150, 40))
        self.select_song_label.setObjectName("select_song_label")
        self.select_song_label.clicked.connect(lambda: self.openfile(MainWindow))

        self.PredictButton = QtWidgets.QPushButton(self.centralwidget)
        self.PredictButton.setGeometry(QtCore.QRect(210, 10, 150, 40))
        self.PredictButton.setObjectName("PredictButton")
        self.PredictButton.clicked.connect(lambda: self.predict(MainWindow))

        self.mainListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mainListWidget.setGeometry(QtCore.QRect(70, 370, 300, 150))
        self.mainListWidget.setObjectName("mainListWidget")
        self.might_like_label = QtWidgets.QLabel(self.centralwidget)
        self.might_like_label.setGeometry(QtCore.QRect(400, 10, 181, 41))
        self.might_like_label.setObjectName("might_like_label")

        self.progressBar_1 = QtWidgets.QLabel(self.centralwidget)
        self.progressBar_1.setGeometry(QtCore.QRect(430, 60, 400, 23))

        # self.progressBar_1.setProperty("value", 0)
        self.progressBar_1.setObjectName("progressBar_1")


        self.playButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.playButton_1.setGeometry(QtCore.QRect(400, 60, 30, 30))
        self.playButton_1.setObjectName("playButton_1")
        self.playButton_1.clicked.connect(lambda: self.btn1Click(MainWindow))
        self.playButton_1.setIcon(self.toPlay)
        self.playButton_1.setIconSize(QSize(20, 20))
        self.playButton_1.setFlat(True)

        self.ListWidget_1 = QtWidgets.QListWidget(self.centralwidget)
        self.ListWidget_1.setGeometry(QtCore.QRect(400, 110, 400, 100))
        self.ListWidget_1.setObjectName("ListWidget_1")
        self.progressBar_2 = QtWidgets.QLabel(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(430, 220, 400, 23))
        # self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        # self.progressBar_2.setText('kkk')
        self.ListWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.ListWidget_2.setGeometry(QtCore.QRect(400, 265, 400, 100))
        self.ListWidget_2.setObjectName("ListWidget_2")

        self.playButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.playButton_2.setGeometry(QtCore.QRect(400, 220, 30, 30))
        self.playButton_2.setObjectName("playButton_2")
        self.playButton_2.clicked.connect(lambda: self.btn2Click(MainWindow))
        self.playButton_2.setIcon(self.toPlay)
        self.playButton_2.setIconSize(QSize(20, 20))
        self.playButton_2.setFlat(True)


        self.progressBar_3 = QtWidgets.QLabel(self.centralwidget)
        self.progressBar_3.setGeometry(QtCore.QRect(430, 370, 400, 23))
        # self.progressBar_3.setText('kkk')
        # self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setObjectName("progressBar_3")



        self.ListWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.ListWidget_3.setGeometry(QtCore.QRect(400, 420, 400, 100))
        self.ListWidget_3.setObjectName("ListWidget_3")


        self.playButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.playButton_3.setGeometry(QtCore.QRect(400, 370, 30, 30))
        self.playButton_3.setObjectName("playButton_3")
        self.playButton_3.clicked.connect(lambda: self.btn3Click(MainWindow))
        self.playButton_3.setIcon(self.toPlay)
        self.playButton_3.setIconSize(QSize(20, 20))
        self.playButton_3.setFlat(True)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # menuBar()创建菜单栏。这里创建了一个菜单栏，并在上面添加了一个file菜单，
        # 并关联了点击退出应用的事件。
        menubar = MainWindow.menuBar()
        fileMenu = menubar.addMenu('&File')
        MainWindow.setMenuBar(menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "基于深度学习的歌曲分类推荐系统"))
        self.songImage.setText(_translate("MainWindow", "The image of song"))
        font = QFont()
        font.setFamily('Comic Sans MS')
        # self.MainPlayButton.setText(_translate("MainWindow", "pl"))
        self.select_song_label.setText(_translate("MainWindow", "Select song"))
        self.select_song_label.setFont(font)
        self.PredictButton.setText(_translate("MainWindow", "Push to Predict"))
        self.PredictButton.setFont(font)
        self.might_like_label.setText(_translate("MainWindow", "You might also like..."))
        font = QFont()
        font.setPointSize(20)
        font.setFamily('Comic Sans MS')
        self.might_like_label.setFont(font)
        font.setPointSize(30)
        self.songImage.setFont(font)
        self.songImage.setScaledContents(True)
        font.setPointSize(15)
        self.progressBar_1.setFont(font)
        self.progressBar_2.setFont(font)
        self.progressBar_3.setFont(font)
        # self.playButton_1.setText(_translate("MainWindow", "pl"))
        # self.playButton_2.setText(_translate("MainWindow", "pl"))
        # self.playButton_3.setText(_translate("MainWindow", "pl"))

    def mainButtonClick(self,MainWindow):
        if self.cursong0 =='':
            QMessageBox.information(MainWindow, "温馨提示", "请先打开歌曲再进行播放！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.setAllButton2Play()
        if self.ButtonStatus[0] == 0:
            self.MainPlayButton.setIcon(self.Stop)
        else:
            self.MainPlayButton.setIcon(self.toPlay)
        self.ButtonStatus[0] = not self.ButtonStatus[0]
        self.play(MainWindow, self.cursong0, 0)
    def btn1Click(self, MainWindow):
        if self.song1 == '':
            QMessageBox.information(MainWindow, "温馨提示", "请先打开歌曲再进行播放！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.setAllButton2Play()
        if self.ButtonStatus[1] == 0:
            self.playButton_1.setIcon(self.Stop)
        else:
            self.playButton_1.setIcon(self.toPlay)
        self.ButtonStatus[1] = not self.ButtonStatus[1]
        self.play(MainWindow, self.song1, 1)
    def setAllButton2Play(self, exp = 0):
        self.MainPlayButton.setIcon(self.toPlay)
        # self.MainPlayButton.setIconSize(QSize(20, 20))
        self.playButton_1.setIcon(self.toPlay)
        # self.playButton_1.setIconSize(QSize(20, 20))
        self.playButton_2.setIcon(self.toPlay)
        # self.playButton_2.setIconSize(QSize(20, 20))
        self.playButton_3.setIcon(self.toPlay)
        # self.playButton_3.setIconSize(QSize(20, 20))

    def btn2Click(self, MainWindow):
        if self.song2 == '':
            QMessageBox.information(MainWindow, "温馨提示", "请先打开歌曲再进行播放！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.setAllButton2Play()
        if self.ButtonStatus[2] == 0:
            self.playButton_2.setIcon(self.Stop)
        else:
            self.playButton_2.setIcon(self.toPlay)
        self.ButtonStatus[2] = not self.ButtonStatus[2]
        self.play(MainWindow, self.song2, 2)

    def btn3Click(self, MainWindow):
        if self.song3 == '':
            QMessageBox.information(MainWindow, "温馨提示", "请先打开歌曲再进行播放！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.setAllButton2Play()
        if self.ButtonStatus[3] == 0:
            self.playButton_3.setIcon(self.Stop)
        else:
            self.playButton_3.setIcon(self.toPlay)
        self.ButtonStatus[3] = not self.ButtonStatus[3]
        self.play(MainWindow, self.song3,3 )


    def openfile(self, MainWindow):
        self.PredictButton.setText('Push to Predict')
        self.might_like_label.setText('You might also like...')
        self.MainPlayButton.setIcon(self.toPlay)
        if(self.status == 'playing'):
            self.status = 'stop'
            self.Thread.terminate()
            self.playAuthor = 0
        print('openfile')
        fname = QFileDialog.getOpenFileName(MainWindow, '打开文件', './')
        if fname[0] == '':
            return
        filename = fname[0]#带完整路径的文件名
        self.TobePredictSong = filename
        fileinfo = QFileInfo(fname[0])
        file_name = fileinfo.fileName();#仅文件名
        self.getPicFromMp3(filename)
        self.addSongInfo(self.mainListWidget, self.solveSongInfo(filename))
        audiofile = eyed3.load(filename)
        self.Type = str(audiofile.tag.genre)
        font = QFont()
        font.setPointSize(15)
        font.setFamily('Comic Sans MS')
        self.mainListWidget.setFont(font)
        if (filename[-1] == '3'):  # 如果读入的是一个mp3文件
            sound = AudioSegment.from_mp3(filename)
            self.cursong0 = 'cursong0' + '.wav'
            sound.export('cursong0'+ '.wav', format="wav")
        else:
            self.cursong0 = filename
        with open('curpic.jpg', 'rb') as img:
            pix = QPixmap('curpic.jpg')
            self.songImage.setPixmap(pix)
            self.songImage.setScaledContents(True)
        #开始加载数据库中的三首歌曲

            # 将文件读入并将格式由mp3转为wav
        # t = threading.Thread(target=self.playMusic(file_name))
        #
        # t.start()
        # self.Thread = MyThread(file_name)
        # self.Thread.start()
        # print(file_name)
        # # 文件后缀
        # file_suffix = fileinfo.suffix()
        # print(file_suffix)
        # # 绝对路径
        # file_path = fileinfo.absolutePath();
        # print(file_path)
    def convert2wav(self, songname, aftername):
        sound = AudioSegment.from_mp3(songname)
        sound.export(aftername + '.wav', format="wav")

    def solveSongInfo(self, songname):#用于读取歌曲信息
        audiofile = eyed3.load(songname)
        cursonginfo = {}
        cursonginfo['Artist:'] = audiofile.tag.artist
        cursonginfo['Title :'] = audiofile.tag.title
        cursonginfo['Album :'] = audiofile.tag.album
        cursonginfo['Time  :'] = str((audiofile.info.time_secs) // 60)+ '分' + str((audiofile.info.time_secs) % 60) + '秒'
        # cursonginfo['Genre :'] = str(audiofile.tag.genre)
        return cursonginfo
    def addSongInfo(self, ListWidget, songinfo):#用于将歌曲信息添加入ListWidget
        ListWidget.clear()
        d = 30
        font = QFont()
        font.setPointSize(10)
        font.setFamily('Comic Sans MS')
        ListWidget.setFont(font)
        for key in songinfo:
            showContent = str(key) + str(songinfo[key])
            print(showContent)
            ListWidget.addItem(showContent)
            # ListWidget.addItem("Artist")
    def getPicFromMp3(self, filename):
        afile = File(filename)
        print(afile.tags)

        if 'APIC:' in afile.tags:
            artwork = afile.tags['APIC:'].data
            with open('curpic.jpg', 'wb') as img:
                img.write(artwork)
                pix = QPixmap('curpic.jpg')
                self.songImage.setPixmap(pix)
                self.songImage.setScaledContents (True)

    def predict(self, MainWindow):
        print('predicting... and recommend')
        self.PredThread = PredictThread(self, self.TobePredictSong)#分类并推荐
        self.PredThread.start()
        # if self.cursong0 =='':
        #     QMessageBox.information(MainWindow, "温馨提示", "请先打开歌曲再进行预测！", QMessageBox.Yes, QMessageBox.Yes)
        #     return
        # tempPath = '/Users/vector/Desktop/DeepAudioClassification/Data/RAW/'
        # self.song1 = tempPath + '林俊杰-江南.mp3'
        # self.song2 = tempPath + '贝多芬-悲怆奏鸣曲.mp3'
        # self.song3 = tempPath + '不才-参商.mp3'
        # self.addSongInfo(self.ListWidget_1, self.solveSongInfo(self.song1))
        # self.addSongInfo(self.ListWidget_2, self.solveSongInfo(self.song2))
        # self.addSongInfo(self.ListWidget_3, self.solveSongInfo(self.song3))#把歌曲信息分别append到对应的listWidget上
        # self.convert2wav(self.song1, 'song1')#将文件从源mp3文件转位wav文件并保存在当前工作路径下
        # self.song1 = './song1.wav'#并且分别命名为song1.song2.song3
        # self.convert2wav(self.song2, 'song2')
        # self.song2 = './song2.wav'
        # self.convert2wav(self.song3, 'song3')
        # self.song3 = './song3.wav'


    def play(self, MainWindow, songname, author):
        print(self.playAuthor)
        if self.playAuthor != author and self.status == 'playing':
            self.Thread.terminate()
            QMessageBox.information(MainWindow, "温馨提示", "马上为您播放", QMessageBox.Yes, QMessageBox.Yes)
            self.status = 'playing'
            self.playAuthor = int(str(author)[-1])
            self.Thread = MyThread(songname)
            self.Thread.start()
            return
        self.playAuthor = int(str(author)[-1])
        if self.status == 'stop':
            QMessageBox.information(MainWindow, "温馨提示", "马上为您播放", QMessageBox.Yes, QMessageBox.Yes)
            self.status = 'playing'
            self.Thread = MyThread(songname)
            self.Thread.start()
            self.Thread.isFinished()
        else:
            QMessageBox.information(MainWindow, "温馨提示", "停止播放！", QMessageBox.Yes, QMessageBox.Yes)
            self.status = 'stop'
            if self.Thread.isFinished() == False:
                self.Thread.terminate()
                self.playAuthor = int(str(author)[-1])

