from __future__ import print_function
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import IdentificationRecognitionSerializer
from .serializers import IdentificationListSerializer
from .serializers import IdentificationUrlOrNameSerializer
from .models import IdentificationRecognition, IdentificationList, IdentificationUrlOrName

from typing import NoReturn

from matplotlib import image
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import cv2
import imutils
import requests
from imageio import imread
from . import face_detection 
from . import idcropper
import torch
import os , os.path, sys
import traceback


def cropImageLocal(img):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'id_rec/yolov5/runs/train/exp9/weights/best.pt', force_reload=False)
    get_image = idcropper.Cropper(img,model)
    linku =  get_image.crop()
    del get_image
    del model
    return linku



def CropListImageLocal(listu):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'id_rec/yolov5/runs/train/exp9/weights/best.pt', force_reload=False)
    res = []
    for name in listu:
        get_image = idcropper.Cropper(name,model)
        linku = get_image.crop()
        res.append(linku)
    return res

class IdentificationRecognitionView(viewsets.ModelViewSet):
    queryset = IdentificationRecognition.objects.all()
    serializer_class = IdentificationRecognitionSerializer
        

    def mse(self, imageA, imageB):
        
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        return err



    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype = "float32")

        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis = 1)

        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect


    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - tl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))


        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")

        
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped



    def createDetector(self):
        detector = cv2.ORB_create(nfeatures=2000)
        return detector


    def getFeatures(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = self.createDetector()
        kps, descs = detector.detectAndCompute(gray, None)
        return kps, descs, img.shape[:2][::1]


    def detectFeatures(self, img, train_features):
        train_kps, train_descs, shape = train_features

        #get features from image
        kps, descs, _ = self.getFeatures(img)

        #check if keypoints are extracted
        if not kps:
            return None
        
        #to find matching keypoints in two sets of descriptors 
        #(from sample image, and from algorithm for that)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(train_descs, descs, k=2)

        good = []
        # apply ratio test to matches of each keypoint
        # idea is if train KP have a matching KP on image,
        # it will be much closer than next closest non-matching KP
        # otherwise, all KPs will be almost equally far
        for m, n in matches:
            if (m.distance < 0.8 * n.distance):
                good.append(m)
            
        # stop if didn't find enough matching keypoints
        if len(good) < 0.1 * len(train_kps):
            return None
        
        # estimate a transformation matrix which maps 
        # keypoints from train image coordinates to sample image

        src_pts = np.float32([train_kps[m[0].queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kps[m[0].trainIdx].pt for m in good]).reshape(-1, 1, 2)

        m, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if m is not None:
            # apply perspective transform to train image corners to get a bounding box 
            # coordinates on a sample image

            scene_points = cv2.perspectiveTransform(np.float32([(0, 0), (0, shape[0] - 1),
                            (shape[1] - 1), (shape[1] - 1, shape[0] - 1), 
                            (shape[1] - 1, 0)]).reshape(-1, 1, 2, m))
            
            rect = cv2.minAreaRect(scene_points)

            # check resulting rect ratio knowing we have almost square train image
            if rect[1][1] > 0 and 0.8 < (rect[1][0] / rect[1][1]) < 1.2:
                return rect
        
        return None


    def findTemplate(self, image, template):
        image = imread(image, pilmode="RGB")
        image = image.copy()
        
        template_original = imread(template, pilmode="RGB")
        template_rotate_90_counterclockwise = cv2.rotate(template_original, cv2.ROTATE_90_COUNTERCLOCKWISE)
        template_rotate_90_clockwise = cv2.rotate(template_original, cv2.ROTATE_90_CLOCKWISE)
        template_rotate_180 = cv2.rotate(template_original, cv2.ROTATE_180)

        template_original = template_original.copy()
        template_rotate_90_counterclockwise = template_rotate_90_counterclockwise.copy()
        template_rotate_90_clockwise = template_rotate_90_clockwise.copy()
        template_rotate_180 = template_rotate_180.copy()

        templateArray = []
        templateArray.append(template_original)
        templateArray.append(template_rotate_90_counterclockwise)
        templateArray.append(template_rotate_90_clockwise)
        templateArray.append(template_rotate_180)

        maxMaxVal = 0
        for template in templateArray:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 50, 200)
            (tH, tW) = template.shape[:2]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            found = None

            # loop over the scales of the image
            for scale in np.linspace(0.2, 1.0, 15)[::-1]:
                # resize the image according to the scale, and keep track
                # of the ratio of the resizing
                resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
                r = gray.shape[1] / float(resized.shape[1])
                # if the resized image is smaller than the template, then break
                # from the loop
                if resized.shape[0] < tH or resized.shape[1] < tW:
                    break

                # detect edges in the resized, grayscale image and apply template
                # matching to find the template in the image
                edged = cv2.Canny(resized, 50, 200)
                result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)

                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result, None)

                # if new maximum correlation value is found, then update
                # the bookkeeping variable
                if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)
                    print(maxVal)
                    # checking if it's a good match, value of 0.1 selected based on testings
                    # if (maxVal > 0.1):
                    #     haveFoundBool = True

            
            if found[0] > maxMaxVal:
                maxMaxVal = found[0]
            
            if maxMaxVal > 0.1:
                return maxMaxVal
            # uncomment below to draw detected object (Mongolian ID)

            # (_, maxLoc, r) = found
            # (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            # (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
            # # draw a bounding box around the detected result and display the image
            # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            # cv2.imshow("Image", image)
            # cv2.waitKey(0)

            # return haveFoundBool
        return maxMaxVal
        

    @action(methods=['post'], detail=False)
    def findTemplateInImage(self, request):
        serializer = IdentificationRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                template = request.data.get('template')
                image = request.data.get('idImage')
            except:
                return Response({'code': '101', 'status': 'error', 'message': 'Error occurred while reading template and/or ID.'})
            try:
                result = self.findTemplate(image, template)
                status = ''
                if (result > 0.1):
                    status = 'valid'
                elif (result > 0.08 and result <= 0.1):
                    status = 'revision_needed'
                elif (result <= 0.08):
                    status = 'invalid'
            except:
                return Response({'code': '102', 'status': 'error', 'message': 'Error occurred while processing images. (INAVLID IMAGE)'})
            return Response({'code': '201', 'status': 'success', 'id_status': status})
        else:
            print(serializer.errors)
        return Response({'status': 'error', 'message': 'invalid request'})

    @action(methods=['post'], detail=False)
    def cropListImages(self, request):
        try:
            imlist = request.data.get('idList')
            print(imlist)
        except:
            return Response({'code': '101', 'status': 'error', 'message': 'Error occurred while reading IDList.'})

        try:
            status = CropListImageLocal(imlist)
            #print(status)
        except:
            return Response({'code': '102', 'status': 'error', 'message': 'Error occurred while processing images. (INAVLID IMAGE)'})
        
        return Response({'code': '201', 'status': 'success', 'id_status': status})
    

    @action(methods=['post'], detail=False)
    def cropImage(self, request):
        serializer = IdentificationUrlOrNameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image = request.data.get('urlOrName')
            except:
                return Response({'code': '101', 'status': 'error', 'message': 'Error occurred while reading UrlOrName'})
            
            try:
                status = cropImageLocal(str(image))
                #print(status)
            except Exception as e: 
                return Response({'code': '102', 'status': 'error', 'message': str(e) })
            
            return Response({'code': '201', 'status': 'success', 'id_status': status})
        
        return Response({'status': 'error', 'message': 'invalid request'})
    

    @action(methods=['post'], detail=False)
    def faceDetection(self, request):
        
        if 'selfie' in request.data:
            try:
                selfie = request.data.get('selfie')
            except:
                return Response({'code': '101', 'status': 'error', 'message': 'Error occurred while getting selfie'})
        
            try:
                face_count = face_detection.countFace(selfie)
            except:
                return Response({'code': '102', 'status': 'error', 'message': 'Error occurred while processing images. (INAVLID IMAGE)'})
            return Response({'code': '201', 'status': 'success', 'face_found': face_count})
        else:
            print('value of input [selfie] is not in the request')
        return Response({'status': 'error', 'message': 'invalid request'})