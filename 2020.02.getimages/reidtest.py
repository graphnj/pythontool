


import requests
import hashlib
import time
import cv2,json

url = "http://10.45.154.64:9010/trajectory/reid/feature"

imgname='3.jpg'

files = {'imageData':open(imgname,'rb')}

#data = {'enctype':'multipart/form-data','name':'wang'}

reponse = requests.post(url,files=files)

text = reponse.text
rst=json.loads(text)['data'][0]['result']
#print(rst)
frame=cv2.imread(imgname)
for rec in rst:
    rect=rec['rect']
    print(rect)
    cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 2)
#print (text)
cv2.imshow('reid body detect',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
