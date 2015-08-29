# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
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
        Form.setObjectName(_fromUtf8("生产测试工具"))
        Form.resize(782, 553)
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 671, 101))
        self.frame.setStyleSheet(_fromUtf8(""))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.OldTest = QtGui.QPushButton(self.frame)
        self.OldTest.setGeometry(QtCore.QRect(110, 10, 91, 80))
        self.OldTest.setMinimumSize(QtCore.QSize(50, 80))
        self.OldTest.setObjectName(_fromUtf8("OldTest"))
        self.DisconnectTest = QtGui.QPushButton(self.frame)
        self.DisconnectTest.setGeometry(QtCore.QRect(210, 10, 101, 80))
        self.DisconnectTest.setMinimumSize(QtCore.QSize(50, 80))
        self.DisconnectTest.setStyleSheet(_fromUtf8(""))
        self.DisconnectTest.setAutoDefault(False)
        self.DisconnectTest.setDefault(False)
        self.DisconnectTest.setFlat(False)
        self.DisconnectTest.setObjectName(_fromUtf8("DisconnectTest"))
        self.Settings = QtGui.QPushButton(self.frame)
        self.Settings.setEnabled(True)
        self.Settings.setGeometry(QtCore.QRect(320, 10, 101, 80))
        self.Settings.setMinimumSize(QtCore.QSize(50, 80))
        self.Settings.setStyleSheet(_fromUtf8(""))
        self.Settings.setObjectName(_fromUtf8("Settings"))
        self.BasicTest = QtGui.QPushButton(self.frame)
        self.BasicTest.setGeometry(QtCore.QRect(10, 10, 91, 80))
        self.BasicTest.setMinimumSize(QtCore.QSize(50, 80))
        self.BasicTest.setObjectName(_fromUtf8("BasicTest"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "生产测试工具", None))
        self.OldTest.setText(_translate("Form", "老化测试", None))
        self.DisconnectTest.setText(_translate("Form", "通断测试", None))
        self.Settings.setText(_translate("Form", "系统设置", None))
        self.BasicTest.setText(_translate("Form", "基本功能测试", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
