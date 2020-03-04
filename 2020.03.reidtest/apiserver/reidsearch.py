import requests
import hashlib
import time
import matplotlib.pyplot as plt
import cv2,json,os
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
 
from datetime import timedelta
import base64,numpy as np
url = "http://10.45.154.64:9010/trajectory/reid/feature"

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
            
            
imginfo={}
def getfeature():

    #plt.figure(figsize=(15, 12)) 


    imgpath='../imgsmall/'
    imglist=os.listdir(imgpath)
    #imgname='1.jpg'
    seq=0
    featurearr=[]

    for i in imglist:
        imgname=imgpath+i
        #imgname='../../../input/imgsmall/2020-01-06-14-01-29S_569.jpg'
        files = {'imageData':open(imgname,'rb')}

        #data = {'enctype':'multipart/form-data','name':'wang'}

        reponse = requests.post(url,files=files)

        text = reponse.text
        rst=json.loads(text)['data'][0]['result']
        #print(imgname)
        #print(text)
        if type(rst)!= list and rst.get('errorMessage'):
            continue
        frame=cv2.imread(imgname)
        
        for rec in rst:
            rect=rec['rect']
            featurestr=rec['feature'][16:]

            t=base64.b64decode(featurestr)
            s=str(t,encoding = "utf-8").split(' ')
            feature=np.array(s).astype(np.float32)
            #print(feature.shape)
            #print(feature)
            featurearr.append(feature)
            #print(rect)
            #cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
            cv2.imwrite('tmp/%d.jpg'%seq,frame[rect[1]:rect[3],rect[0]:rect[2],:])
            imginfo[seq]={"name":i,"score":rec['quality'],"rect":rect}
            seq=seq+1
            print(seq)
    return np.array(featurearr)   

'''
featurearrnp=getfeature()
np.save('featurearrnp',featurearrnp)
imginfofile=open('imginfo.txt','w')
json.dump(imginfo,imginfofile)
imginfofile.close()
'''
print("ok")


imginfofile=open('imginfo.txt','r')
imginfo=json.load(imginfofile)

featurearrnp = np.load('featurearrnp.npy')
print('get feature finished! %d'%len(featurearrnp))

from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine

def search(imgfile):
    files = {'imageData':imgfile}
    time_start=time.time()
    response = requests.post(url,files=files)
    end=time.time()
    print("get feature use time:",end-time_start)
    text = response.text
    rst=json.loads(text)['data'][0]['result']
    if type(rst)!= list and rst.get('errorMessage'):
        return []
    
    
    rec=rst[0]
    rect=rec['rect']
    featurestr=rec['feature'][16:]
    import base64,numpy as np
    t=base64.b64decode(featurestr)
    s=str(t,encoding = "utf-8").split(' ')
    feature=np.array(s).astype(np.float32)
    

    cr=1-pairwise_distances([feature],featurearrnp, metric="cosine")
    return cr
    
    

#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST'])  # 添加路由
def upload():

    f = request.files['file']

    if not (f and allowed_file(f.filename)):
        return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

    user_input = request.form.get("name")
    print('get name:',user_input)
    #imgfile=open('tmp/1.jpg','rb')
    cr=search(f)
    sortimg = np.argsort(-cr[0]) 
    print(sortimg[:30])
    data=[]
    for imgidx in sortimg[:16]:
        inf=imginfo[str(imgidx)]
        x={'id':imgidx,'sim':cr[0][imgidx],'name':inf['name'],'score':inf['score'],'rect':inf['rect']}
        print(x)
        data.append(x)
    ret={'code':0,'data':data}
    return json.dumps(data, cls=NpEncoder)

    
@app.route('/')
def home():
    return render_template("index.html")
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=9999, debug=True)

