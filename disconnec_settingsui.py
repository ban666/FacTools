# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dis_setting.ui'
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
        Form.resize(594, 434)
        self.saveSettings = QtGui.QPushButton(Form)
        self.saveSettings.setGeometry(QtCore.QRect(470, 380, 75, 23))
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
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(90, 130, 71, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gen_type = QtGui.QComboBox(Form)
        self.gen_type.setGeometry(QtCore.QRect(170, 130, 151, 20))
        self.gen_type.setObjectName(_fromUtf8("Com"))
        self.gen_type.addItem(_fromUtf8(""))
        self.gen_type.addItem(_fromUtf8(""))
        self.gen_type.addItem(_fromUtf8(""))

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(90, 170, 71, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.disTimes = QtGui.QLineEdit(Form)
        self.disTimes.setGeometry(QtCore.QRect(170, 50, 151, 20))
        self.disTimes.setObjectName(_fromUtf8("disTimes"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 90, 181, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.deviceList = QtGui.QTextEdit(Form)
        self.deviceList.setGeometry(QtCore.QRect(170, 170, 151, 231))
        self.deviceList.setObjectName(_fromUtf8("deviceList"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(340, 170, 181, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(340, 200, 181, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(340, 2300, 181, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(340, 240, 181, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(340, 270, 181, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(340, 290, 181, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(340, 50, 211, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.saveSettings.setText(_translate("Form", "设置", None))
        self.label.setText(_translate("Form", "通断次数", None))
        self.label_2.setText(_translate("Form", "结束时间", None))
        self.label_3.setText(_translate("Form", "待通断设备", None))
        self.label_4.setText(_translate("Form", "控制策略", None))
        self.label_5.setText(_translate("Form", "eg:2015-08-19 20:17:35", None))
        self.deviceList.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_6.setText(_translate("Form", "请输入通断设备18位二维码", None))
        self.label_7.setText(_translate("Form", "以换行分隔，如：", None))
        self.label_8.setText(_translate("Form", "00124b000a01354516", None))
        self.label_9.setText(_translate("Form", "00124b000a01354614", None))
        self.label_10.setText(_translate("Form", "00124b000a01354715", None))
        self.label_11.setText(_translate("Form", ".......", None))
        self.label_12.setText(_translate("Form", "通断次数与结束时间至少填写一项", None))
        self.gen_type.setItemText(0, _translate("Form", "单点通断", None))
        self.gen_type.setItemText(1, _translate("Form", "全向通断", None))
        self.gen_type.setItemText(2, _translate("Form", "反向通断", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())