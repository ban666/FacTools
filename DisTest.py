#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os,time
from multiprocessing import Queue
from Dis_settings import DisSettings
from disconnec_ui import Ui_Form as Dis_ui
from DisTest_function import DisTestFunction
import serial
import threading

q = Queue()
class DisTest(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(DisTest, self).__init__(parent)
        self.disui = Dis_ui()
        self.disui.setupUi(self)
        self.dis_settings = DisSettings()
        self.disui.disSettings.clicked.connect(self.settings_show)
        self.disui.startTest.clicked.connect(self.start_test)
        self.disui.endTest.clicked.connect(self.terminal_test)
        self.dis_settings.dis_signal.connect(self.change_settings)
        self.timeout = 30
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
        self.dis_settings.show()

    def start_test(self):
        #open com
        self.disui.startTest.setEnabled(False)
        try:
            check_result = self.check_config()
            if check_result == False:
                return
            self.t = serial.Serial(str(self.com),38400)
            self.distest = DisTestFunction(self.t,self.device_list)
            self.zigbee_thread = DisTestZigbeeThread(self.t,self.channelID,self.device_list)
            self.distest.okSignal.connect(self.start_control)
            self.distest.controltimesSignal.connect(self.lcd1_change)
            self.distest.endtimeSignal.connect(self.lcd2_change)
            self.distest.errSignal.connect(self.err_handle)
            self.distest.control_times = self.control_times
            self.distest.end_time = self.end_time
            self.distest.timeout = self.timeout
            self.wait_for_access()
            self.zigbee_thread.start()
        except Exception as e:
            print e
        #start control

    def check_config(self):
        if self.device_list == '' or (self.control_times == '' and self.end_time == ''):
            self.err_handle(u'配置信息不正确，请正确填写配置信息后重新点击开始测试！')
            return False
        return True
    def err_handle(self,tstr):
        warning = QtGui.QMessageBox.warning(self,'Warning',tstr,QtGui.QMessageBox.Yes)
        self.terminal_test()

    def lcd1_change(self,tstr):
        pass

    def lcd2_change(self,tstr):
        pass

    def start_control(self,signal):
        if signal == 'ok':
            tstr = u'通断设备已全部入网，是否开始通断测试'
            confirm = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                self.distest.start()
        elif signal == 'fail':
            tstr = u'通断设备并未全部入网，是否开始通断测试'
            pass


    def wait_for_access(self):
        global q
        self.wait_thread = threading.Thread(target=self.distest.check_online, args=(q,))
        self.wait_thread.start()


    def terminal_test(self):
        try:
            self.disui.startTest.setEnabled(True)
            self.t.close()
            time.sleep(0.1)
            self.zigbee_thread.stop()
            self.zigbee_thread.join()
        except Exception as e:
            print e

class DisTestZigbeeThread(threading.Thread):

    def __init__(self,t,channel,whitelist,thread_num=0, timeout=0.01):
        super(DisTestZigbeeThread, self).__init__()
        self.thread_num = thread_num
        self.channel = channel
        self.whitelist = whitelist
        self.t = t
        self.stopped = False
        self.timeout = timeout

    def run(self):
        global q
        subthread = threading.Thread(target=DisTestFunction(self.t,self.whitelist).com_read, args=(q,self.channel,))
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
    ps = DisTest()
    ps.show()
    sys.exit(app.exec_())