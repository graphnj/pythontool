#coding:utf-8

import re
import os
from PyQt4.QtGui import QMessageBox
class DIM_CFG(object):
    '''配置文件处理类'''
    def __init__(self):
        self.re_str = re.compile("\$")
        self.AVPCFG={}
        self.APPCFG={}
        self.CMDCFG={}
        
        self.refresh()

       
                
    def refresh(self):
        try:
            fh = open("./config/cfg.ini", "r")
        except:
            print "Error!   open  './config/cfg.ini' fail"
            os.system('pause')
            exit(0)
        
        linenum=0    
        for eachline in fh:
            # 格式化行信息
            linenum+=1
            line_list = self.re_str.split(eachline)
            line_list=[ss.strip() for ss in line_list]
            if len(line_list)<3:
                print 'config line (%d:%s ) vacant or error, continue'%(linenum, eachline.strip())
                continue
            if (line_list[0] == "AVP") and (len(line_list)<4):
                print 'AVP config line (%d:%s ) vacant or error, continue'%(linenum, eachline.strip())
                continue
                
            self.re_num2num=re.compile('\-')
            #处理范围如123-156,将会对每一个都插入配置中
            num1_to_num2=self.re_num2num.split(line_list[1])
            if len(num1_to_num2)>1:
                for n in range(int(num1_to_num2[0]),  int(num1_to_num2[1])+1):
                    self.initcfg(line_list, n)                 
            else:
                self.initcfg(line_list, int(line_list[1]))
        #print 'AVPCFG:', self.AVPCFG    
        fh.close()
        
    def initcfg(self, line_list, id):
        #通过每行的第一个word确定该行的配置类型
        #print 'initcfg:', line_list[0], id, line_list[2]
        if line_list[0] == "AVP":
            #line_list[2]:name line_list[3]:valueType  line_list[4]:vendorid
            vendorid=0
            try:
                vendorid=int(line_list[4])
            except:
                vendorid=0
            self.AVPCFG[(int(id), vendorid)] = [line_list[2], line_list[3]]
        elif line_list[0]=="CMD":
            self.CMDCFG[int(id)] = line_list[2]
        elif line_list[0]=="APP":
            self.APPCFG[int(id)] = line_list[2]


    def __del__(self):
        print 'dim_config del'
        del self.AVPCFG
        del self.APPCFG
        del self.CMDCFG
        
    def get_avpconfig(self, avp_code=None):
        try:
            #print 'get avp cfg:', avp_code,   self.AVPCFG[int(avp_code)]
            return self.AVPCFG[avp_code]
        except KeyError:
            print "no this avp(%d,%d) in config!" % (avp_code[0], avp_code[1])
            return self.AVPCFG[(0, 0)]

    def get_appidconfig(self, appid=None):
        try:
            #print 'get avp cfg:', avp_code,   self.AVPCFG[int(avp_code)]
            return self.APPCFG[appid]
        except KeyError:
            print "no this avp(%d) in config!" % (appid)
            return self.APPCFG[100]
            
    def get_cmdcodeconfig(self, cmdcode=None):
        try:
            #print 'get avp cfg:', avp_code,   self.AVPCFG[int(avp_code)]
            return self.CMDCFG[cmdcode]
        except KeyError:
            print "no this avp(%d) in config!" % (cmdcode)
            return self.CMDCFG[0]
