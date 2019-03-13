#coding:utf-8

from avp import AVP
import avp_factory

class Grouped(AVP):
    '''该数据字段定义为一个AVP序列。这些AVP按其定义的顺序排列，
            每一个都包括它们的头和填充位。AVP长度字段值设置为8（如果“V”比特有效，则为12），
            加上所有序列内的AVP的长度总和。因此Grouped类型的AVP的AVP长度字段总是4的倍数。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        AVP.__init__(self, avp_code, avp_cfg,  decode_buf)
        
    def set_avp_operator_type(self):
        pass
        
    
        
    def decode_data(self, offset):
        '''重载，将AVP_BUF多次进行解析'''
        offset_ = offset
        self.avp_value = []
        while offset_ < self.avp_length:
            sub_buf_ = self.avp_decodebuf[offset_:]
            avp_object = avp_factory.create_avp(sub_buf_)
            avp_object.decode()
            self.avp_subavpobj.append(avp_object)
            self.avp_value.append(repr({repr(avp_object.avp_code):avp_object.avp_value}))
            
            # avp_length 4字节对齐
            lengthset = (avp_object.avp_length + 3) // 4 * 4
            
            offset_ += lengthset
            
