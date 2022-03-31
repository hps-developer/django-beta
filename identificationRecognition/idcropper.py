from re import U
import cv2 as cv
import imutils
import os
from pathlib import Path
import requests
from mybend import settings



class Cropper():
    def __init__(self,img_link,model):
        self.img_link = img_link
        self.model = model
        
    def crop(self):
        source = str(self.img_link)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        fn = self.img_link
        

        #check url
        if is_url:
            link_s = str(self.img_link).split('/')
            fn1 = link_s[-1].split('.')
            fn = Path(str(fn1[0]) + '.jpeg')
            r = requests.get(self.img_link, allow_redirects=True)

            #save url image
            complate_name = os.path.join((settings.IMGU_PATH), fn)
            #print(complate_name)
            a = open(complate_name, 'wb')
            a.write(r.content)
            a.close()
            imgcv = cv.imread(complate_name)
            
            #pos, angle, confidence
            res = self.model(self.img_link)
        else:
            #pos, angle, confidence
            res = self.model(str(settings.IMGC_PATH)+'/'+self.img_link)
            imgcv = cv.imread(str(settings.IMGC_PATH)+'/'+self.img_link)
            
        

        
        #check detection
        try:
            pos = res.xyxy[0][0][0:6].tolist()
        except:
            if is_url:
                del_pic = os.path.join(settings.IMGU_PATH,fn)
                os.remove(del_pic)
            del imgcv
            del res
            raise Exception("ERROR no detection")
            
        
        #print(pos)
        #check confidence
        if pos[4] < 0.9:
            if is_url:
                del_pic = os.path.join(settings.IMGU_PATH,fn)
                os.remove(del_pic)
            del imgcv
            del res
            raise Exception("ERROR low confidence")
        
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
        complate_path = os.path.join(settings.IMG_PATH, fn)
        resized_image = cv.resize(rotated, (800, 500)) 
        cv.imwrite(complate_path, resized_image)

        #delete url
        if is_url:
                del_pic = os.path.join(settings.IMGU_PATH,fn)
                os.remove(del_pic)
     
        del imgcv
        del resized_image
        del rotated
        del cimg
        return complate_path