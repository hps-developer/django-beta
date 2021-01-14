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
    
    image_original = imread(selfie, pilmode="RGB")
    image_rotate_90_counterclockwise = cv2.rotate(image_original, cv2.ROTATE_90_COUNTERCLOCKWISE)
    image_rotate_90_clockwise = cv2.rotate(image_original, cv2.ROTATE_90_CLOCKWISE)
    image_rotate_180 = cv2.rotate(image_original, cv2.ROTATE_180)

    image_original = image_original.copy()
    image_rotate_90_counterclockwise = image_rotate_90_counterclockwise.copy()
    image_rotate_90_clockwise = image_rotate_90_clockwise.copy()
    image_rotate_180 = image_rotate_180.copy()

    image_array = []
    image_array.append(image_original)
    image_array.append(image_rotate_90_counterclockwise)
    image_array.append(image_rotate_90_clockwise)
    image_array.append(image_rotate_180)

    
    # ratio = image.shape[0] / 100.0
    # orig = image.copy()
    # image = imutils.resize(image, height = 700)

    face_count = 0

    for image in image_array:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(10, 10),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        face_found = len(faces)

        if face_found > 0:
            break

    return face_found

    # use below to draw rectangle around faces found
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)