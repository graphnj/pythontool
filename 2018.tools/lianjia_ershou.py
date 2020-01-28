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
#sys.setdefaultencoding('utf-8')

urbanlist={'gulou':100,
       'jianye':61,
       'qinhuai':100,
       'xuanwu':59,
       'yuhuatai':28,
       'qixia':55,
       'jiangning':100,
       'pukou':100       
       }

#建立csv存储文件，wb写 a+追加模式
csvfile = open('lianjia_nj_ershou.csv', 'a+',encoding='utf8',newline='')
writer = csv.writer(csvfile)




        
def getpage(urban,pagenum):
    for k in range(10,pagenum+1):
        #读取网页
        response = urllib.request.urlopen('https://nj.lianjia.com/ershoufang/'+urban+'/pg'+str(k))
        the_page = response.read()
        #解析网页
        soup = BeautifulSoup(the_page,"lxml")
        list0=[]
        list1=[]
        listregion=[]
        listdesc=[]
        listflood=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        list6=[]
        #提取楼盘名称字段
        count=0
        for tag in soup.find_all(name="li", attrs={"class": re.compile("clear")}):
            count+=1
                #添加城市字段
            list0.append(urban)
            
            ta1 = tag.find(name="div",attrs={"class": re.compile("title")}).find("a")
            list1.append(ta1.string)
            
            
            #提取地址
            ta2 = tag.find(name="div", attrs={"class": re.compile("address")})
            t2 = ta2.find(name="a")
            if t2 != None:
                listregion.append(t2.string)
            else:
                listregion.append(0)  
                
            desc=ta2.find(name="div",attrs={"class":re.compile("houseInfo")})
            if desc!=None and len(desc)>=3:
                desc=desc.contents[2]
                listdesc.append(desc)
            else:
                listdesc.append(0)
                
                
            #提取建筑楼层
            ta2 = tag.find(name="div", attrs={"class": re.compile("positionInfo")})
            flood=ta2.contents[1]
            listflood.append(flood)
            t2 = ta2.find(name="a")
            if t2 != None:
                list2.append(t2.string)
            else:
                list2.append(0)
    
    
                
    
            #提取在售状态字段
            ta3 = tag.find(name="div", attrs={"class": re.compile("totalPrice")})
            list3.append(ta3.find(name="span").string)
            #提取每平米均价字段
            ta4 = tag.find(name="div", attrs={"class": re.compile("unitPrice")})
            list4.append(ta4.find(name="span").string)
        
       
        #将提取的数据合并
        data = []
        print(list0)
        print(list1)
        print(listregion)
        print(listdesc)
        print(list2)
        print(list3)
        print(list4)
        print(listflood)
    
        
        for i in range(0,count):
            print("i="+str(i))
            data.append((list0[i],list1[i], listregion[i],listdesc[i],list2[i], list3[i], list4[i], listflood[i]))
        print(data)
        #将合并的数据存入csv
        writer.writerows(data)
        #csvfile.close()
        print("第" + str(k) + "页完成")
    
    
getpage('gulou', 100)
'''
#根据网页数设置范围
for urban in urbanlist.keys():
    print('Now get '+urban+' ',urbanlist[urban])
    getpage(urban, urbanlist[urban])
   ''' 