#coding:utf-8

from avp import AVP

class Unsigned64(AVP):
    '''
    64比特无符号整数，按照网络字节顺序。AVP长度字段必须设置为16（如果“V”比特有效，则为20）。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        self.avp_format  = "!Q"
        
