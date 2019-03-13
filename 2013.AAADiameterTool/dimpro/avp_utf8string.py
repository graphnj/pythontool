#coding:utf-8

from avp_octetstring import OctetString
from codecs import getencoder, getdecoder


class UTF8String(OctetString):
    '''
    UTF8String格式是从OctetString AVP基本格式导出的。
            该格式是使用ISO/IEC IS 10646－1字符集表示的可读的字符串，
            使用RFC 2279中描述的UTF-8转换格式，编码为一个OctetString。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        OctetString.__init__(self, avp_code, avp_cfg,  decode_buf)
            
    def after_decode_data(self):
        self.avp_value = self.avp_value.rstrip('\x00')
        
        u8decoder = getdecoder("utf_8")
        self.avp_value = str(u8decoder(self.avp_value)[0])

