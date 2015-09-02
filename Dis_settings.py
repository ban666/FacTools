#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os,time
from disconnec_settingsui import Ui_Form as dis_settings_ui


class DisSettings(QtGui.QMainWindow):
    dis_signal = QtCore.pyqtSignal(dict)
    def __init__(self, parent = None):
        super(DisSettings, self).__init__(parent)
        self.dissettingsui = dis_settings_ui()
        self.dissettingsui.setupUi(self)
        self.dissettingsui.saveSettings.clicked.connect(self.save_settings)
        self.typelist=['14','15','16']

    def save_settings(self):
        result = self.check_data()
        #print self.control_times,self.end_time,self.devicelist
        if result != False:
            send_dict = {'control_times':self.control_times,'end_time':self.end_time,'device_list':self.devicelist}
            self.dis_signal.emit(send_dict)
            self.alert_warning(tstr=u'配置成功，请关闭窗口')

    def check_endtime(self,timestrip):
        if timestrip == '':
            return 'null'
        try:
            now_time = time.strptime(timestrip,"%Y-%m-%d %H:%M:%S")
            now_time = time.mktime(now_time)
            print now_time
            if now_time<time.time():
                return False
            return int(now_time)
        except:
            return False

    def check_controltimes(self,tstr):
        if tstr == '':
            return 'null'
        if str(tstr).isdigit():
            return tstr
        else:
            return False

    def check_devicelist(self,content):
        content = content.split('\n')
        for i in content:
            if len(i)!=18 or not str(i)[-2:] in self.typelist:
                return False
        if len(content) != len(set(content)):
            tstr=u'设备列表中有重复元素，请检查后重新填写'
            self.alert_warning(tstr)
            return False
        if len(content) > 100:
            tstr=u'通断设备最大为100个，配置名单超过范围'
            self.alert_warning(tstr)
            return False
        return content

    def alert_warning(self,tstr):
        warning = QtGui.QMessageBox.warning(self,'Warning',tstr,QtGui.QMessageBox.Yes)

    def check_data(self):
        self.control_times = self.check_controltimes(self.dissettingsui.disTimes.text())
        self.end_time = self.check_endtime(self.dissettingsui.endTime.text())
        self.devicelist = self.check_devicelist(self.dissettingsui.deviceList.toPlainText())
        tlist = [self.control_times,self.end_time,self.devicelist]
        for i in tlist:
            if i == False:
                tstr=u'配置错误，请检查后重新填写'
                self.alert_warning(tstr)
                return False
        if self.control_times == 'null' and self.end_time == 'null':
            tstr = u'通断次数与结束时间至少填写一项！'
            self.alert_warning(tstr)
            return False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = DisSettings()
    ps.show()
    sys.exit(app.exec_())