# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'old_settingsui.ui'
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
        Form.resize(814, 587)
        self.saveSettings = QtGui.QPushButton(Form)
        self.saveSettings.setGeometry(QtCore.QRect(650, 540, 75, 23))
        self.saveSettings.setObjectName(_fromUtf8("saveSettings"))
        self.endTime = QtGui.QLineEdit(Form)
        self.endTime.setGeometry(QtCore.QRect(170, 90, 151, 20))
        self.endTime.setObjectName(_fromUtf8("endTime"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 50, 51, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 51, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(90, 130, 71, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.disTimes = QtGui.QLineEdit(Form)
        self.disTimes.setGeometry(QtCore.QRect(170, 50, 151, 20))
        self.disTimes.setObjectName(_fromUtf8("disTimes"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 90, 181, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(340, 130, 181, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(340, 240, 331, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_12 = QtGui.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(340, 50, 211, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(340, 160, 181, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(340, 220, 181, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(340, 180, 181, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(340, 200, 181, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.deviceList = QtGui.QTextEdit(Form)
        self.deviceList.setGeometry(QtCore.QRect(170, 130, 151, 361))
        self.deviceList.setObjectName(_fromUtf8("deviceList"))
        self.label_13 = QtGui.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(340, 290, 181, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(340, 270, 181, 20))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(340, 330, 181, 20))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_17 = QtGui.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(340, 310, 181, 20))
        self.label_17.setObjectName(_fromUtf8("label_17"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.saveSettings.setText(_translate("Form", "设置", None))
        self.label.setText(_translate("Form", "控制次数", None))
        self.label_2.setText(_translate("Form", "结束时间", None))
        self.label_3.setText(_translate("Form", "待老化设备", None))
        self.label_5.setText(_translate("Form", "eg:2015-08-19 20:17:35", None))
        self.label_6.setText(_translate("Form", "请输入待老化设备18位二维码,如:", None))
        self.label_7.setText(_translate("Form", "对于需要进行控制测试的设备,请在18位二维码后添加2,如:", None))
        self.label_12.setText(_translate("Form", "控制次数与结束时间至少填写一项", None))
        self.label_8.setText(_translate("Form", "00124b000a01354516", None))
        self.label_11.setText(_translate("Form", ".......", None))
        self.label_9.setText(_translate("Form", "00124b000a01354614", None))
        self.label_10.setText(_translate("Form", "00124b000a01354715", None))
        self.deviceList.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_13.setText(_translate("Form", "00124b000a013546142", None))
        self.label_14.setText(_translate("Form", "00124b000a013545162", None))
        self.label_15.setText(_translate("Form", ".......", None))
        self.label_17.setText(_translate("Form", "00124b000a013547152", None))

