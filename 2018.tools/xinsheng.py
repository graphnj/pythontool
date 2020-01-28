# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 21:44:25 2018

@author: zhujinhua
"""




#coding:utf-8
import urllib
from bs4 import BeautifulSoup
import csv
import re
import sys,imp
imp.reload(sys)
import time
#sys.setdefaultencoding('utf-8')



#建立csv存储文件，wb写 a+追加模式
csvfile = open('xinshengurl.csv', 'a+',encoding='utf8',newline='')
writer = csv.writer(csvfile)




        
def getpage(urban,pagenum):
    for k in range(1,pagenum+1):
        #读取网页
        response = urllib.request.urlopen('http://xinsheng.huawei.com/cn/index.php?app=forum&mod=List&act=index&class=461&p='+str(k))
        the_page = response.read()
        #解析网页
        soup = BeautifulSoup(the_page,"lxml")
        
        list_title=[]
        list_author=[]
        list_url=[]
        list_view=[]
        list_reply=[]
        
        titlelist=soup.find_all(name="div", attrs={"class": re.compile("font_box")})
        for node in titlelist:
            t=node.find(name="div",attrs={"class": re.compile("title")}).find_all("a")
            for ahref in t:
                if ahref.attrs.get('title')!=None:
                    print(ahref.attrs)
                    print('title:'+ahref.attrs['title']+'  '+ahref.attrs['href'])
            
                    list_title.append(ahref.attrs['title'])
                    list_url.append(ahref.attrs['href'])
            
            t=node.find(name="div",attrs={"class": re.compile("pro")}).find("a")
            if t!=None:
                print('auth:'+re.sub('[\r\n \xa0]','',t.get_text()))
            else:
                print('auth is null')
            list_author.append(re.sub('[\r\n \xa0]','',t.get_text()))
            
            t=node.find(name="div",attrs={"class": re.compile("pro")}).find_all("span")
            if t!=None:
                print(len(t),t)
                print('view:'+t[0].get_text()+'  '+t[1].get_text())
                list_view.append(t[0].get_text())
                list_reply.append(t[1].get_text())
            else:
                print('view is null')
                list_view.append('')
                list_reply.append('')


        #将提取的数据合并
        data = []
        
        for i in range(0,40):
            print("i="+str(i))
            data.append((list_author[i],list_title[i], list_url[i],list_view[i],list_reply[i]))
        print(data)
        #将合并的数据存入csv
        writer.writerows(data)
        #csvfile.close()
        print("第" + str(k) + "页完成")
        time.sleep(3)
    
    
getpage('gulou', 100)
'''
#根据网页数设置范围
for urban in urbanlist.keys():
    print('Now get '+urban+' ',urbanlist[urban])
    getpage(urban, urbanlist[urban])
   ''' 