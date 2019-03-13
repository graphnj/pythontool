#coding:utf-8

from socket import AF_INET, AF_INET6, getaddrinfo, inet_aton, inet_ntoa

from avp_octetstring import OctetString
from struct import unpack_from

class Address(OctetString):
    '''
            地址格式是从OctetString AVP基本格式导出的。它与其它数据格式不同，例如需要
            区分32比特（IPV4）或128比特（IPV6）地址。地址AVP的头两个八位组为AddressType，
            其包含一个在［IANA的“地址簇号码”］中定义的地址簇。AddressType用来区别剩下
            八位组的内容和格式。
    IANA的“地址簇号码”的定义参见:
    http://www.iana.org/assignments/address-family-numbers/address-family-numbers.xml
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        OctetString.__init__(self, avp_code, avp_cfg,  decode_buf)
        

            
    def set_avp_operator_type(self):
        '''需要根据不同的数据长度来设置解码格式'''
        # 根据self.avp_length进行判断
        print 'set_avp_operator_type'
        if self.iavp_vendorid == 0x00:
            __data_length = self.avp_length - 10
        else:
            __data_length = self.avp_length - 14
                
        self.avp_format = "!h" + str(__data_length) + "s"
            

        
    def decode_data(self, offset):
        '''解码AVP包体数据
                     返回本次解码AVP包的总长度
        '''
        
        (self.avp['AVP_ADDR_FAMILY'], self.avp_value) \
            = unpack_from(self.avp_format, self.avp_decodebuf, offset)

        self.after_decode_data()
        
        return self.avp_length
    
    def after_decode_data(self):
        if self.avp['AVP_ADDR_FAMILY'] == 1:
            self.avp_value = self.avp_value[:4]
        elif self.avp['AVP_ADDR_FAMILY'] == 2:
            self.avp_value = self.avp_value[:16]

        self.avp_value = inet_ntoa(self.avp_value)
        

