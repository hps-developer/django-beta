import idcropper
import torch
import os , os.path

path = 'C:/Users/khmun/id_rec/final_test/idcard_data/idcard_test'

pic_list = []
file_txt = open('res_list.txt','a')

for f in os.listdir(path):
    ext = os.path.splitext(f)[-1]
    #print("TEST -- " + ext)
    #print(f)
    if ext.lower() in '.jpeg':
        pic_list.append(f)

print(pic_list)
file_txt.writalines('[')
file_txt.writelines()
file_txt.writalines(']')