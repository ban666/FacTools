#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

from serial import Serial
from time import sleep
#import threading
import random
from PyQt4.QtCore import *

class Controller(QThread):

    sinOut = pyqtSignal(str)

    def __init__(self,parent=None):
        super(Controller,self).__init__(parent)

        self.identity = None

    def setIdentity(self,text):
        self.identity = text

    def setVal(self,val):
        self.times = int(val)

        self.start()

    def run(self):
        while True:
            abc=raw_input('aaaa:')
            self.sinOut.emit(abc+" "+str(self.times))
            self.times -= 1
            sleep(1)