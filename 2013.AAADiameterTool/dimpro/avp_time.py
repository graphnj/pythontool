#coding:utf-8

from avp_octetstring import OctetString
from time import strftime, strptime, mktime, localtime

class Time(OctetString):
    '''
            时间格式是从OctetString AVP基本格式导出的。该字符串必须包含4个八位组，
            与NTP时间戳格式的前4个字节格式相同。NTP时间戳在NTP协议规范［RFC2030］
            第3章中定义。本格式描述的时间，从通用协调时间（UTC）1900年1月1日0点
            开始。在UTC时间2036年二月7日6点28分16秒，时间值将溢出。SNTP规范中描述
            了将时间扩展到2104年的程序，所有DIAMETER节点都必须支持该程序。
    '''
    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        OctetString.__init__(self, avp_code, avp_cfg,  decode_buf)
        self.COMPACTTIMEFORMAT = '%Y%m%d%H%M%S'
        self.TIMEFORMAT=self.COMPACTTIMEFORMAT
        self.seconds_between_1900_and_1970 = ((70*365)+17)*86400

        
    def set_avp_operator_type(self):
        self.avp_format = '!I'

    def NTPStamp2Time(self, stamp):
        '将NTP时间戳转换为年月日的时间格式'
        #stamp = float(repr(stamp))
        myUTCTime = stamp - self.seconds_between_1900_and_1970
        return strftime(self.TIMEFORMAT, localtime(myUTCTime))
        
    def after_decode_data(self):
        self.avp_value = self.NTPStamp2Time(self.avp_value)
        

