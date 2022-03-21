import idcropper_addframe
import torch
import os , os.path

path = 'C:/Users/khmun/id_rec/final_test/idcard_data/idcard_test'
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'yolov5/runs/train/exp9/weights/best.pt', force_reload=False)

file_txt = open('res.txt','a')

cnt = 0
cnt_det = 0
cnt_non = 0
for f in os.listdir(path):
    cnt+=1
    ext = os.path.splitext(f)[1]
    #print("TEST -- " + ext)
    #print(f)
    if ext.lower() in '.jpeg':
        test = idcropper_addframe.Cropper(path + '/' + f,model)
        linku =  test.crop()
        if linku.lower().split('.')[-1] in 'jpeg':
            cnt_det += 1
            file_txt.writelines(linku + ' -> ' + 'YES\n')
        else:
            file_txt.writelines(f + ' -> ' + linku + '\n')
        #print(linku)
    else:
        cnt_non += 1
        file_txt.writelines(f + ' -> ' + 'Not jpeg\n')


file_txt.writelines('pic = ' + str(cnt) + '\n')
file_txt.writelines('pic det = ' + str(cnt_det) +'\n')
file_txt.writelines('non jpeg = ' +str(cnt_non)+'\n')