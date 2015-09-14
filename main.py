#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from PyQt4 import QtCore, QtGui
import sys,os
from mainui import Ui_Form as mainui
from basictest import AutoTools as BasicTest
from settings import Settings
from DisTest import DisTest
from oldtest import OldTest

class MainWindow(QtGui.QMainWindow, mainui):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.mainui = mainui()
        self.mainui.setupUi(self)
        self.settings = Settings()
        self.com = 'COM1'
        self.channelID = '15'
        self.timeout = 30
        self.settings.comsettings.connect(self.change_settings)
        self.mainui.BasicTest.clicked.connect(self.basic_show)
        self.mainui.Settings.clicked.connect(self.settings_show)
        self.mainui.OldTest.clicked.connect(self.oldtest_show)
        self.mainui.DisconnectTest.clicked.connect(self.disconnect_show)

    def change_settings(self,setting):
        self.com = setting['com']
        self.channelID = setting['channelID']
        self.timeout = setting['timeout']
        print self.com,self.channelID,self.timeout


    def basic_show(self):
        self.basictest = BasicTest()
        self.basictest.com = self.com
        self.basictest.channelID = self.channelID
        self.basictest.timeout = self.timeout
        self.basictest.show()

    def settings_show(self):
        self.settings.show()

    def oldtest_show(self):
        self.oldtest = OldTest()
        self.oldtest.com = self.com
        self.oldtest.channelID = self.channelID
        self.oldtest.timeout = self.timeout
        self.oldtest.show()

    def disconnect_show(self):
        self.Distest = DisTest()
        self.Distest.com = self.com
        self.Distest.channelID = self.channelID
        self.Distest.timeout = self.timeout
        self.Distest.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = MainWindow()
    ps.show()
    sys.exit(app.exec_())
