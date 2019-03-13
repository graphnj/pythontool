#coding:utf-8

from avp_integer32 import Integer32

class Enumerated(Integer32):
    '''
    Enumerated是从Integer32 AVP基本格式导出的。该定义包含一个有效值的列表
        及相关解释，并在引入该AVP的Diameter应用中有所描述。
    
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        Integer32.__init__(self, avp_code, avp_cfg,  decode_buf)
        
