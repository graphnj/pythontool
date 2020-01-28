#coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import urllib,re,sys
doc_version=['11.9.0','11.8.0','11.7.0','11.6.0','11.5.0','11.4.0','11.3.0','11.2.0','11.1.0']
baseurl='http://www.3gpp.org/ftp/Specs/html-info/%s.htm'

 
class StandardDialog(QDialog):

    def __init__(self,parent=None):
        super(StandardDialog,self).__init__(parent)
        
        self.setWindowTitle("3GPP doc Downloader!")
        DimMsgDecodeButton=QPushButton(self.tr("Dim Msg Decode"))

        self.label_SrcBuf = QLabel('3GPP DocID: 29273 29280 ...')
        
        self.fileTextEditInput=QTextEdit()
        self.fileTextEditOutput=QTextEdit()
        self.fileTextEditOutput.setReadOnly(1)
        

        layout=QGridLayout()
        #col 0
        layout.addWidget(self.label_SrcBuf, 0, 0)
        layout.addWidget(self.fileTextEditInput, 1, 0, 3, 1)
        layout.addWidget(self.fileTextEditOutput,4,0, 12, 1)
        #col 1
        layout.addWidget(DimMsgDecodeButton,2,1)

        self.setLayout(layout)
        self.connect(DimMsgDecodeButton,SIGNAL("clicked()"),self.DecodeDimMsgSlot)

    def getdoc(self,doc_no):
        url=baseurl%(doc_no)
        log='preparing download from'+url
        self.fileTextEditOutput.append(log)
        
        try:
            webpage=urllib.urlopen(url).read()
            for ver in doc_version:
                doc_urls=re.findall('<a href=(.*?)>'+ver, webpage)
                if doc_urls:
                    doc_url=doc_urls[0]
                    break
                    
            filename1=re.search('\d{5}-b\d{2}.zip',doc_url)
            if filename1:
                filename=filename1.group()
            else:
                filename=doc_no

            s=urllib.urlopen(doc_url)
            destfile=s.read()
            open(filename,'wb').write(destfile)
            log='download %s from %s success!!'%(filename, doc_url)
            self.fileTextEditOutput.append(log)
        except:
            log='open url ['+url+'] failure!'
            self.fileTextEditOutput.append(log)

    def DecodeDimMsgSlot(self):
        hexstr=str(self.fileTextEditInput.toPlainText()).strip()

        downloadlist=re.split('[ ,]',hexstr)
        print downloadlist
        for docid in downloadlist:
            self.getdoc(docid)

if __name__ == '__main__':
    print 'starting!!!'
    app=QApplication(sys.argv)
    form=StandardDialog()
    form.show()
    app.exec_()