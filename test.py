# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import random
import time,threading
from PyTextEdit import PyTextEdit
from multiprocessing import Process

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 80, 75, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textEdit = PyTextEdit(self.centralwidget)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(False)
        self.textEdit.setCursorWidth(9)
        self.textEdit.setGeometry(QtCore.QRect(130, 70, 104, 64))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTest3 = QtGui.QMenu(self.menubar)
        self.menuTest3.setObjectName(_fromUtf8("menuTest3"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTest3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        #self.connect(pushButton, QtCore.SIGNAL("clicked()"), self,
                     #QtCore.SLOT("test()"
        #self.pushButton.clicked.connect(self.p1)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def p1(self):
        t1 = threading.Thread(target=self.test1(),args=())

        t2 = threading.Thread(target=self.test2(),args=())
        t2.start()
        t1.start()
        self.connect(self.cw.ui.dispTE.qObj, QtCore.SIGNAL('SerialSendData'), self.onSendData)

    def test1(self):
        a= random.randint(0,1000)
        a=str(a)+self.textEdit.toPlainText()
        #a=str(a)+self.textEdit.toPlainText()
        #QtGui.QMessageBox.information(self.pushButton, u"信息", u"由槽弹出")
        self.textEdit.setText(a)
        print a

    def test2(self):
        a='abc'
        self.textEdit.setText(str(a)+self.textEdit.toPlainText())
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.menuTest3.setTitle(_translate("MainWindow", "测试1", None))
        self.menu_2.setTitle(_translate("MainWindow", "测试2", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

