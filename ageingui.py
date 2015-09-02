# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ageing.ui'
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
        Form.resize(715, 506)
        self.allStatus = QtGui.QTextEdit(Form)
        self.allStatus.setGeometry(QtCore.QRect(20, 50, 341, 431))
        self.allStatus.setObjectName(_fromUtf8("textEdit"))
        self.singleStatus = QtGui.QTextEdit(Form)
        self.singleStatus.setGeometry(QtCore.QRect(380, 50, 301, 131))
        self.singleStatus.setObjectName(_fromUtf8("textEdit_2"))
        self.oldSettings = QtGui.QPushButton(Form)
        self.oldSettings.setGeometry(QtCore.QRect(610, 340, 91, 41))
        self.oldSettings.setObjectName(_fromUtf8("oldSettings"))
        self.startTest = QtGui.QPushButton(Form)
        self.startTest.setGeometry(QtCore.QRect(610, 390, 91, 41))
        self.startTest.setObjectName(_fromUtf8("pushButton"))
        self.endTest = QtGui.QPushButton(Form)
        self.endTest.setGeometry(QtCore.QRect(610, 440, 91, 41))
        self.endTest.setObjectName(_fromUtf8("pushButton_2"))
        self.statudMac = QtGui.QLineEdit(Form)
        self.statudMac.setGeometry(QtCore.QRect(490, 20, 191, 20))
        self.statudMac.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(390, 20, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 111, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.oldSettings.setText(_translate("Form", "老化设置", None))
        self.startTest.setText(_translate("Form", "开始老化", None))
        self.endTest.setText(_translate("Form", "结束老化", None))
        self.label.setText(_translate("Form", "单节点状态查看：", None))
        self.label_2.setText(_translate("Form", "全部节点状态查看：", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
