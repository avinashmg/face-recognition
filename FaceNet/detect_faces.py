# face detection for the 5 Celebrity Faces Dataset
import argparse
from os import listdir
from os.path import isdir
from PIL import Image
from matplotlib import pyplot
from numpy import savez_compressed
from numpy import asarray
from mtcnn.mtcnn import MTCNN

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset",
                help="path to input directory of faces + images")
args = ap.parse_args()


# extract a single face from a given photograph
def extract_face(filename, required_size=(160, 160)):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        face = extract_face(path)
        # store
        faces.append(face)
    return faces


# Load a dataset that contains one subdir for each class
# that in turn contains images
def load_dataset(directory):
    X, y = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        # load all faces found in the subdirectory
        faces = load_faces(path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)


if args.dataset:
    # load from arguments
    trainX, trainy = load_dataset(args.dataset + '/train/')
    print(trainX.shape, trainy.shape)
    # load test dataset
    testX, testy = load_dataset(args.dataset + '/val/')
else:
    # load from default arguments
    # load train dataset
    trainX, trainy = load_dataset('5-celebrity-faces-dataset/train/')
    print(trainX.shape, trainy.shape)
    # load test dataset
    testX, testy = load_dataset('5-celebrity-faces-dataset/val/')

# save arrays to one file in compressed format
# TODO: Need to change naming scheme in case custom dataset is loaded
savez_compressed('5-celebrity-faces-dataset.npz', trainX, trainy, testX, testy)
