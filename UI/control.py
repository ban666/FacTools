# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control.ui'
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
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(400, 340, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 340, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.lcdNumber = QtGui.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(140, 50, 151, 51))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(360, 60, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(360, 170, 71, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(140, 170, 151, 41))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(450, 50, 141, 51))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(450, 170, 141, 41))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "开始控制", None))
        self.pushButton_2.setText(_translate("Form", "结束控制", None))
        self.label.setText(_translate("Form", "当前控制次数：", None))
        self.label_2.setText(_translate("Form", "计划控制次数：", None))
        self.label_3.setText(_translate("Form", "运行时间：", None))
        self.label_4.setText(_translate("Form", "开始时间：", None))

