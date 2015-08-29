#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os
from settingsui import Ui_Form as settingsui


class Settings(QtGui.QMainWindow):
    comsettings = QtCore.pyqtSignal(dict)
    def __init__(self, parent = None):
        super(Settings, self).__init__(parent)
        self.settingsui = settingsui()
        self.settingsui.setupUi(self)
        self.settingsui.saveSettings.clicked.connect(self.saveSettings)
        self.com=self.settingsui.Com.currentText()
        self.channelID=self.settingsui.ChannelID.currentText()
        self.timout = 30

    def saveSettings(self):
        self.com = self.settingsui.Com.currentText()
        self.channelID = self.settingsui.ChannelID.currentText()
        self.timout = self.settingsui.Timeout.currentText()
        send_dict = {'com':self.com,'channelID':self.channelID,'timeout':self.timout}
        self.comsettings.emit(send_dict)

    def closeEvent(self, event):
        self.saveSettings()
        tstr = u'Com:'+self.com+'\nChannelID:'+self.channelID+u'\n是否配置成功？'
        close = QtGui.QMessageBox.question(self,'Message',tstr,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if close == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = Settings()
    ps.show()
    sys.exit(app.exec_())