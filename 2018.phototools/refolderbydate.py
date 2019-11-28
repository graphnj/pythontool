# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:43:13 2018

@author: zhujinhua
"""

#coding: gbk

import shutil
import os
import stat
import time
##图像的exif,百度知道:http://baike.baidu.com/view/22006.htm
import exifread as exif

def getDate(filename):
    try:
        fd = open(filename, 'rb')
    except:
        raise "unopen file[%s]\\n" % filename 
    data = exif.process_file( fd )
    if data:
        #获取图像的 拍摄日期
        try:
            t = data['EXIF DateTimeOriginal']
            #转换成 yyyy-mm-dd 的格式
            return str(t).replace(":","-").replace(" ","-")[:20]+'S'
        except:
            pass
    #如果没有取得 exif ，则用图像的创建日期，作为拍摄日期
    state = os.stat(filename)
    return time.strftime("%Y-%m-%d", time.localtime(state[-2]))+'C'

def refolderByDate(path):
    '''显示文件的属性。包括路径、大小、创建日期、最后修改时间，最后访问时间'''
    import time,os
    #遍历目录下的所有文件
    for root,dirs,files in os.walk(path,True):
        dirs[:] = []
        print("位置：" + root)
        
        for filename in files:
            fullfilename = os.path.join(root, filename)
            #如果文件名是 'jpg','png' 就处理，否则不处理
            f,e = os.path.splitext(filename)
            if e.lower() not in ('.jpg','.png','JPG'):
                continue
            info = "文件名: " + filename + " "
            #文件的拍摄日期
            t = getDate( fullfilename )
            info = info + "拍摄时间：" + t + " "
            pwd = 'v:\\zhujingyidate2' +'\\\\'+ t[0:7]
            dst = pwd + '\\\\' + t+e.lower()
            #按照图片的拍摄日期创建目录，把每个图片放到相应的目录中去
            if not os.path.exists(pwd ):
                os.mkdir(pwd)
                print('info:'+info, 'dst:'+dst)
            
            #用 copy2 会保留图片的原始属性
            shutil.copy2( fullfilename, dst )
            #os.remove( filename )

if __name__ == "__main__":
    path = "V:\\photo\\20180603"
    paths=["V:\\xx待整理\\20190601"]
    for path in paths:
        refolderByDate(path)