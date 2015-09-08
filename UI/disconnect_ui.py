# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'disconnectui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(629, 411)
        self.startTest = QtGui.QPushButton(Form)
        self.startTest.setGeometry(QtCore.QRect(400, 340, 75, 23))
        self.startTest.setObjectName(_fromUtf8("startTest"))
        self.endTest = QtGui.QPushButton(Form)
        self.endTest.setGeometry(QtCore.QRect(510, 340, 75, 23))
        self.endTest.setObjectName(_fromUtf8("endTest"))
        self.currentTimes = QtGui.QLCDNumber(Form)
        self.currentTimes.setGeometry(QtCore.QRect(140, 50, 151, 51))
        self.currentTimes.setObjectName(_fromUtf8("currentTimes"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.disSettings = QtGui.QPushButton(Form)
        self.disSettings.setGeometry(QtCore.QRect(290, 340, 75, 23))
        self.disSettings.setObjectName(_fromUtf8("disSettings"))
        self.remainTime = QtGui.QLCDNumber(Form)
        self.remainTime.setGeometry(QtCore.QRect(140, 150, 341, 51))
        self.remainTime.setSmallDecimalPoint(True)
        self.remainTime.setNumDigits(12)
        self.remainTime.setDigitCount(12)
        self.remainTime.setMode(QtGui.QLCDNumber.Bin)
        self.remainTime.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.remainTime.setProperty("value", 1000000000.0)
        self.remainTime.setProperty("intValue", 1000000000)
        self.remainTime.setObjectName(_fromUtf8("remainTime"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 160, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.startTest.setText(_translate("Form", "开始控制", None))
        self.endTest.setText(_translate("Form", "结束控制", None))
        self.label.setText(_translate("Form", "当前控制次数：", None))
        self.disSettings.setText(_translate("Form", "通断设置", None))
        self.label_2.setText(_translate("Form", "剩余时间：", None))

