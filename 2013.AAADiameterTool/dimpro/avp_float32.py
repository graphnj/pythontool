#coding:utf-8

from avp import AVP

class Float32(AVP):
    '''
    该类型表示单精度浮点数，遵循IEEE标准754-1985中关于浮点的描述。
    该32比特值按网络字节顺序传送。AVP长度字段必须设置为12（如果“V”比特有效，则为16）。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        self.avp_format  = "!f"
        
