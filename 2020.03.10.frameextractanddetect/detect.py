import requests
import hashlib
import time
import matplotlib.pyplot as plt
import cv2,json,os
#plt.figure(figsize=(15, 12)) 
url = "http://10.45.154.64:9010/trajectory/reid/feature"
url="http://10.45.154.129/verify/face/detectAndQuality"
url="http://10.45.154.64:9010/verify/face/detect"


fdetectlog=open('africadetectznv.log','w')

def detectface_znv(seq,imgname,isShowImg=False):
    files = {'imageData':open(imgname,'rb')}

    #data = {'enctype':'multipart/form-data','name':'wang'}

    reponse = requests.post(url,files=files)

    text = reponse.text
    #print(text)
    text=json.loads(text)
    if text['result']=='error':
        print(text)
        return
    rst=text['data'][0]['result']
    fname=imgname.split('/')[-1][:-4]
    frame=cv2.imread(imgname)
    if rst==None:
        ss=fname+" detect face:none!"
        print(ss)
        fdetectlog.write(ss+'\n')
        return 
    ss=fname+" detect face:%d"%len(rst)+str(rst)
    print(ss)
    fdetectlog.write(ss+'\n')
    cnt=0
    for rec in rst:
        rect=rec['rect']
        #featurestr=rec['feature']
        #if rec['quality']<0.99:
        #    continue
        #feature=base64Tofloat(featurestr)
        #print(feature.shape)
        #print(feature)
        #featurearr.append(feature)
        #print(rect)
        #cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
        rect0=0 if rect[0]-20<0 else rect[0]-20
        rect1=0 if rect[1]-20<0 else rect[1]-20
        rect2=frame.shape[1] if rect[2]+20>frame.shape[1] else rect[2]+20
        rect3=frame.shape[0] if rect[3]+20>frame.shape[0] else rect[3]+20
        
        #cv2.imwrite('africa/%s-%d.jpg'%(fname,cnt),frame[rect[1]:rect[3],rect[0]:rect[2],:])
        cv2.imwrite('africa-znv/%s-face-%d.jpg'%(fname,cnt),frame[rect1:rect3,rect0:rect2,:])
        #imginfo[seq]={"name":i,"score":rec['quality'],"rect":rect}
        cnt=cnt+1

    for rec in rst:
        rect=rec['rect']
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
    
    cv2.imwrite('africa-znv/%s-rect.jpg'%fname,frame)


    #print (text)
    if isShowImg:
        im2 = frame[:,:,::-1]
        #recx=rst[3]['rect']
        plt.figure(figsize=(40,80))
        plt.imshow(im2)



import dlib
dlibdetector = dlib.get_frontal_face_detector()
def detectface_dlib(seq,imgname,isShowImg=False):
    fname=imgname.split('/')[-1][:-4]
    frame=cv2.imread(imgname)

    dets = dlibdetector(frame, 1)
    if dets==None:
        ss=fname+" detect face:none!"
        print(ss)
        fdetectlog.write(ss+'\n')
        return 
    ss=fname+" detect face:%d"%len(dets)+str(dets)
    print(ss)
    fdetectlog.write(ss+'\r\n')
    fdetectlog.flush()
    print("Number of faces detected: {}".format(len(dets)))
    cnt=0
    for i, d in enumerate(dets):
        #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #    i, d.left(), d.top(), d.right(), d.bottom()))
        rect0=0 if d.left()-20<0 else d.left()-20
        rect1=0 if d.top()-20<0 else d.top()-20
        rect2=frame.shape[1] if d.right()+20>frame.shape[1] else d.right()+20
        rect3=frame.shape[0] if d.bottom()+20>frame.shape[0] else d.bottom()+20
        
        #cv2.imwrite('africa/%s-%d.jpg'%(fname,cnt),frame[rect[1]:rect[3],rect[0]:rect[2],:])
        cv2.imwrite('africa-dlib/%s-face-%d.jpg'%(fname,cnt),frame[rect1:rect3,rect0:rect2,:])
        #imginfo[seq]={"name":i,"score":rec['quality'],"rect":rect}
        cnt=cnt+1

    for i, d in enumerate(dets):
        cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 0), 2)
    
    cv2.imwrite('africa-dlib/%s-rect.jpg'%fname,frame)
    
        #print (text)
    if isShowImg:
        im2 = frame[:,:,::-1]
        #recx=rst[3]['rect']
        plt.figure(figsize=(40,80))
        plt.imshow(im2)        
        
        
        
        
        
# 正式代码 
imgpath='../../input/africaimages/'
imglist=os.listdir(imgpath)
#imgname='1.jpg'
seq=0
featurearr=[]
imginfo={}
for imgfname in imglist:
    imgname=imgpath+imgfname
    #imgname='../../../input/imgsmall/2020-01-06-14-01-29S_569.jpg'
    detectface_znv(seq,imgname)
    #print(imgfname)
