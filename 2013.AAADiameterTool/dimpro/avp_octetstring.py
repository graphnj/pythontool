#coding:utf-8

from avp import AVP
from binascii import a2b_hex, b2a_hex
class OctetString(AVP):
    '''
    该数据包含任意可变长的数据。除非另外注明，
    AVP长度字段必须至少设置为8（如果“V”比特有效，则为12）。
    这种类型的AVP值的长度如果不是4个八位组的倍数，应按照需要填充，
    这样下一个AVP（如果有）才能够在一个32比特边界开始。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        # 根据self.avp_length进行判断
        #print 'oct set_avp_operator_type'
        if self.iavp_vendorid == 0x00:
            __data_length = self.avp_length - 8
        else:
            __data_length = self.avp_length - 12
                
        self.avp_format = "!" + str(__data_length) + "s"
        #print "avp_format=", self.avp_format
        
    def after_decode_data(self):
        self.avp_value = self.avp_value.rstrip('\x00')
        
