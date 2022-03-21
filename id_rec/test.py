
import cv2 as cv
import torch
import matplotlib.pyplot as plt
import numpy as np
import imutils
import os
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
save_path = Path(str(ROOT)+'/img_saver')

model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'yolov5/runs/train/exp8/weights/best.pt', force_reload=True)

img = "C:/Users/khmun/id_rec/final_test/idcard_data/idcard_test/06a3c82a-4433-49cb-a220-2833ad7ef3aa.jpeg"

imgcv = cv.imread(img)
res = model(img)
res.print()
white = [0,0,0]
imgcv_copy = cv.copyMakeBorder(imgcv,50,50,50,50,cv.BORDER_CONSTANT,value=white)

link_s = str(img).split('/')
fn1 = link_s[-1].split('.')
fn = Path(str(fn1[0]) + '.jpeg')
res_cp = os.path.join(save_path,str(fn1[0]) + 'copy.jpeg')
cv.imwrite(res_cp, imgcv_copy)
res = model(Path(str(save_path)+'/'+str(fn1[0]) + 'copy.jpeg'))
res.print()
imgcv = imgcv_copy
imgcv = cv.imread(img)

#coor = res.pandas().xyxy[0]
#print(coor)
#res.pandes().xyxy[0].sort_values('confidence')
test = res.xyxy[0][0][0:6].tolist()
print(test[4])
if test[4] < 0.8:
    print("ERROR")
    
    
xmin,ymin,xmax,ymax = test[0:4]
#print(xmin)
print(xmin,ymin,xmax,ymax)

#cal angle
r_degree = int(test[5])
if r_degree >= 4:
    r_degree -=4
rotate_angle = 90*r_degree
#print(rotate_angle)

#crop
cimg = imgcv[int(ymin):int(ymax), int(xmin):int(xmax)]

#rotate

rotated = imutils.rotate_bound(cimg, rotate_angle)



cv.imshow("crop", cimg)
cv.imshow("rotated",rotated)
cv.waitKey(0)