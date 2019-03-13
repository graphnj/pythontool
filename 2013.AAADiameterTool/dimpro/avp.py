
#coding:utf-8
'''
zhu.jinhua 20130214
Format	C Type			Python type		Standard size	Notes
x		pad byte		no value	 	 
c		char			    string of length 1	1	 
b		signed char		integer				1	
B		unsigned char	integer				1	
?		_Bool			    bool				    1	
h		short			    integer				2	
H		unsigned short	integer				2	
i		int				    integer				4	
I		unsigned int	integer				4	
l		long			    integer				4	
L		unsigned long	integer				4	
q		long long		integer				8	
Q		unsigned long long	integer		8	
f		float			    float				    4	
d		double			float				    8	
s		char[]			string	 	 
p		char[]			string	 	 
P		void *			integer	 			
'''

import traceback
from glo import g_dimcfg
import struct

class AVP(object):
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        self.avp = {}
        self.avp_code                   = avp_code
        self.avp_flag          = 0x00
        self.avp_length        = 0x00
        self.avp_value          = ""
        self.iavp_flag_exist_vendorid = 0
        self.iavp_flag_mandatory     = 0x00
        self.iavp_flag_private       = 0x00
        self.iavp_vendorid     = 0x00

        self.avp_decodebuf           = decode_buf
        self.avp_data_type              = ""
        self.avp_format                 = ""
        self.avp_subavpobj           = []
        self.cavp_name          = ""
        
        # 根据传入的 AVP_CODE 获取相应的配置信息
        self.my_avp_cfg = avp_cfg
        self.cavp_name = self.my_avp_cfg[0]
    
    '''    
    def __del__(self):
        del self.avp
        del self.avp_code
        del self.avp_data_type
        del self.avp_decodebuf
        del self.my_avp_cfg
'''

    def __repr__(self):
        print 'avp repr !!!!!!!!!!!!!!!!'
        return repr({repr(self.avp_code):self.avp_value})
        
    def __str__(self):
        return self.__repr__()
    
        
    def set_avp_type(self):
        '设置AVP的数据类型'
        self.avp_data_type = self.my_avp_cfg[1]
        
    def set_avp_operator_type(self):
        print 'sub class set'
        raise 1, "Unknow AVP Type, Can Not Use set_avp_operator_type!"
    
    def decode(self, offset=0):
        '''解码AVP包, 返回所解码包的PACK_BUF'''
        #print 'decode'
        offset_ = offset
        offset_ += self.decode_head(offset_)
        
        print 'len(self.avp_decodebuf) %d, self.avp_length %d'%(len(self.avp_decodebuf) , self.avp_length)
        # 校验AVP_LENGTH是否合法
        if len(self.avp_decodebuf) < self.avp_length:
            raise "Decode AVP_CODE[%s] Error: The Length In BUF Is Wrong!\nReal Length:[%d]\nPack BUF Length:[%d]" % \
                    (avp_code[0], len(self.avp_decodebuf), self.avp_length)
        
        #print "self.avp_length=",self.avp_length
        buf_length = (self.avp_length + 3) // 4* 4
        #print "buf_length=",buf_length
        self.avp_decodebuf = self.avp_decodebuf[offset:buf_length]
        
        # 设置解析数据类型
        self.set_avp_type()
        
        # 设置解析操作类型
        self.set_avp_operator_type()
        
        #print 'before avp decode_data'
        # 对数据进行解码
        self.decode_data(offset_)
        #print 'end avp decode'
             
        return self.avp
    
    def decode_head(self, offset=0):
        '''解码AVP头
                     返回包头的总长度位置
        '''
        #print '__decode_head'
        offset_ = offset + 4 # 偏移 AVP_CODE 的位置

        # 解析AVP_LENGTH AND AVP_FLAG
        self.decode_avp_flag_and_length(offset_)
        offset_ += 4 # 偏移 avp_length_flag 的位置
        
        # 解析校验设置AVP_FLAG
        self.decode_avp_flag()
        
        # 解析AVP_vendor_ID
        if self.iavp_flag_exist_vendorid == 1:
            self.decode_avp_vender_id(offset_)
            offset_ += 4 # 偏移 AVP_VANDOR_ID 的位置
        
        #print 'decode head end'
        return offset_
    
    def decode_avp_flag_and_length(self, offset):
        '解析avp leng and flag'
        print 'len(self.avp_decodebuf) %d, offset %d buf:%s'%(len(self.avp_decodebuf) , offset, repr(self.avp_decodebuf[:20]))

        (__flags_and_length,)  = struct.unpack_from("!I", self.avp_decodebuf, offset)
        
        self.avp_flag      = (__flags_and_length >> 24)
        self.avp_length    = (__flags_and_length & 0x00FFFFFF)
        
    def decode_avp_flag(self):
        '从AVP_FLAG中解析AVP_FLAG的各个属性'
        # 解析 VENDOR_ID
        if (self.avp_flag & 0x80) > 0:       # 说明存在VONDER_ID
            if self.avp_length < 12:
                raise "The AVP Length less for min Len: 12!"
            
            self.iavp_flag_exist_vendorid = 1
        else:
            if self.avp_length < 8:
                raise "The AVP Length less for min Len: 8!"
            
        # 解析 MANDATORY
        if (self.avp_flag & 0x40) > 0:
            self.iavp_flag_mandatory = 1
        
        # 解析 PRIVATE
        if (self.avp_flag & 0x20) > 0:
            self.iavp_flag_private = 1
        
    def decode_avp_vender_id(self, offset):
        '解析AVP_VENDOR_ID'
        (self.iavp_vendorid,) = struct.unpack_from("!I", self.avp_decodebuf, offset)
    
    def decode_data(self, offset):
        '''解码AVP包体数据
                     返回本次解码AVP包的总长度
        '''
        #print 'in avp decode_data:', self.avp_format, repr(self.avp_decodebuf),  offset
        
        (self.avp_value,) = struct.unpack_from(self.avp_format, self.avp_decodebuf, offset)

        
        # 解码数据类型后进行一些后续处理
        self.after_decode_data()
        #print '__decode_data end'
        
        return self.avp_length
    
    def after_decode_data(self):
        '解码后进行后续处理'
        #print 'after_decode_data'
        pass
    

