#coding:utf-8

from avp import AVP

class Float64(AVP):
    '''
    该类型表示双精度浮点值，遵循IEEE标准754-1985中关于浮点的描述。
    该64比特值按网络字节顺序传送。AVP长度字段必须设置为16（如果“V”比特有效，则为20）。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        self.avp_format  = "!d"
        
