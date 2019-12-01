# This Python file uses the following encoding: utf-8
import os
import pickle
import threading
from time import sleep

import imutils
import numpy as np
import cv2
from PySide2.QtGui import QImage


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


    def recognise(self, image):
        # load our serialized face detector from disk
        print("[INFO] loading face detector...")
        self.protoPath = os.path.sep.join(["face_detection_model", "deploy.prototxt"])
        self.modelPath = os.path.sep.join(["face_detection_model",
                                           "res10_300x300_ssd_iter_140000.caffemodel"])
        self.detector = cv2.dnn.readNetFromCaffe(self.protoPath, self.modelPath)

        # load our serialized face embedding model from disk
        print("[INFO] loading face recognizer...")
        self.embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")

        # load the actual face recognition model along with the label encoder
        self.recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())
        self.le = pickle.loads(open("output/le.pickle", "rb").read())
        cv2.imwrite("temp/temp.jpg", image)
        image = cv2.imread("temp/temp.jpg")
        os.remove("temp/temp.jpg")
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]
        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        self.detector.setInput(imageBlob)
        detections = self.detector.forward()
        print("NO OF DETECTIONS:", str(len(detections)))
        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > 0.5:
                # compute the (x, y)-coordinates of the bounding box for the
                # face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                                 (0, 0, 0), swapRB=True, crop=False)
                self.embedder.setInput(faceBlob)
                vec = self.embedder.forward()

                # perform classification to recognize the face
                preds = self.recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = self.le.classes_[j]

                # draw the bounding box of the face along with the associated
                # probability
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(image, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        return image

    @threaded
    def processFrames(self):
        i = 0
        cap = cv2.VideoCapture(0)
        while self.threadFlag:
            print("Prcoessing frame no.:" + str(i))
            ret, frame = cap.read()
            frame = self.recognise(frame)
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

