# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
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
        Form.resize(605, 338)
        self.saveSettings = QtGui.QPushButton(Form)
        self.saveSettings.setGeometry(QtCore.QRect(450, 260, 75, 23))
        self.saveSettings.setObjectName(_fromUtf8("pushButton"))
        self.ChannelID = QtGui.QComboBox(Form)
        self.ChannelID.setGeometry(QtCore.QRect(170, 90, 151, 20))
        self.ChannelID.setObjectName(_fromUtf8("ChannelID"))
        for i in range(11,27):
            self.ChannelID.addItem(_fromUtf8(""))
        self.Com = QtGui.QComboBox(Form)
        self.Com.setGeometry(QtCore.QRect(170, 50, 151, 22))
        self.Com.setObjectName(_fromUtf8("Com"))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.Com.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 50  , 51, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 71, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 90, 61, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(90, 130, 71, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(340, 130, 81, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.Timeout = QtGui.QComboBox(Form)
        self.Timeout.setGeometry(QtCore.QRect(170, 130, 151, 22))
        self.Timeout.setObjectName(_fromUtf8("Timeout"))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.Timeout.addItem(_fromUtf8(""))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.saveSettings.setText(_translate("Form", "设置", None))
        self.Com.setItemText(0, _translate("Form", "Com1", None))
        self.Com.setItemText(1, _translate("Form", "Com2", None))
        self.Com.setItemText(2, _translate("Form", "Com3", None))
        self.Com.setItemText(3, _translate("Form", "Com4", None))
        self.Com.setItemText(4, _translate("Form", "Com5", None))
        self.Com.setItemText(5, _translate("Form", "Com6", None))
        self.Com.setItemText(6, _translate("Form", "Com7", None))
        self.Com.setItemText(7, _translate("Form", "Com8", None))
        self.Com.setItemText(8, _translate("Form", "Com9", None))
        self.Com.setItemText(9, _translate("Form", "Com10", None))
        for i in range(11,27):
            channel_id = '{:02x}'.format(i)
            self.ChannelID.setItemText(i-11, _translate("Form",channel_id, None))
        self.label.setText(_translate("Form", "串口：", None))
        self.label_2.setText(_translate("Form", "ChannelID：", None))
        self.label_5.setText(_translate("Form", "0b---1a", None))
        self.label_3.setText(_translate("Form", "Timeout：", None))
        self.label_6.setText(_translate("Form", "30--300(秒)", None))
        self.Timeout.setItemText(0, _translate("Form", "30", None))
        self.Timeout.setItemText(1, _translate("Form", "60", None))
        self.Timeout.setItemText(2, _translate("Form", "90", None))
        self.Timeout.setItemText(3, _translate("Form", "120", None))
        self.Timeout.setItemText(4, _translate("Form", "150", None))
        self.Timeout.setItemText(5, _translate("Form", "180", None))
        self.Timeout.setItemText(6, _translate("Form", "210", None))
        self.Timeout.setItemText(7, _translate("Form", "240", None))
        self.Timeout.setItemText(8, _translate("Form", "270", None))
        self.Timeout.setItemText(9, _translate("Form", "300", None))
