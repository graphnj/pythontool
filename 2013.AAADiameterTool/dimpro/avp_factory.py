#coding:utf-8

from avp_integer32 import Integer32
from avp_integer64 import Integer64
from avp_unsigned32 import Unsigned32
from avp_unsigned64 import Unsigned64
from avp_octetstring import OctetString
from avp_float32 import Float32
from avp_float64 import Float64
from avp_grouped import Grouped

from avp_address import Address
from avp_time import Time
from avp_utf8string import UTF8String
from avp_diameteridentity import DiameterIdentity
from avp_enumerated import Enumerated
from avp_raw import RawType
from glo import g_dimcfg
from struct import unpack_from, unpack

import traceback

def create_avp(decode_buf   = None):
    '''根据传入的AVP_CODE或者AVP_BUF创建解析出AVP_CODE创建对应的AVP
    '''
    avp_data=""
    
    #print 'create_avp'

    if decode_buf:
        avp_code_and_vendorid = decode_avp_code(decode_buf)
    else:
        print 'decode_buf is None'
        raise 1,"decode_buf is None"

    #print 'create_avp for:', __my_avp_code
    # 获取对应AVP_CODE的配置
    __my_avp_cfg = g_dimcfg.get_avpconfig(avp_code_and_vendorid)

    print "create_avp my avp code:", avp_code_and_vendorid,'__my_avp_cfg', __my_avp_cfg
    
    
    # 创建对应的AVP实例
    para=[avp_code_and_vendorid, __my_avp_cfg,  decode_buf]
    if __my_avp_cfg[1] == 'Integer32':
        return Integer32(*para)
    elif __my_avp_cfg[1] == 'Integer64':
        return Integer64(*para)
    elif __my_avp_cfg[1] == 'Float32':
        return Float32(*para)
    elif __my_avp_cfg[1] == 'Float64':
        return Float64(*para)
    elif __my_avp_cfg[1] == 'Unsigned32':
        return Unsigned32(*para)
    elif __my_avp_cfg[1] == 'Unsigned64':
        return Unsigned64(*para)
    elif __my_avp_cfg[1] == 'OctetString':
        return OctetString(*para)
    elif __my_avp_cfg[1] == 'Grouped':
        return Grouped(*para)
    elif __my_avp_cfg[1] == 'Address':
        return Address(*para)
    elif __my_avp_cfg[1] == 'Time':
        return Time(*para)
    elif __my_avp_cfg[1] == 'UTF8String':
        return UTF8String(*para)
    elif __my_avp_cfg[1] == 'DiameterIdentity':
        return DiameterIdentity(*para)
    elif __my_avp_cfg[1] == 'Enumerated':
        return Enumerated(*para)
    elif __my_avp_cfg[1] == 'RawType':
        return RawType(*para)
    else:
        print 'sssss'
        raise 1,"unknown avp[%s] data type[%s]!" % (__my_avp_cfg[2], __my_avp_cfg[1])
    print 'end '
    
def decode_avp_code(avp_buf):
    '''从AVP_BUF中解析出来头部的AVP_CODE
    '''
    (my_avp_code,avp_length_flag, TempVendorID) = unpack_from("!LLL", avp_buf)
    avp_flag        = (avp_length_flag>>24)
    avp_length    = (avp_length_flag & 0x00FFFFFF)
    if (avp_flag & 0x80) > 0:       # 说明存在VENDER_ID
        if avp_length < 12:
            raise "The AVP Length less for min Len: 12!"
    else:
        if avp_length < 8:
            raise "The AVP Length less for min Len: 8!"
        TempVendorID=0
    print 'my_avp_code=', my_avp_code, "avp_flag=", avp_flag, "  avp_length=", avp_length,  '  VendorID=', TempVendorID
    return (my_avp_code, TempVendorID)
