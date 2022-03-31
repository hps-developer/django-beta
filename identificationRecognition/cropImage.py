import torch
from . import idcropper
def cropImageLocal(img):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'id_rec/yolov5/runs/train/exp9/weights/best.pt', force_reload=False)
    get_image = idcropper.Cropper(img,model)
    linku =  get_image.crop()
    del get_image
    del model
    return linku