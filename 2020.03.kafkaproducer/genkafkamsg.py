# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os,json,time
tt=time.localtime()
faceidbatchtime=time.strftime("%Y%m%d%H%M%S", time.localtime())

def gendata(i,imgname1,imgname2):
    rec={
        "FaceListObject": {
            "Type": "",
            "FaceObject": [
                {
                    "FaceID": "31011577011218000105022020030314135900001",
                    "GenderCode": "",
                    "FaceAppearTime": "20200303141359",
                    "DeviceID": "31011577011218000105",
                    "SourceID": "1159077405",
                    "IsVictim": "1",
                    "SubImageList": {
                        "SubImageInfoObject": [
                            {
                                "Type": "11",
                                "StoragePath": "/ZNVFSIMG/group1/M00/00/00/CkhCvl5d9aiAfG8yAAA7NFaBKyk841.jpg",
                                "DeviceID": "31011577011218000105",
                                "ImageID": "",
                                "EventSort": "1",
                                "Data": "",
                                "Height": "0",
                                "ShotTime": "20200303141359",
                                "FileFormat": "",
                                "Width": "0"
                            },
                            {
                                "Type": "14",
                                "StoragePath": "/ZNVFSIMG/group1/M00/00/00/CkhCvl5d9aiAf3xBAAUryvbxCaY728.jpg",
                                "DeviceID": "31011577011218000105",
                                "ImageID": "",
                                "EventSort": "1",
                                "Data": "",
                                "Height": "0",
                                "ShotTime": "20200303141359",
                                "FileFormat": "",
                                "Width": "0"
                            }
                        ]
                    },
                    "LeftTopY": "0",
                    "LeftTopX": "0",
                    "FaceDisAppearTime": "20200303141359",
                    "IsSuspectedTerrorist": "0",
                    "IsDriver": "1",
                    "IsForeigner": "0",
                    "InfoKind": "1",
                    "RightBtmY": "0",
                    "IsCriminalInvolved": "0",
                    "RightBtmX": "0",
                    "IsDetainees": "0",
                    "IsSuspiciousPerson": "1",
                    "LocationMarkTime": "20200303141359",
                    "IDNumber": ""
                }
            ]
        }
    }
    
    devid="3101157701121800010%d"%(i%10)
    
    obj=rec['FaceListObject']['FaceObject'][0]
    obj['DeviceID']=devid
    obj["FaceID"]=devid+"02%s%05d"%(faceidbatchtime,i)
    shorttime=140000+i//60*100+i%60
    obj["FaceAppearTime"]="20200303"+str(shorttime)
    obj["FaceDisAppearTime"]="20200303"+str(shorttime+3)
    obj["LocationMarkTime"]=obj['FaceAppearTime']
    subimg=obj['SubImageList']['SubImageInfoObject']
    subimg[0]['StoragePath']='/capshot3000/'+imgname1
    subimg[1]['StoragePath']='/capshot3000/'+imgname2
    subimg[0]['DeviceID']=devid
    subimg[1]['DeviceID']=devid
    subimg[0]['ShotTime']=shorttime
    subimg[1]['ShotTime']=shorttime
    
    return rec





#生成img list, 据此构建随机数据， 其图片路径由此处路径文件名构成
imglist=os.listdir("../../../input/capshot3000/")
imgmap={}
for img in imglist:
    name=img[:-4]
    if len(name)>15:
        sname=name.split('_')
        smallimg=name
        bigimg='_'.join(sname[:3])
        imgmap[smallimg]=bigimg
#print(imgmap)

#连接kafka
producer = KafkaProducer(bootstrap_servers=['10.45.154.209:9092'])
seq=0
cnt=len(imgmap)
for small in imgmap.keys():
    rec=gendata(seq,small+".jpg",imgmap[small]+".jpg")
    devid="3101157701121800010%d"%(seq%10)
    seq=seq+1
    print("sending...")
    xx=producer.send("gangerstest0304",key= bytes(devid, encoding = "utf8") ,value=json.dumps(rec).encode('utf-8'))
    #xx=producer.send("gangertest",key= b'aaaaa' ,value=b'bbbbbbbbb')
    result = xx.get(timeout= 100)
    print(result)
print("finish send total records:",seq)
