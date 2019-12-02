# This Python file uses the following encoding: utf-8
import os
import pickle
import threading
from time import sleep

import imutils
import numpy as np
import cv2
from PySide2.QtGui import QImage

from recognizer import Recogniser


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class VideoController():

    def __init__(self):
        print("Initialising video controller")
        print("Calling processFrames")
        # self.processFrames()
        self.frames = []
        self.threadFlag = True
        self.recogniser = Recogniser()
        self.i = 0
        self.cap = cv2.VideoCapture(0)

    # # @threaded
    # def processFrames(self):
    #     i = 0
    #     cap = cv2.VideoCapture(0)
    #     while self.threadFlag:
    #         print("[INFO] prcoessing frame no.:" + str(i))
    #         ret, frame = cap.read()
    #         prcoessedFrame = self.recogniser.recogniseFromImage(frame.copy())
    #         print("[INFO] appending frame to array")
    #         self.frames.append(prcoessedFrame)
    #         i = i + 1
    #     cap.release()
    #     return

    # @threaded
    def nextQtFrame(self):
        print("[INFO] qt requesting frame")
        print("[INFO] prcoessing frame no.:" + str(self.i))
        ret, frame = self.cap.read()
        prcoessedFrame = self.recogniser.recogniseFromImage(frame.copy())
        self.i = self.i + 1
        qtImg = self.convertToQImage(prcoessedFrame)
        print("[INFO] sending frame to Qt")
        return qtImg


    def convertToQImage(self, cvImg):
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg

    def __del__(self):
        self.cap.release()




# if __name__ == "__main__":
#     vc = VideoController()

