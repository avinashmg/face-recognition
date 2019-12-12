import os
import pickle

import cv2
import face_recognition
import imutils
import numpy as np


class Recogniser:
    def __init__(self):
        # load our serialized face detector from disk
        print("[INFO] loading face detector...")
        self.protoPath = os.path.sep.join(["face_detection_model", "deploy.prototxt"])
        self.modelPath = os.path.sep.join(["face_detection_model",
                                           "res10_300x300_ssd_iter_140000.caffemodel"])
        self.detector = cv2.dnn.readNetFromCaffe(self.protoPath, self.modelPath)

        print("[INFO] loading face recognizer...")
        self.embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")

        print("[INFO] loading encodings...")
        self.data = pickle.loads(open("output/encodings.pickle", "rb").read())

    def recogniseFromImage(self, image):
        # load the input image and convert it from BGR to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        print("[INFO] recognizing faces...")
        boxes = face_recognition.face_locations(rgb,
                                                model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        # initialize the list of names for each face detected
        names = []
        # loop over the facial embeddings
        print("[INFO] faces detected:", len(encodings))
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"],
                                                     encoding)
            name = "Unknown"
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)
                # update the list of names
                names.append(name)
        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
        print("[INFO] detected faces:", names)
        if len(names) != 0:
            key = names[0]
        else:
            key = 'null'
        return image, key

    def recogniseFromFileName(self, filename):
        image = cv2.imread(filename)
        self.recogniseFromImage(image)