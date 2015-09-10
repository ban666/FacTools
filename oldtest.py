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
import serial
import threading

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
        self.old_settings.old_signal.connect(self.change_settings)
        self.timeout = 10
        self.com = 'com1'
        self.channelID = '17'
        self.env_init()

    def env_init(self):
        self.control_times = ''
        self.end_time = ''
        self.device_list = ''
        self.t = ''

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
            print 1111
            self.oldtest = OldTestFunction(self.t,self.device_list)
            print 2222
            self.oldtest.init_Signal.connect(self.display_init)
            print 3333
            self.oldtest.id_gen()
            print 4444
            '''
            self.zigbee_thread = oldtestZigbeeThread(self.t,self.channelID,self.device_list)
            self.oldtest.okSignal.connect(self.start_control)
            self.oldtest.terminalSignal.connect(self.terminal_test)
            self.oldtest.controltimesSignal.connect(self.lcd1_change)
            self.oldtest.endtimeSignal.connect(self.lcd2_change)
            self.oldtest.errSignal.connect(self.err_handle)

            self.oldtest.control_times = self.control_times
            self.oldtest.end_time = self.end_time
            self.oldtest.timeout = self.timeout
            self.wait_for_access()
            self.zigbee_thread.start()
            '''
        except Exception as e:
            self.err_handle(u'测试出现异常，请检查相关配置')
            '''
            self.terminal_test()
            '''
            print e
        #start control

    def display_init(self,statusdict):
        print 5555
        for i,j in statusdict.items():
            print i,j
            for k in range(len(j)):
                print j[k]
                item = self.tableWidget.item(int(i), int(k))
                item.setText(_translate("Form", str(j[k]), None))

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
        pass

    def lcd2_change(self,tstr):
        self.lcd2.display(tstr)

    def start_control(self,signal):
        if signal == 'ok':
            tstr = u'通断设备已全部入网，是否开始通断测试'
            confirm = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                self.oldtest.start()
            else:
                self.terminal_test()
        elif signal == 'fail':
            tstr = u'通断设备并未全部入网，是否开始通断测试'
            confirm = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                self.oldtest.start()
            else:
                self.terminal_test()
        else:
            self.terminal_test()

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

    def __init__(self,t,channel,whitelist,thread_num=0, timeout=0.01):
        super(oldtestZigbeeThread, self).__init__()
        self.thread_num = thread_num
        self.channel = channel
        self.whitelist = whitelist
        self.t = t
        self.stopped = False
        self.timeout = timeout

    def run(self):
        global q
        subthread = threading.Thread(target=oldtestFunction(self.t,self.whitelist).com_read, args=(q,self.channel,))
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