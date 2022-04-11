import cv2 as cv
import pytesseract
import os
import numpy as np
from pathlib import Path
import requests
from mybend import settings

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
custom_config = r'-l eng+mon --psm 6'

#image enhancement
def imgToGray_local(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)
    divide = cv.divide(gray, blur, scale=150)
    return divide

def blurred_local(img):
    kernel = np.array([[-1,-1,-1], 
                       [-1, 9,-1],
                       [-1,-1,-1]])
    sharpened = cv.filter2D(img, -1, kernel)
    res = imgToGray_local(sharpened)
    return res

#get data
def get_data_local(img):
    data = pytesseract.image_to_data(img, config = custom_config,output_type='data.frame')
    return data

#list to str
def list_to_string_local(list):
    res = ''
    for i in list:
        res += i +' '
    return res

#find family name -> line
def get_line_local(lines):
    cnt_line = 0
    for i in lines:
        str = list_to_string_local(i).lower()
        if {'овог','family','өвөг'} & set(str.split()):
            cnt_line+=1
            break
        cnt_line+=1
    return cnt_line

#get family name
def get_family_name_local(line,conf):
    res_str = ''
    for i in range(len(line)):
        if conf[i] > 90:
            res_str+=line[i]+' '
            
    check = 'qwertyuiop[]\|asdfghjkl;\'zxcvbnm,./QWERTYUIOP\{\}ASDFGHJKL:"ZXCVBNM<>?/ 1234567890-=`~!@#$%^&*()_+§'
    res_str = res_str.strip(check)
    list = ['Хүйс', 'Регистрийн', 'дугаар', 'Төрсөн', 'он', 'сар','өдөр']
    if(len(res_str) == 0): 
        return ''
    if res_str[0].islower():
        return ''
    test = res_str.split(' ')
    res = ""
    for i in (test):
        i = i.strip(check)
        if not i.isupper() and not i in list:
            res+= i + ' '
    
    res_str = res.strip(check)
    return res_str

class Getu_data():
    def __init__(self,img_link):
        self.img_link = img_link

    def data(self):
        source = str(self.img_link)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        name = str(self.img_link).split('/')
        fn1 = name[-1].split('.')
        fn = Path(str(fn1[0]) + '.jpeg')
        #check url
        if is_url:
            r = requests.get(self.img_link, allow_redirects=True)

            #save url image
            complate_name = os.path.join((settings.IMG_PATH), fn)
            #print(complate_name)
            a = open(complate_name, 'wb')
            a.write(r.content)
            a.close()
            res = self.image_to_text(settings.IMG_PATH+'/'+complate_name)
            del_pic = os.path.join(settings.IMG_PATH+'/'+fn)
            os.remove(del_pic)
        else:
            res = self.image_to_text(str(settings.IMG_PATH)+'/'+str(fn))
        return res
         
    def image_to_text(self, link):
        try:
            img = cv.imread(link)
            id_img = imgToGray_local(img)
            data = get_data_local(id_img)
            data = data[data.conf != -1]
            lines = data.groupby('line_num')['text'].apply(list)
            conf = data.groupby('line_num')['conf'].apply(list)
            #print(data)
            family_name_line = get_line_local(lines)
            
            #when blurred it will work
            if family_name_line == len(lines):
                id_img = blurred_local(img)
                data = get_data_local(id_img)
                
                data = data[data.conf != -1]
                lines = data.groupby('line_num')['text'].apply(list)
                conf = data.groupby('line_num')['conf'].apply(list)
                
                family_name_line = get_line_local(lines)
                if family_name_line == len(lines):
                    return 'Didn\'t find family name\'s line'
            
            res = get_family_name_local(lines[family_name_line+1],conf[family_name_line+1])
            if len(res) > 1:
                return res
            else:
                return 'Didn\'t find family name'
        except Exception as er:
            return type(er).__name__, er.__traceback__.tb_lineno