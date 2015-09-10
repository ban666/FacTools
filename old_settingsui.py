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
        self.label_6.setGeometry(QtCore.QRect(480, 130, 181, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(480, 240, 331, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_12 = QtGui.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(340, 50, 211, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(170, 130, 301, 391))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(100)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnWidth(0,140)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(1,110)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(480, 160, 181, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(480, 220, 181, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(480, 180, 181, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(480, 200, 181, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        for i in range(100):
            item = QtGui.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 1, item)
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
        #self.label_7.setText(_translate("Form", "需进行控制测试的设备请在 是否需要进行控制测试栏填入 是", None))
        self.label_12.setText(_translate("Form", "控制次数与结束时间至少填写一项", None))
        '''
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        '''
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "设备MAC", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "是否进行控制测试", None))
        self.label_8.setText(_translate("Form", "00124b000a01354516", None))
        self.label_11.setText(_translate("Form", ".......", None))
        self.label_9.setText(_translate("Form", "00124b000a01354614", None))
        self.label_10.setText(_translate("Form", "00124b000a01354715", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
