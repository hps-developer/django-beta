from re import U
import cv2 as cv
import torch
import imutils
import sys
import os
from pathlib import Path
import requests

white = [255,255,255]
#path
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
save_path = Path(str(ROOT)+'/img_saver')
save_path_cropped = Path(str(save_path)+'/crop_p')

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))


class Cropper():
    def __init__(self,img_link,model):
        self.img_link = img_link
        self.model = model
    
    def crop(self):
        source = str(self.img_link)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        
        #get filename
        link_s = str(self.img_link).split('/')
        
        fn1 = link_s[-1].split('.')
        fn = Path(str(fn1[0]) + '.jpeg')
        #check url
        if is_url:
            r = requests.get(self.img_link, allow_redirects=True)
            #save url image
            complate_name = os.path.join(save_path, fn)
            #print(complate_name)
            open(complate_name, 'wb').write(r.content)
            imgcv = cv.imread(complate_name)
        else:
            imgcv = cv.imread(self.img_link)
            
        #pos, angle, confidence
        
        res = self.model(self.img_link)
        
        #check detection
        try:
            pos = res.xyxy[0][0][0:6].tolist()
        except:
            if is_url:
                del_pic = os.path.join(save_path,fn)
                os.remove(del_pic)
            return "ERROR no detection"
        
        #print(pos)
        #check confidence
        
        res_cp = None
        if pos[4] < 0.9:
            imgcv_copy = cv.copyMakeBorder(imgcv,20,20,20,20,cv.BORDER_CONSTANT,value=white)
            res_cp = os.path.join(save_path,str(fn1[0]) + 'copy.jpeg')
            cv.imwrite(res_cp, imgcv_copy)
            res1 = self.model(Path(str(save_path)+'/'+str(fn1[0]) + 'copy.jpeg'))
            try:
                pos = res1.xyxy[0][0][0:6].tolist()
            except:
                os.remove(res_cp)
                if is_url:
                    del_pic = os.path.join(save_path,fn)
                    os.remove(del_pic)
                return "ERROR no detection"
            if pos[4] < 0.9:
                os.remove(res_cp)
                if is_url:
                    del_pic = os.path.join(save_path,fn)
                    os.remove(del_pic)
                return 'ERROR low confidence'
            else:
                imgcv = imgcv_copy
                if is_url:
                    del_pic = os.path.join(save_path,fn)
                    os.remove(del_pic)
            
        
        #cal angle
        r_degree = int(pos[5])
        if r_degree >= 4:
            r_degree -=4
        rotate_angle = 90*r_degree
        
        #crop
        xmin,ymin,xmax,ymax = pos[0:4]
        cimg = imgcv[int(ymin):int(ymax), int(xmin):int(xmax)]
        
        #rotate
        rotated = imutils.rotate_bound(cimg, rotate_angle)
        
        #save
        complate_path = os.path.join(save_path_cropped, fn)
        cv.imwrite(complate_path, rotated)

        #delete non cropped pic form url
        if is_url:
            del_pic = os.path.join(save_path,fn)
            os.remove(del_pic)
            
        try:
            os.remove(res_cp)
        except:
            None
            
        return complate_path