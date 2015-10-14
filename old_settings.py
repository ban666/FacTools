#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os,time
from oldsettingsui import Ui_Form as old_settings_ui


class OldSettings(QtGui.QMainWindow):
    old_signal = QtCore.pyqtSignal(dict)
    def __init__(self, parent = None):
        super(OldSettings, self).__init__(parent)
        self.oldsettingsui = old_settings_ui()
        self.oldsettingsui.setupUi(self)
        self.oldsettingsui.saveSettings.clicked.connect(self.save_settings)
        #self.table = self.oldsettingsui.tableWidget
        self.typelist=['01','03','04','0c','0d','0e','06','11','14','15','16','17','18','20']

    def check_devicelist(self,content):
        content = content.split('\n')
        if str(content[-1]).strip()=='':
            content = content[:-1]
        for j in range(len(content)):
            i=str(content[j]).strip()
            if len(i)!=18 and len(i)!=19:
                tstr=u'第'+str(j+1)+u'行 数据长度错误！'
                self.alert_warning(tstr)
                return False
            if not str(i)[16:18] in self.typelist:
                tstr=u'第'+str(j+1)+u'行 设备类型错误！'
                self.alert_warning(tstr)
                return False
            if len(i)==19 and i[-1:]!='2':
                tstr=u'第'+str(j+1)+u'行 需控制测试的设备最后一位需为2！'
                self.alert_warning(tstr)
                return False
        if len(content) != len(set(content)):
            tstr=u'设备列表中有重复元素，请检查后重新填写'
            self.alert_warning(tstr)
            return False
        if len(content) > 200:
            tstr=u'通断设备最大为200个，配置名单超过范围'
            self.alert_warning(tstr)
            return False
        return content

    def check_mac(self,mac):
        if len(mac)!=18 or not mac[-2:] in self.typelist:
            return False
        else:
            return True

    def alert_warning(self,tstr):
        warning = QtGui.QMessageBox.warning(self,'Warning',tstr,QtGui.QMessageBox.Yes)

    def save_settings(self):
        result = self.check_data()
        print self.control_times,self.end_time,self.devicelist
        if result != False:
            send_dict = {'control_times':self.control_times,'end_time':self.end_time,'device_list':self.devicelist}

            self.old_signal.emit(send_dict)
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

    def check_data(self):
        self.control_times = self.check_controltimes(self.oldsettingsui.disTimes.text())
        self.end_time = self.check_endtime(self.oldsettingsui.endTime.text())
        self.devicelist = self.check_devicelist(self.oldsettingsui.deviceList.toPlainText())
        tlist = [self.control_times,self.end_time,self.devicelist]
        for i in tlist:
            if i == False:
                tstr=u'配置错误，请检查后重新填写'
                self.alert_warning(tstr)
                return False
        if self.end_time == 'null':
            tstr = u'结束时间为必填项！'
            self.alert_warning(tstr)
            return False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = OldSettings()
    ps.show()
    sys.exit(app.exec_())