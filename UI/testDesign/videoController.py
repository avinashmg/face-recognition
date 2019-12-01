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
        self.processFrames()
        self.frames = []
        self.threadFlag = True
        self.recogniser = Recogniser()

    @threaded
    def processFrames(self):
        i = 0
        cap = cv2.VideoCapture(0)
        while self.threadFlag:
            print("Prcoessing frame no.:" + str(i))
            ret, frame = cap.read()
            frame = self.recogniser.recogniseFromImage(frame)
            self.frames.append(frame)
            i = i + 1
            sleep(0.01)
        cap.release()
        return

    # @threaded
    def nextQtFrame(self):
        # print("Sending frame")
        if(len(self.frames) == 0):
            sleep(1)
        cvImg = self.frames[-1]
        qtImg = self.convertToQImage(cvImg)
        return qtImg


    def convertToQImage(self, cvImg):
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg




# if __name__ == "__main__":
#     vc = VideoController()

