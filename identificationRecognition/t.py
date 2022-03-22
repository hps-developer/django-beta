
import os , os.path

path = 'C:/Users/khmun/hipay/django-beta/images'

pic_list = []

for f in os.listdir(path):
    ext = os.path.splitext(f)[-1]
    #print("TEST -- " + ext)
    #print(f)
    if ext.lower() in '.jpeg':
        pic_list.append(f)

print(pic_list)
