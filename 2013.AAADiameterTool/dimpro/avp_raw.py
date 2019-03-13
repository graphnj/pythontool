#coding:utf-8

from avp_octetstring import OctetString
from binascii import a2b_hex, b2a_hex
class RawType(OctetString):
    '''
    该数据包含任意可变长的数据。除非另外注明，
    AVP长度字段必须至少设置为8（如果“V”比特有效，则为12）。
    这种类型的AVP值的长度如果不是4个八位组的倍数，应按照需要填充，
    这样下一个AVP（如果有）才能够在一个32比特边界开始。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        OctetString.__init__(self, avp_code, avp_cfg,  decode_buf)
        

    def after_decode_data(self):
        self.avp_value = '0x'+b2a_hex(self.avp_value.rstrip('\x00'))

        
