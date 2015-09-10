# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oldtestui.ui'
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
        Form.resize(806, 622)
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(25, 101, 741, 461))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(100)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnWidth(0,140)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(1,80)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.setColumnWidth(3,80)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.setColumnWidth(4,140)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.setColumnWidth(5,140)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        self.oldSettings = QtGui.QPushButton(Form)
        self.oldSettings.setGeometry(QtCore.QRect(490, 580, 71, 31))
        self.oldSettings.setObjectName(_fromUtf8("oldSettings"))
        self.startTest = QtGui.QPushButton(Form)
        self.startTest.setGeometry(QtCore.QRect(590, 580, 71, 31))
        self.startTest.setObjectName(_fromUtf8("startTest"))
        self.endTest = QtGui.QPushButton(Form)
        self.endTest.setGeometry(QtCore.QRect(690, 580, 71, 31))
        self.endTest.setObjectName(_fromUtf8("endTest"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 40, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.currentTimes = QtGui.QLCDNumber(Form)
        self.currentTimes.setGeometry(QtCore.QRect(130, 30, 251, 51))
        self.currentTimes.setNumDigits(10)
        self.currentTimes.setDigitCount(10)
        self.currentTimes.setObjectName(_fromUtf8("currentTimes"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(400, 40, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.remainTime = QtGui.QLCDNumber(Form)
        self.remainTime.setGeometry(QtCore.QRect(490, 30, 251, 51))
        self.remainTime.setSmallDecimalPoint(True)
        self.remainTime.setNumDigits(10)
        self.remainTime.setDigitCount(10)
        self.remainTime.display('0000:00:00')
        self.remainTime.setObjectName(_fromUtf8("remainTime"))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "设备MAC", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "设备类型", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "是否在网", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "设备状态", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "数据开始时间", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "数据更新时间", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        '''
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "123456789012345616", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "是", None))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "1开", None))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Form", "2", None))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Form", "2015-08-08 20:11:22", None))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Form", "4", None))
        '''
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.oldSettings.setText(_translate("Form", "老化设置", None))
        self.startTest.setText(_translate("Form", "开始老化", None))
        self.endTest.setText(_translate("Form", "结束老化", None))
        self.label.setText(_translate("Form", "当前控制次数：", None))
        self.label_2.setText(_translate("Form", "运行时间：", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())