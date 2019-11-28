# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:13:32 2018

@author: zhujinhua
"""


import sys
import os
import cv2
import dlib

input_dir = 'V:\\pic\\2018-05'

output_dir = './dataset/jing200'
size = 200

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()


def handledir(input_dir):
    print("handle dir "+input_dir)
    index = 1
    for (path, dirnames, filenames) in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.JPG'):
                print('Being processed picture %s' % index)
                img_path = path+'/'+filename
                print(img_path)
                # 从文件读取图片
                img = cv2.imread(img_path)
                # 转为灰度图片
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # 使用detector进行人脸检测 dets为返回的结果
                dets = detector(gray_img, 1)
    
                #使用enumerate 函数遍历序列中的元素以及它们的下标
                #下标i即为人脸序号
                #left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离 
                #top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
                for i, d in enumerate(dets):
                    w=d.width()
                    h=d.height()
                    print("d=",d,w,h)
                    x1 = d.top()-(int)(h*0.1) if d.top()-(int)(h*0.1) > 0 else 0
                    y1 = d.bottom()+(int)(h*0.1) if d.bottom()+(int)(h*0.1) < gray_img.shape[0] else gray_img.shape[0]
                    x2 = d.left()-(int)(w*0.1) if d.left()-(int)(w*0.1) > 0 else 0
                    y2 = d.right()+(int)(w*0.1) if d.right()+(int)(w*0.1) < gray_img.shape[1] else gray_img.shape[1]
                    # img[y:y+h,x:x+w]

                    print("width:",x2,y2,w,"height:",x1,y1,h)
                    face = img[x1:y1,x2:y2]
                    # 调整图片的尺寸
                    face = cv2.resize(face, (size,size))
                    cv2.imshow('image',face)
                    # 保存图片
                    cv2.imwrite(output_dir+'/'+filename[:-4]+'-'+str(i)+'.jpg', face)
                    index += 1
    
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    sys.exit(0)

handledir(input_dir)
'''
for (path, dirnames, filenames) in os.walk(input_dir):
    print(path,";",dirnames,";",filenames)
    for dirname in dirnames:
        print("handle dir "+dirname)
        dirfullname=os.path.join(input_dir, dirname)
        handledir(dirfullname)
        '''