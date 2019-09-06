This attempt uses the following as the base tutorial from Machine Learning Mastery:
https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/

It uses MTCNN for detecting faces and then uses the Keras port of the FaceNet model by Hiroki Taniai (found at https://github.com/nyoki-mtl/keras-facenet) to extract embeddings and train a SVM classifier on top of the same.

It is initially trained on the 5 celebrity faces dataset.
