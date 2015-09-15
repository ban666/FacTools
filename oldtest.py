#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os,time
from multiprocessing import Queue
from old_settings import OldSettings
from oldtestui import Ui_Form as Old_ui
from Oldtest_Function import OldTestFunction
from Ana_function import ConfigAnalysis
from Zip_function import zip_folder
import serial
import threading
import shutil

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

q = Queue()
class OldTest(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(OldTest, self).__init__(parent)
        self.oldui = Old_ui()
        self.oldui.setupUi(self)
        self.lcd1 = self.oldui.currentTimes
        self.lcd2 = self.oldui.remainTime
        self.tableWidget = self.oldui.tableWidget
        self.old_settings = OldSettings()
        self.oldui.oldSettings.clicked.connect(self.settings_show)
        self.oldui.startTest.clicked.connect(self.start_test)
        self.oldui.endTest.clicked.connect(self.terminal_test)
        self.oldui.anaData.clicked.connect(self.save_anadata)
        self.old_settings.old_signal.connect(self.change_settings)
        self.timeout = 300
        self.com = 'com1'
        self.channelID = '17'
        self.env_init()

    def env_init(self):
        self.control_times = ''
        self.end_time = ''
        self.device_list = ''
        self.t = ''
        fol = os.getcwd()+'/Log/'
        if not os.path.exists(fol):
            os.mkdir(fol)
        self.reporttime = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        self.report_folder = os.getcwd()+'\\Report\\'
        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
        self.report_folder = self.report_folder+self.reporttime
        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
        self.zigbeefile = fol+'Zigbeelog'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.txt'

    def ana_zigbeefile(self,time_range = 1500):
        try:
            ofolder= self.report_folder+'\\oldtest\\'
            readfile= self.zigbeefile
            print 'ana_file:',readfile
            zipname = ofolder+'oldtest_'+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+'.zip'
            cfg=ConfigAnalysis(readfile,ofolder)
            get_content = cfg.GetDate(2)
            result = cfg.GetAllErrByType(time_range=time_range)
            cfg.WriteToExcel(result)
            zip_folder(ofolder,zipname)
            return zipname
        except Exception as e:
            print 'ana_zigbeefile:',e
            return False

    def save_anadata(self):
        tstr = u'是否分析本次老化测试结果'
        close = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        zipfile = self.ana_zigbeefile()
        if close == QtGui.QMessageBox.Yes:
            if zipfile == None:
                tstr = u'无法分析结果，请检查是否成功开始测试！'
                self.err_handle(tstr)
            elif zipfile == False:
                tstr = u'后台数据为空，请等待测试完成后进行分析！'
                self.err_handle(tstr)
                return
            else:
                s =QtGui.QFileDialog.getExistingDirectory()
                save_folder = unicode(QtCore.QString(s))+'\\oldtest'+self.reporttime
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                shutil.copy(zipfile,save_folder)

    def change_settings(self,content):
        self.control_times = content['control_times']
        self.end_time = content['end_time']
        self.device_list = content['device_list']
        print 'aaa',self.control_times,self.end_time,list(self.device_list)

    def settings_show(self):
        self.old_settings.show()

    def start_test(self):
        #open com
        print self.com,self.channelID,self.timeout
        self.oldui.startTest.setEnabled(False)
        try:
            check_result = self.check_config()
            if check_result == False:
                return
            self.t = serial.Serial(str(self.com),38400)
            self.oldtest = OldTestFunction(self.t,self.device_list)
            self.oldtest.init_Signal.connect(self.display_init)
            self.oldtest.statusChange_Signal.connect(self.display_change)
            self.oldtest.id_gen()
            self.zigbee_thread = oldtestZigbeeThread(self.t,self.channelID,self.device_list,self.end_time,self.zigbeefile)
            self.oldtest.ot_okSignal.connect(self.start_control)
            self.oldtest.ot_terminalSignal.connect(self.terminal_test)
            self.oldtest.ot_controltimesSignal.connect(self.lcd1_change)
            self.oldtest.ot_endtimeSignal.connect(self.lcd2_change)
            self.oldtest.ot_errSignal.connect(self.err_handle)
            self.oldtest.control_times = self.control_times
            self.oldtest.end_time = self.end_time
            self.oldtest.timeout = self.timeout
            self.wait_for_access()
            self.zigbee_thread.start()
            self.back_thread_start()
            print 'zfile:',self.zigbeefile
        except Exception as e:
            self.err_handle(u'测试出现异常，请检查相关配置')
            self.terminal_test()
            print e
        #start control

    def back_thread_start(self):
        global q
        self.judge_loseconnect = threading.Thread(target=self.oldtest.judge_loseconnect, args=())
        self.judge_loseconnect.start()
        self.ana_data = threading.Thread(target=self.oldtest.ana_data, args=(q,))
        self.ana_data.start()

    def display_init(self,statusdict):
        for i,j in statusdict.items():
            for k in range(len(j)-1):
                item = self.tableWidget.item(int(j[0]), int(k))
                item.setText(_translate("Form", str(j[k+1]), None))

    def display_change(self,statuslist):
        for i in range(len(statuslist)-1):
            item = self.tableWidget.item(int(statuslist[0]), i)
            item.setText(_translate("Form", str(statuslist[i+1]), None))

    def check_config(self):
        if self.device_list == '' or (self.control_times == '' and self.end_time == ''):
            self.err_handle(u'配置信息不正确，请正确填写配置信息后重新点击开始测试！')
            return False
        return True

    def err_handle(self,tstr):
        warning = QtGui.QMessageBox.warning(self,'Warning',tstr,QtGui.QMessageBox.Yes)
        self.terminal_test()

    def lcd1_change(self,tstr):
        self.lcd1.display(tstr)

    def lcd2_change(self,tstr):
        self.lcd2.display(tstr)

    def start_control(self,signal):
        if signal == 'ok':
            tstr = u'通断设备已全部入网，是否开始控制测试'
            confirm = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                self.oldtest.start()
            else:
                #self.terminal_test()
                pass
        elif signal == 'fail':
            tstr = u'通断设备并未全部入网，是否开始控制测试'
            confirm = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                self.oldtest.start()
            else:
                #self.terminal_test()
                pass
        else:
            pass

    def wait_for_access(self):
        global q
        self.wait_thread = threading.Thread(target=self.oldtest.login_test, args=(q,))
        self.wait_thread.start()


    def terminal_test(self):
        try:
            print 'endtest'
            self.oldui.startTest.setEnabled(True)
            self.t.close()
            self.oldtest.stopflag = True
            time.sleep(0.1)
            self.zigbee_thread.stop()
            self.zigbee_thread.join()
        except Exception as e:
            print e

class oldtestZigbeeThread(threading.Thread):

    def __init__(self,t,channel,whitelist,endtime,zigbeefile,thread_num=0, timeout=0.01):
        super(oldtestZigbeeThread, self).__init__()
        self.thread_num = thread_num
        self.channel = channel
        self.whitelist = whitelist
        self.endtime = endtime
        self.zigbeefile = zigbeefile
        self.t = t
        self.stopped = False
        self.timeout = timeout

    def run(self):
        global q
        self.zigbee = OldTestFunction(self.t,self.whitelist)
        self.zigbee.end_time =self.endtime
        self.zigbee.id_gen()
        subthread = threading.Thread(target=self.zigbee.com_read, args=(q,self.channel,self.zigbeefile,))
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
    ps = OldTest()
    ps.show()
    sys.exit(app.exec_())