import idcropper
import os , os.path
import torch

path = '0c3dfbe7-fa49-42bc-8cdc-ef4b50e21b4b.jpeg'
model = torch.hub.load('ultralytics/yolov5','custom', path = '/home/itgl/Desktop/hipay/django-beta/id_rec/yolov5/runs/train/exp9/weights/best.pt', force_reload=False)

test = idcropper.Cropper(path,model)

linku = test.crop()

print(linku)