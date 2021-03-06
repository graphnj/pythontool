#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2010-9-13

@author: zdl
'''

from avp import AVP

class Integer32(AVP):
    '''
    32比特有符号整数，按照网络字节顺序。AVP长度字段必须设置为12（如果“V”比特有效，则为16）。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        self.avp_format = '!i'
        
