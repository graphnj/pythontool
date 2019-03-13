#!/usr/bin/evn python
#-*- coding:utf-8 -*-

from avp_octetstring import OctetString

class DiameterIdentity(OctetString):

    def __init__(self, avp_code     = (0, 0),  avp_cfg = None,  decode_buf   = None):
        OctetString.__init__(self, avp_code, avp_cfg,  decode_buf)
        
