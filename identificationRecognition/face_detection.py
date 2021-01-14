import cv2
import argparse
import imutils
from imageio import imread
import os

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", help="Path to images")
# ap.add_argument("-c", "--casc", help="casc")

# args = vars(ap.parse_args())
# # image = cv2.imread(args["image"])

# cascPath = args["casc"]



def countFace(selfie):

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = imread(selfie, pilmode="RGB")
    image = image.copy()

    # ratio = image.shape[0] / 100.0
    # orig = image.copy()
    # image = imutils.resize(image, height = 700)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10, 10),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print ("Found {0} faces.".format(len(faces)))
    return len(faces)

    # uncomment below to draw rectangle around faces found
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)