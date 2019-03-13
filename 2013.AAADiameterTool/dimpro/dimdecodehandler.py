#coding:utf-8

import json
from time import time
import re
import struct

from avp_factory import create_avp
from glo  import g_dimcfg

class CDimDecodeHandler(object):
    def __init__(self, dim_config):
        self.dmsg = {}
        self.DimVer                             = 0x01
        self.dmsg['DIM_HEADER_FLAG']            = 0x00
        self.dmsg['DIM_HEADER_FLAG_REQ']        = 0x00      #需要将读取配置文件中的对应设置
        self.dmsg['DIM_HEADER_FLAG_PROXIABLE']  = 0x00
        self.dmsg['DIM_HEADER_FLAG_ERROR']      = 0x00
        self.dmsg['DIM_HEADER_FLAG_TPOTENTIALLY'] = 0x00
        self.DimCMDCode         = 0x00
        
        self.DimAppID       = 1
        self.DimHopByHop     = 0x00
        self.DimEndToEnd     = 0x00
        

        self.ucDimPackBuf                   = None
        self.DimPackBufLen                  = 0x00

        self.DimAVPObj_list                   = []
        self.DimAVP_JSON                      = None
        self.DimMsgHeader_JSON                = None
        
    def __del__(self):
        #print 'CDimDecodeHandler del'
        del self.dmsg
        del self.DimAppID
        del self.DimHopByHop
        del self.DimEndToEnd
        del self.ucDimPackBuf
        del self.DimPackBufLen
        del self.DimAVPObj_list
        del self.DimAVP_JSON
        del self.DimMsgHeader_JSON
        

    def __str__(self):
        return self.DimAVP_JSON
      
        
    def unpack_json(self, pack_buf):
        '解压传入的buf，返回json串'
        self.unpack(pack_buf)
        print 'unpack_json'
        return self.DimAVP_JSON
    
    def unpack_head(self, pack_buf):
        '''解码包头内容'''
        offset_ = 0
        (ver_and_len,) = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        self.DimVer = ver_and_len >> 24
        
        self.DimPackBufLen  = ver_and_len & 0x00FFFFFF
        
        if len(pack_buf) != self.DimPackBufLen:
            raise "The Length Wrong In Msg Head!\n \
                    \tThe Real Length:[%d]\n \
                    \tThe Length In Msg Head:[%d]" \
                    % (len(pack_buf), self.DimPackBufLen)
        
        (flags_and_code,)  = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        self.dmsg['DIM_HEADER_FLAG'] = flags_and_code >> 24
        self.DimCMDCode  = flags_and_code & 0x00FFFFFF
        
        if self.dmsg['DIM_HEADER_FLAG'] & 0x80 >0:
            self.dmsg['DIM_HEADER_FLAG_REQ'] = 1
        else:
            self.dmsg['DIM_HEADER_FLAG_REQ'] = 0
            
        if self.dmsg['DIM_HEADER_FLAG'] & 0x40>0:
            self.dmsg['DIM_HEADER_FLAG_PROXIABLE'] = 1
        else:
            self.dmsg['DIM_HEADER_FLAG_PROXIABLE'] = 0
            
        if self.dmsg['DIM_HEADER_FLAG'] & 0x20>0:
            self.dmsg['DIM_HEADER_FLAG_ERROR'] = 1
        else:
            self.dmsg['DIM_HEADER_FLAG_ERROR'] = 0
            
        if self.dmsg['DIM_HEADER_FLAG'] & 0x10>0:
            self.dmsg['DIM_HEADER_FLAG_TPOTENTIALLY'] = 1
        else:
            self.dmsg['DIM_HEADER_FLAG_TPOTENTIALLY'] = 0
        
        (self.DimAppID,)   = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        (self.DimHopByHop,) = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        (self.DimEndToEnd,) = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        print 'Header:', self.DimAppID, self.DimHopByHop, self.DimEndToEnd
        self.generateHeaderJson()
        return offset_
    
    def generateHeaderJson(self):
        header_json=[]
        header_json.append({'Version':self.DimVer})
        header_json.append({'Length':self.DimPackBufLen})
        flag=''
        if self.dmsg['DIM_HEADER_FLAG_REQ']:
            flag+='R'
        if self.dmsg['DIM_HEADER_FLAG_PROXIABLE']:
            flag+='P'
        if self.dmsg['DIM_HEADER_FLAG_ERROR']:
            flag+='E'
        if self.dmsg['DIM_HEADER_FLAG_TPOTENTIALLY']:
            flag+='T'
        header_json.append({'FLAGS':str(self.dmsg['DIM_HEADER_FLAG'])+'['+flag+']'})
        header_json.append({'CMD CODE':str(self.DimCMDCode)+'['+g_dimcfg.get_cmdcodeconfig(self.DimCMDCode)+']'})
        header_json.append({'APP ID':str(self.DimAppID)+'['+g_dimcfg.get_appidconfig(self.DimAppID)+']'})
        header_json.append({'Hop By Hop':str(self.DimHopByHop)})
        header_json.append({'END to END':str(self.DimEndToEnd)})
        self.DimMsgHeader_JSON = json.dumps(header_json, indent=4)
        
        
        
    def unpack(self, pack_buf):

        self.ucDimPackBuf = pack_buf
        avp_pack_buf = ""
        
        # 解析包头
        offset = self.unpack_head(self.ucDimPackBuf)
        
        
        while offset != self.DimPackBufLen:
            # 确定具体需要解包的AVP BUF
            avp_pack_buf = self.ucDimPackBuf[offset:]
            zjhflag=0
            
            try:
                # 返回需要解析AVP的avp_object
                avp_object = create_avp(decode_buf = avp_pack_buf)
            except Exception, e:
                zjhflag=1
                print 'break now'
                break
            
            if zjhflag==0:
                # AVP解包，并且将解包后结果添加到self.DimAVPObj_list
                avp_object.decode()
                self.DimAVPObj_list.append(avp_object)
                
                # avp_length 4字节对齐
                lengthset = (avp_object.avp_length + 3) // 4 * 4
                
                offset += lengthset
        
        
        
        # 将AVP组合为需要返回的数据类型，之后装为json
        self.DimAVP_JSON = json.dumps(self.__compress_json_obj(self.DimAVPObj_list),  indent=4)

        #print 'unpack:', self.dmsg
        return self.dmsg
    
    def __compress_json_obj(self, avp_instance_list):
        '将实例列表转为json可以编辑的数据对象'
        _json_obj = []
        for avp in avp_instance_list:
            idwithName=repr(avp.avp_code)+'['+avp.cavp_name+']'
            if avp.avp_data_type == 'Grouped':
                _json_obj.append({idwithName:self.__compress_json_obj(avp.avp_subavpobj)})
            else:
                _json_obj.append({idwithName:avp.avp_value})
                
        return _json_obj
    
    
