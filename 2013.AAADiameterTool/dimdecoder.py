#coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import json
from binascii import a2b_hex, b2a_hex
#import gc
from dimpro import  glo
from dimpro import CDimDecodeHandler,  DIM_CFG
import struct
param = {}
json_str = None
hex_str = None
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))





class StandardDialog(QDialog):

    def __init__(self,parent=None):
        super(StandardDialog,self).__init__(parent)
        
        self.dim_JSON={}
        self.dim_JSON['Header']=None
        self.dim_JSON['AVP']    =None
        
        self.setWindowTitle("ZTE HLR AAA Diameter Decoder!")
        self.resize(800, 600)
        DimMsgDecodeButton=QPushButton(self.tr("Dim Msg Decode"))
        ButtonRefreshCfg=QPushButton(self.tr("Refresh config"))

        self.label_SrcBuf = QLabel('Diameter Hex Data')
        self.label_TreeView = QLabel('Diameter Tree View')
        
        self.fileTextEditInput=QTextEdit()
        self.fileTextEditOutput=QTextEdit()
        self.fileTextEditOutput.setReadOnly(1)

        self.tTreeWidget=QTreeWidget()
        self.tTreeWidget.setColumnCount(2)
        self.tTreeWidget.setHeaderLabels(['AVPID','Value'])
        
        
        layout=QGridLayout()
        #col 0
        layout.addWidget(self.label_SrcBuf, 0, 0)
        layout.addWidget(self.fileTextEditInput, 1, 0, 3, 1)
        layout.addWidget(self.fileTextEditOutput,4,0, 12, 1)
        #col 1
        layout.addWidget(DimMsgDecodeButton,2,1)
        layout.addWidget(ButtonRefreshCfg,15,1)
        
        #clo 2
        layout.addWidget(self.label_TreeView, 0, 2)
        layout.addWidget(self.tTreeWidget,1,2, 15, 1)
        
        self.setLayout(layout)
        
        self.connect(DimMsgDecodeButton,SIGNAL("clicked()"),self.DecodeDimMsgSlot)
        self.connect(ButtonRefreshCfg,SIGNAL("clicked()"),self.RefreshConfigSlot)

    def add_tree_nodes(self, parent_item=None, items=None):
        for item in items:
            if isinstance(item, dict):
                #print 'dict ', item
                self.add_tree_nodes(parent_item,item)
            else:
                if isinstance(items, dict) and not isinstance(items[item], (dict, list)):
                    #print 'item=', item
                    child1 = QTreeWidgetItem(parent_item)
                    child1.setText(0,item)
                    if len(str(items[item]))==0:
                        child1.setText(1,"[N/A]")
                        child1.setTextColor(1, QColor(200, 0, 0))
                    else:
                        child1.setText(1,str(items[item]))
                elif isinstance(items,list):
                    print 'list: 尚未实现'
                    continue
                else:
                    #print 'Group:', item
                    new_parent = QTreeWidgetItem(parent_item)
                    new_parent.setText(0,item)
                    new_parent.setText(1,"[Grouped! Click expand]")
                    new_parent.setBackgroundColor(1, QColor(60,200,10))
                    self.add_tree_nodes(new_parent,  items[item])
                
        #print 'finished\n\n\n'

    def DisplayTreeView(self,  jsondata):
        root= QTreeWidgetItem(self.tTreeWidget)
        root.setText(0,'Diameter Msg')
        root.setTextColor(0, QColor(100, 100, 255))
        self.tTreeWidget.expandItem(root)
        
        NodeHeader = QTreeWidgetItem(root)
        NodeHeader.setText(0,'Diameter Msg Header')
        self.add_tree_nodes(NodeHeader, json.loads(jsondata['Header']))
        NodeHeader.setTextColor(0, QColor(50, 0, 255))
                        
        NodeAVP = QTreeWidgetItem(root)
        NodeAVP.setText(0,'Diameter Msg AVP')
        NodeAVP.setTextColor(0, QColor(100, 0, 255))
        
        self.add_tree_nodes(NodeAVP, json.loads(jsondata['AVP']))
        self.tTreeWidget.addTopLevelItem(NodeAVP)
        self.tTreeWidget.expandItem(NodeAVP)
        #self.tTreeWidget.openPersistentEditor(root, 1)#QTreeWidget.openPersistentEditor (self, QTreeWidgetItem item, int column = 0)  这个只能编辑指定项
        
        
    def CheckValid(self,  pack_buf):
        offset_ = 0
        buflen=len(pack_buf)
        #print buflen
        if buflen<4:
            self.error='buf is too small'
            return 0
        
        (ver_and_len,) = struct.unpack_from("!I", pack_buf, offset_)
        offset_ += 4
        self.dimmsgleninheader  = ver_and_len & 0x00FFFFFF
        
        if buflen != self.dimmsgleninheader:
            self.error='Length in DimeterHeader is %d, but givin %d'%(self.dimmsgleninheader,  buflen)
            return 0
            
        return 1
        
    def unpack_hex(self,  pack_buf):
        '解码HEX数据'

        my_msg = CDimDecodeHandler(glo.g_dimcfg)
        my_msg.unpack_json(pack_buf)
        self.dim_JSON['Header']=my_msg.DimMsgHeader_JSON
        self.dim_JSON['AVP']=my_msg.DimAVP_JSON
        #print 'Dim Header:', self.dim_JSON['Header']
        #print 'AVP:', self.dim_JSON['AVP']
        return self.dim_JSON

    def DecodeDimMsgSlot(self):
        #out_json = unpack_hex(a2b_hex(hex_str))
        hexstr=str(self.fileTextEditInput.toPlainText())
        hexstr1=hexstr.replace(' ', '')
        hexstr1=hexstr1.replace('\n', '')
        bindata=a2b_hex(hexstr1)
        if 0==self.CheckValid(bindata):
            self.fileTextEditOutput.setText(self.error)
        else:
            '''
            gc.enable()
            # Set the garbage collection debugging flags.
            gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)
            '''
            out_json = self.unpack_hex(bindata)
            self.fileTextEditOutput.setText(str(out_json['Header'])+str(out_json['AVP']))
            self.DisplayTreeView(out_json)
            '''
            print 'begin collect...'
            _unreachable = gc.collect()
            print 'unreachable object num:%d' % _unreachable
            print 'garbage object num:%d' % len(gc.garbage)
            '''
            
    def RefreshConfigSlot(self):
        glo.g_dimcfg.refresh()


if __name__ == '__main__':
    print 'starting!!!'
    app=QApplication(sys.argv)
    form=StandardDialog()
    form.show()
    app.exec_()
