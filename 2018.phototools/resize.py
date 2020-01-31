#coding:utf-8
from PIL import Image
import os

#图片压缩批处理  
def compressImage(srcPath,dstPath):  
    for filename in os.listdir(srcPath):  
        #如果不存在目的目录则创建一个，保持层级结构
        if not os.path.exists(dstPath):
                os.makedirs(dstPath)        

        #拼接完整的文件或文件夹路径
        srcFile=os.path.join(srcPath,filename)
        dstFile=os.path.join(dstPath,filename)
        print (srcFile)
        print (dstFile)

        #如果是文件就处理
        if os.path.isfile(srcFile):     
            compressImageByPIL(srcFile,dstFile)

        #如果是文件夹就递归
        if os.path.isdir(srcFile):
            compressImage(srcFile,dstFile)

       
def compressImageByPIL(srcFile,dstFile):
    print(srcFile)
    sImg = Image.open(srcFile)
    exifinfo = sImg.info['exif'] if sImg.info.get('exif') else None
    w,h=sImg.size  
    print (w,h)
    if min(w,h)>2000:
        sImg=sImg.resize(((int)(w/2),(int)(h/2)),Image.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
    if exifinfo:
        sImg.save(dstFile, quality=90,exif=exifinfo)
    else:
        sImg.save(dstFile, quality=90)
    print (dstFile+" compressed succeeded")
        
        
if __name__=='__main__':  
    compressImage("V:\\zxxdate","v:\\xxbaiduarch")
