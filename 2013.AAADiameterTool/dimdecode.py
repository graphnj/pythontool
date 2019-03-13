 # coding:utf-8
 
import sys
from getopt import getopt
from sys import argv
from random import randint
from binascii import a2b_hex, b2a_hex

from dimpro import  glo
from dimpro import CDimDecodeHandler, DIM_CFG

param = {}
json_str = None
hex_str = None


def unpack_hex(pack_buf):
    '解码HEX数据'

    my_msg = CDimDecodeHandler(glo.g_dimcfg)
    
    my_msg.unpack_json(pack_buf)
    print 'unpack_hex'
    return my_msg.dmsg['DCC_JSON']

'''
if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'should "%s filenamewantedecoded" '%(sys.argv[0])
        exit(0)
    
    
    # 打开需要读取的文件
    encode_file = open(sys.argv[1], 'r')
    hex_str = encode_file.readline()
    encode_file.close()
    #print 'hex_str',hex_str
    
    out_json = unpack_hex(a2b_hex(hex_str))
    print 'main'
    print out_json
'''
