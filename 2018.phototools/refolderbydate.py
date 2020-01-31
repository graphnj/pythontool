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
from PIL import Image
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
    print("stat time:",state)
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(state[-2]))+'C'

def compressImageByPIL(srcFile,dstFile):
    print(srcFile)
    sImg = Image.open(srcFile)
    exifinfo = sImg.info['exif'] if sImg.info.get('exif') else None
    w,h=sImg.size  
    print (w,h)
    if min(w,h)>2000:
        sImg=sImg.resize(((int)(w/2),(int)(h/2)),Image.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
    if exifinfo:
        sImg.save(dstFile, quality=80,exif=exifinfo)
    else:
        sImg.save(dstFile, quality=80)
    print (dstFile+" compressed succeeded")
def refolderByDate(path, dstPath):
    '''显示文件的属性。包括路径、大小、创建日期、最后修改时间，最后访问时间'''
    import time,os
    #遍历目录下的所有文件
    ii=0
    for root,dirs,files in os.walk(path,True):
        dirs[:] = []
        print("位置：" + root)
        
        for filename in files:
            fullfilename = os.path.join(root, filename)
            #如果文件名是 'jpg','png' 就处理，否则不处理
            f,e = os.path.splitext(filename)
            if e.lower() not in ('.jpg','.png','JPG',"jpeg"):
                print("new format:"+e)
                continue
            info = "文件名: " + filename + " "
            #文件的拍摄日期

            t = getDate( fullfilename )
            info = info + "拍摄时间：" + t + " "
            pwd = dstPath +'\\\\'+ t[0:7]
            dst = pwd + '\\\\' + t+e.lower()
            #按照图片的拍摄日期创建目录，把每个图片放到相应的目录中去
            if not os.path.exists(pwd ):
                os.mkdir(pwd)
            print('create new dir for info:'+info, 'dst:'+dst)
            
            #用 copy2 会保留图片的原始属性
            #shutil.copy2( fullfilename, dst )
            compressImageByPIL(fullfilename, dst)
            ii=ii+1
            print("count=",ii)
            #os.remove( filename )

if __name__ == "__main__":
    path = "V:\\photo\\20180603"
    paths=["V:\\xx整理\\unhandle\\weixin20200128","V:\\xx整理\\unhandle\\201806-202001"]
    dstPath='v:\\output'
    for path in paths:
        refolderByDate(path, dstPath)