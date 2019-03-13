#-*- coding:utf-8 -*-


__version__ = "0.1"

from dim_config import DIM_CFG
from glo import g_dimcfg
from avp_factory import create_avp
from dimdecodehandler import CDimDecodeHandler
from avp import AVP

def version():
    '打印模块版本'
    print "version = __version__"
    
