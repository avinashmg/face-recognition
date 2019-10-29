# Face Detection using Multi-Task Convolutional Neural Network
from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray
default_image_size = 160


# TODO: Receive direct image instead of filename
def extract_face_mtcnn(
        filename,
        output_size=(default_image_size, default_image_size)
        ):
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

# 2. Face Detection using OpenCV's deep learning based face detector
# 2.1. Load serialized face detector from disk


print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
                             "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


def extract_face_opencv(filename):
    image = cv2.imread(filename)
    cv2.imshow('Original Image', image)
    image = imutils.resize(image, width=600)
    cv2.imshow('Resized Image', image)
