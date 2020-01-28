# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 00:34:32 2018

@author: zhujinhua
"""

import numpy as np

import pandas as pd


from wordcloud import WordCloud
import codecs
import jieba
#import jieba.analyse as analyse
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


houseraw=pd.read_csv('lianjia_nj_ershou.csv')




comment_text = houseraw['recommand']
print (comment_text.values)
wordlist=[]
print(type(comment_text.values))
for line in comment_text.values:
    wordlist.extend(line.split())

print(wordlist)

cut_text = " ".join(wordlist)
cloud = WordCloud(
    #设置字体，不指定就会出现乱码
    font_path="simkai.ttf",
    width=1000, height=860, margin=2,
    #font_path=path.join(d,'simsun.ttc'),
    #设置背景色
    background_color='white',
    #词云形状
    #mask=color_mask,
    #允许最大词汇
    max_words=1000,
    #最大号字体
    max_font_size=40
)
word_cloud = cloud.generate(cut_text) # 产生词云
word_cloud.to_file("pjl_cloud4.jpg") #保存图片

#  显示词云图片
plt.imshow(word_cloud)
plt.axis('off')
plt.show()