# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys,os
import random,time,threading
from uitest import Ui_MainWindow as ui
from functionui import Ui_Form as ui
import serial
import cmdgen
from multiprocessing import Process,Queue
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Basictest_function import *
import xlsxwriter,xlrd,xlwt
from xlutils.copy import copy

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
stopflag = False
q=Queue()
p=Queue()
class AutoTools(QtGui.QMainWindow, ui):
    def __init__(self, parent = None):
        super(AutoTools, self).__init__(parent)
        self.com='com1'
        self.channelID = '15'
        self.timeout = 30
        self.sinOut = pyqtSignal(str)
        self.ui = ui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.p1)
        self.terminate = False
        self.result = ''
        self.content = ''
        self.env_init()
        self.devicedict={
            '01':'智能路由节点',
            '04':'智能调光器',
            '03':'智能门磁感应器',
            '06':'智能全向红外网关',
            '0d':'智能烟雾感应器',
            '0f':'一氧化碳感应器',
            '0c':'人体红外感应器',
            '0e':'可燃气体感应器',
            '14':'智能单开',
            '15':'智能双开',
            '16':'智能三开',
            '11':'智能报警器',
            '13':'红外水晶开关',
            '17':'智能窗帘',
            '18':'智能窗户'
            }

    def change_settings(self,setting):
        self.com = setting['com']
        self.channelID = setting['channelID']
        print 'autotools:',self.com,self.channelID

    def env_init(self):
        self.report_folder = os.getcwd()+'\\Report\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
        self.report_file = self.report_folder+'/Log.txt'
        self.report_excel = self.report_folder+'/Report.xls'
        self.init_excel()

        self.t = ''


    def slotName(self):
        self.ui.pushButton.setEnabled(False)
        content,ok=QtGui.QInputDialog.getText(self,self.tr('二维码扫描'),
                                     self.tr('请扫描二维码:'),
                                     QtGui.QLineEdit.Normal,'')
        if ok:
            if len(content)!=18 or not self.devicedict.has_key(str(content[-2:])):
                self.printForUi(u'条形码错误，请检查！')
                #self.nameLabel.setText("")

                self.slotName()

            else:
                global q,p
                tstr = "设备mac: "+str(content[:16]) +" "+ "设备类型: "+ self.devicedict[str(content[-2:])]
                self.printForUi(tstr.decode('utf-8'))
                self.content = content
                self.thread_test.content =content
                self.thread = threading.Thread(target=self.thread_test.device_test,args=(q,p,))
                self.thread.start()
        else:
            try:
                self.t.close()
                time.sleep(0.1)
                self.zigbee_thread.stop()
                self.zigbee_thread.join()
                self.ui.pushButton.setEnabled(True)
            except Exception as e:
                print e
            return 'terminate'



    def start_test(self,content):
        pass


    def printForUi(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:

        text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text+'\n'
        self.tc = self.ui.textEdit.textCursor()
        self.tc.movePosition(self.tc.End)
        self.ui.textEdit.setTextCursor(self.tc)
        self.ui.textEdit.insertPlainText(text)
        for c in text:
            if c == '\n':
                self.vsb = self.ui.textEdit.verticalScrollBar()
                self.vsb.setSliderPosition(self.vsb.maximum())
        try:
            with open(self.report_file,'a+') as f:
                f.write(unicode(QtCore.QString(text)).encode('utf-8'))
                f.flush()
        except Exception as e:
            print e

    def init_excel(self):
        self.wb = xlsxwriter.Workbook(self.report_excel)
        self.ws = self.wb.add_worksheet()
        columnlist=[u'设备MAC',u'设备种类',u'入网测试结果',u'状态上传测试结果',u'控制测试结果',u'测试结果',u'开始时间',u'结束时间']

        self.ws.set_column(0,7,22)

        #column
        for i in range(8):
            self.ws.write(0,i,columnlist[i])
        self.row = 0
        self.wb.close()



    def writeExcel(self,resultdict):
        print 'write to excel'
        resultlist = [str(self.content[:16]),self.devicedict[str(self.content[-2:])],resultdict['login'],resultdict['status'],resultdict['control'],
                      resultdict['result'],resultdict['starttime'],resultdict['endtime']]
        oldWb = xlrd.open_workbook(self.report_excel)
        newWb = copy(oldWb)
        newWs = newWb.get_sheet(0)
        self.row+=1
        for i in range(8):
            #print data[i][j]
            newWs.col(i).width = 0x1a00

            newWs.write(self.row,i,str(resultlist[i]).decode('utf-8'))
        newWb.save(self.report_excel)

    def p1(self):
        '''
        self.zigbee_thread = TestThread(self.t)
        self.zigbee_thread.start()
        '''
        print 'auto：',self.com,self.channelID,self.timeout
        try:
            self.t = serial.Serial(str(self.com),38400)
            self.thread_test = Dt(self.t)
            self.thread_test.timeout =self.timeout
            self.thread_test.textOut.connect(self.printForUi)
            self.thread_test.writeExcel.connect(self.writeExcel)
            self.thread_test.terminalOut.connect(self.slotName)
            self.zigbee_thread = TestThread(self.t,self.channelID)
            self.zigbee_thread.start()
            self.slotName()
        except Exception as e:
            print e
            self.printForUi(u'串口打开失败，请检查设置并在设置成功后重新运行程序')


    def closeEvent(self, event):
        try:
            self.t.close()
            time.sleep(0.1)
            self.zigbee_thread.stop()
            self.zigbee_thread.join()
        except Exception as e:
            print e
        finally:
            event.accept()

class TestThread(threading.Thread):

    def __init__(self,t,channel,thread_num=0, timeout=0.01):
        super(TestThread, self).__init__()
        self.thread_num = thread_num
        self.channel = channel
        self.t = t
        self.stopped = False
        self.timeout = timeout

    def run(self):
        global q,p
        subthread = threading.Thread(target=Dt(self.t).com_read, args=(q,p,self.channel,))
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            subthread.join(self.timeout)

        print('Thread stopped')

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = AutoTools()
    ps.show()
    sys.exit(app.exec_())




