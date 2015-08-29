# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys,os
import random,time,threading
from uitest import Ui_MainWindow as ui
import serial
import cmdgen
from multiprocessing import Process,Queue
from devicetest_ui import *

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
stopflag = False
class AutoTools(QtGui.QMainWindow, ui):


    def __init__(self, parent = None):
        super(AutoTools, self).__init__(parent)
        self.ui = ui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.p1)
        self.terminate = False
        self.result = ''
        self.content = ''
        self.t = ''
        self.p = Queue()
        self.q = Queue()
        self.defaultid = ''
        self.timeout = 10
        self.defaultid = '77'
        self.iddict ={}
        self.loginstr=''
        self.devicedict={
            '01':'智能路由节点',
            '04':'智能调光器',
            '03':'智能门磁感应器',
            '06':'智能全向红外网关',
            '0d':'智能烟雾感应器',
            '0f':'一氧化碳感应器',
            '0c':'人体红外感应器',
            '0e':'可燃气体感应器',
            '14':'智能单开',
            '15':'智能双开',
            '16':'智能三开',
            '11':'智能报警器',
            '13':'红外水晶开关',
            '17':'智能窗帘',
            '18':'智能窗户'
            }

        self.testdict = {
            '01':[self.login_test],
            '04':[self.login_test,self.status_test,self.control_test],
            '03':[self.login_test,self.status_test],
            '06':[self.login_test],
            '0d':[self.login_test,self.status_test],
            '0f':[self.login_test,self.status_test],
            '0c':[self.login_test,self.status_test],
            '0e':[self.login_test,self.status_test],
            '14':[self.login_test,self.status_test,self.control_test],
            '15':[self.login_test,self.status_test,self.control_test],
            '16':[self.login_test,self.status_test,self.control_test],
            '11':[self.login_test,self.control_test],
            '17':[self.login_test,self.status_test,self.control_test],
            '18':[self.login_test,self.status_test,self.control_test]
        }

        self.statusdict={
            "04":[28,16,22],
            "11":[32,16,22],
            '14':[26,16,24],
            '15':[28,16,24],
            '16':[30,26,36],
            '17':[30,16,26],
            '18':[30,16,26]
        }

        #self.serialOpend = False
        
        #sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def onSendData(self,data):
        if len(data)==18:
            print data
            return data

    def slotName(self):
        content,ok=QtGui.QInputDialog.getText(self,self.tr('二维码扫描'),
                                     self.tr('请扫描二维码:'),
                                     QtGui.QLineEdit.Normal,'')
        if ok:
            if len(content)!=18 or not self.devicedict.has_key(str(content[-2:])):
                self.printForUi(u'条形码错误，请检查！\n')

                return False
            else:
                tstr = "设备mac: "+str(content[:16]) +" "+ "设备类型: "+ self.devicedict[str(content[-2:])]+'\n'
                self.printForUi(tstr.decode('utf-8'.encode('gbk')))
                self.result = True
                self.content = content
                return content
        else:
            return 'terminate'

    def printForUi(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text
        self.tc = self.ui.textEdit.textCursor()
        self.tc.movePosition(self.tc.End)
        self.ui.textEdit.setTextCursor(self.tc)
        self.ui.textEdit.insertPlainText(text)
        for c in text:
            if c == '\n':
                self.vsb = self.ui.textEdit.verticalScrollBar()
                self.vsb.setSliderPosition(self.vsb.maximum())

    def printtest(self,text):
        while True:
            self.normalOutputWritten(text)
            time.sleep(1)

    def clear_q(self):
        while not self.p.empty():
            try:
                self.p.get(timeout=0.01)
            except:
                pass

    def set_whitelist(self,content):
        while not self.p.empty():
            try:
                self.p.get(timeout=0.01)
            except:
                pass
            time.sleep(0.1)
        tstr = content[:16]+self.defaultid
        self.p.put(tstr)
        #print 'put:',tstr

    def checkonline(self,content):
        s_time = time.time()
        t_info = content[:16]+'00'+self.defaultid
        t_data=''
        self.login_thread = MyThread()
        self.login_thread.sinOut.connect(self.printForUi)
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = self.q.get(timeout=0.01)
            except:
                pass
            if t_data[20:40] == t_info:
                #printstr = '入网时间为:'.decode('utf-8').encode('gbk') +str(time_range)
                self.loginstr = u'入网时间为:' + str(time_range) +'\n'+u'入网测试结果：PASS'+'\n'
                self.login_thread.text = self.loginstr
                self.login_thread.setVal(1)
                '''
                self.printForUi(u'入网时间为:')
                self.printForUi(str(time_range))
                self.printForUi('\n')
                #printstr = .decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：PASS')
                self.printForUi('\n')
                self.result = True
                '''
                break
                #return True
            if int(float(time_range)) == self.timeout:
                self.loginstr =  u'设备在规定时间内未能入网,入网测试结果：FAIL'+'\n'
                '''
                self.printForUi(u'设备在规定时间内未能入网')
                self.printForUi('\n')
                printstr = '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：FAIL')
                self.printForUi('\n')
                '''
                self.result = False
                break
                #return False
            time.sleep(0.01)

    def checkonline2(self,content):
        s_time = time.time()
        t_info = content[:16]+'00'+self.defaultid
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = self.q.get(timeout=0.01)
            except:
                pass
            if t_data[20:40] == t_info:
                self.printForUi(u'入网时间为:'+str(time_range)+u'秒\n')
                self.printForUi(u'入网测试结果：PASS\n')
                self.result = True
                break
                #return True
            if int(float(time_range)) == self.timeout:
                self.loginstr =  u'设备在规定时间内未能入网,入网测试结果：FAIL'+'\n'
                '''
                self.printForUi(u'设备在规定时间内未能入网')
                self.printForUi('\n')
                printstr = '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：FAIL')
                self.printForUi('\n')
                '''
                self.result = False
                break
                #return False
            time.sleep(0.01)

    def login_test(self,content):
        printstr = '入网测试启动...'.decode('utf-8').encode('gbk')
        print 11111
        self.printForUi(u'入网测试启动,请将设备上电并等待...\n')
        time.sleep(1)
        self.set_whitelist(content)
        #self.checkonline(content)
        self.checkonline = CheckOnline()
        self.checkonline.start()
        self.connect(self.checkonline,QtCore.SIGNAL('output(QString)'),self.printForUi())
        '''
        checkonline = threading.Thread(target=self.checkonline,args=(content,))
        checkonline.start()
        while self.loginstr == '':
            QtCore.QThread.msleep(100)
        self.printForUi(self.loginstr)
        self.loginstr = ''
        '''
        result = self.result
        #checkonline.join()
        return result

    def status_test(self):
        print '状态上传测试启动...'.decode('utf-8').encode('gbk')
        pass

    def control_test(self,content):
        print '控制测试启动...'.decode('utf-8').encode('gbk')
        result = 0
        type = content[16:]
        tlen = self.statusdict[type][0]
        sid  = self.statusdict[type][1]
        did  = self.statusdict[type][2]
        id_type = '00'+self.defaultid+','+type
        cmdlist,statuslist = cmdgen.CmdGenerate(id_type).CmdGen()
        cmdlist=[x.decode('hex') for x in cmdlist]

        for i in range(len(cmdlist)):
            self.clear_q(self.q)
            self.t.write(cmdlist[i])
            s_time = time.time()
            while True:
                time_range = time.time()-s_time
                try:
                    t_data = self.q.get(timeout=0.01)
                except:
                    pass
                if len(t_data) == tlen and t_data[sid:did] == statuslist[i]:
                    result = 1
                    break
                if int(float(time_range)) == self.timeout:
                    print '设备在规定时间内未收到控制响应信息'.decode('utf-8').encode('gbk')
                    print '控制测试结果：FAIL'.decode('utf-8').encode('gbk')
                    return False

                time.sleep(0.01)
        if result == 1:
            print '设备控制测试通过'.decode('utf-8').encode('gbk')
            print '控制测试结果：Pass'.decode('utf-8').encode('gbk')
            return True

    def device_test(self):
        global stopflag
        while True:

            content=self.slotName()
            if content == 'terminate':
                self.terminate = True
                #time.sleep(2)
                time.sleep(0.1)
                stopflag =True
                self.t2.stop()
                self.t2.join()
                self.t.close()
                break
            if content == False:
                continue
            if not self.login_test(content):
                continue
            continue


    def t3(self):
        self.t = serial.Serial(0,38400)
        zb = ZigbeeTools(self.t)
        zb.com_read(self.q,self.p)
        return zb

    def p1(self):
        self.t = serial.Serial(0,38400)
        #self.t2 = threading.Thread(target=ZigbeeTools(self.t).com_read, args=(self.p,self.q,))
        self.t2 = TestThread(self.t,self.q,self.p)
        self.t2.start()
        print 'Zigbee start'
        '''
        self.st = StartTest(self.t,self.t2)
        self.st.func = self.slotName()
        self.st.setVal()
        '''
        #self.t2.stop()
        #self.t2.join()
        #self.t2 = TestThread(self.t,self.q,self.p)
        #self.t2.start()
        #self.device_test()
        #self.t3 = threading.Thread(target=self.device_test, args=())
        #self.t3.start()
        self.device_test()

    def setDispTEFocus(self):
        self.ui.textEdit.setFocus()


class CheckOnline(QtCore.QThread):
    def __init__(self,content,q,parent=None):
        super(CheckOnline,self).__init__(parent)
        self.content = content
        self.working=True
        self.q =q
        self.defaultid = '77'
        self.num=0
    def __del__(self):
        self.working=False
        self.wait()

    def run(self):
        s_time = time.time()
        t_info = self.content[:16]+'00'+self.defaultid
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = self.q.get(timeout=0.01)
            except:
                pass
            if t_data[20:40] == t_info:
                #printstr = '入网时间为:'.decode('utf-8').encode('gbk') +str(time_range)
                self.loginstr = u'入网时间为:' + str(time_range) +'\n'+u'入网测试结果：PASS'+'\n'
                self.emit(QtCore.SIGNAL('output(QString)'),self.loginstr)
                '''
                self.printForUi(u'入网时间为:')
                self.printForUi(str(time_range))
                self.printForUi('\n')
                #printstr = .decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：PASS')
                self.printForUi('\n')
                self.result = True
                '''
                break
                #return True
            if int(float(time_range)) == self.timeout:
                self.loginstr =  u'设备在规定时间内未能入网,入网测试结果：FAIL'+'\n'
                self.emit(QtCore.SIGNAL('output(QString)'),self.loginstr)
                '''
                self.printForUi(u'设备在规定时间内未能入网')
                self.printForUi('\n')
                printstr = '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：FAIL')
                self.printForUi('\n')
                '''
                self.result = False
                break
                #return False
            time.sleep(0.01)


class StartTest(QtCore.QThread):

    sinOut = QtCore.pyqtSignal(str)

    def __init__(self,t,t2,parent=None):
        super(StartTest,self).__init__(parent)
        self.t = t
        self.t2 = t2
        self.restart = False
        self.func =''



    def set_whitelist(self,content):
        while not self.p.empty():
            try:
                self.p.get(timeout=0.01)
            except:
                pass
            time.sleep(0.1)
        tstr = content[:16]+self.defaultid
        self.p.put(tstr)
        #print 'put:',tstr

    def checkonline(self,content):
        s_time = time.time()
        t_info = content[:16]+'00'+self.defaultid
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = self.q.get(timeout=10)
            except:
                pass
            if t_data[20:40] == t_info:
                #printstr = '入网时间为:'.decode('utf-8').encode('gbk') +str(time_range)

                self.loginstr = u'入网时间为:' + str(time_range) +'\n'+u'入网测试结果：PASS'+'\n'
                self.login_thread.text = self.loginstr
                self.login_thread.setVal(1)
                '''
                self.printForUi(u'入网时间为:')
                self.printForUi(str(time_range))
                self.printForUi('\n')
                #printstr = .decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：PASS')
                self.printForUi('\n')
                self.result = True
                '''
                break
                return True
            if int(float(time_range)) == self.timeout:
                self.loginstr =  u'设备在规定时间内未能入网:'  +'\n'+u'入网测试结果：FAIL'+'\n'
                '''
                self.printForUi(u'设备在规定时间内未能入网')
                self.printForUi('\n')
                printstr = '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                self.printForUi(u'入网测试结果：FAIL')
                self.printForUi('\n')
                '''
                self.result = False
                break
                return False
            time.sleep(10)

    def login_test(self,content):
        printstr = '入网测试启动...'.decode('utf-8').encode('gbk')
        print 11111
        self.printForUi(u'入网测试启动,请将设备上电并等待...')
        time.sleep(1)
        self.set_whitelist(content)
        self.checkonline(content)
        #checkonline = threading.Thread(target=self.checkonline,args=(content,))
        #checkonline.start()
        #checkonline.join()
        #while self.loginstr == '':
            #time.sleep(1)
        #print self.loginstr
        result = self.result
        return result

    def setText(self,text):
        self.text = text

    def setVal(self):
        #self.times = int(val)

        ##执行线程的run方法
        self.start()
        print 'mythread start'

    def run(self):
        global stopflag
        a = self.func
        while True:
            content = b
            if content == 'terminate':
                self.terminate = True
                #time.sleep(2)
                time.sleep(0.1)
                stopflag =True
                self.t2.stop()
                self.t2.join()
                self.t.close()
                break
            if content == False:
                continue
            if not self.login_test(content):
                continue
            continue

class MyThread(QtCore.QThread):

    sinOut = QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)
        self.identity = None

    def setText(self,text):
        self.text = text

    def setVal(self,val):
        #self.times = int(val)

        ##执行线程的run方法
        self.start()
        print 'mythread start'

    def run(self):
        #while 1:
            ##发射信号
        self.sinOut.emit(self.text)
        #    time.sleep(1)

class TestThread(threading.Thread):

    def __init__(self,t,q,p, thread_num=0, timeout=0.01):
        super(TestThread, self).__init__()
        self.thread_num = thread_num
        self.t = t
        self.q = q
        self.p = p
        self.stopped = False
        self.timeout = timeout

    def run(self):
        def target_func():
            inp = raw_input("Thread %d: " % self.thread_num)
            print('Thread %s input %s' % (self.thread_num, inp))
        subthread = threading.Thread(target=ZigbeeTools(self.t).com_read, args=(self.p,self.q,))
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            subthread.join(self.timeout)

        print('Thread stopped')

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped

class ZigbeeTools:
    def __init__(self,t):
        self.timeout = 60
        self.defaultid = '77'
        self.channel = '15'
        self.t = t
        self.iddict = {}
        #print t
        self.folder = os.getcwd()+'/Log/'
        self.stopped = stopflag
    def CheckSum(self,data,jz=16):
        sum=0
        for i in range(0,len(data),2):
            sum+=int(data[i:i+2],jz)
        result='{:004x}'.format(sum)
        return result

    def setZigbee(self,channel='15',panid='3125'):
        tstr=''.join(['000000000000a103',channel,panid])
        tstr=''.join(['F8e6',tstr,self.CheckSum(tstr)])
        return tstr

    def deviceAccess(self,tstr,id):
        info=self.getDeviceInfo(tstr)
        tstr='000000000000a20a'+info[0]+id+info[1]
        csum=self.CheckSum(tstr)
        result='f8e6'+tstr+csum
        return result

    def getDeviceInfo(self,tstr):
        mac=tstr[20:36]
        seq=tstr[36:38]
        result=[mac,seq]
        return result

    def stop(self):
        self.stopped = True
        print 'stopped!!!!!!'

    def com_start(self,q,p):
        subthread = threading.Thread(target=ZigbeeTools(self.t).com_read, args=(q,p,))
        subthread.start()


    def isStopped(self):
        return self.stopped

    def com_read(self,q,p):
        global stopflag
        file = self.folder + time.strftime("%Y%m%d%H%M%S", time.localtime())+'.txt'
        with open(file,'w') as f:
            while True:
                if stopflag == True:
                    print 'stopped!!!'
                    break
                buffer=''
                try :
                    rlength=self.t.inWaiting()
                except Exception as e:
                    #print e
                    pass
                if rlength>=12:
                    buffer+=self.t.read(rlength).encode('hex')
                while len(buffer) >= 24:
                    if (buffer[0:4] == 'f8e6'):
                        #init
                        if buffer=='f8e6000000000000a10000a1':
                            self.t.write(self.setZigbee(channel=self.channel).decode('hex'))

                        dlength=(int(buffer[18:20],16)+12)*2
                        if (len(buffer)<dlength):
                            break
                        #checksum
                        checksum=self.CheckSum(buffer[4:dlength-4])
                        if(checksum!=buffer[dlength-4:dlength]):
                            buffer=buffer[dlength:]
                            continue
                        #get correct data
                        cdata=buffer[:dlength]

                        q.put(cdata)
                        iddict_new=''
                        try:
                            iddict_new = p.get(timeout=0.01)
                        except:
                            pass
                        if iddict_new !='':
                            #print 'get',iddict_new
                            self.iddict = {iddict_new[:16]:iddict_new[16:]}
                        #print self.iddict
                        #id mac generate
                        if dlength==42 and cdata[16:20]=='a209':
                            mac=cdata[20:36]
                            #print self.iddict
                            if self.iddict.has_key(mac):
                                id=self.iddict[mac]
                                print id,mac
                                access_cmd=self.deviceAccess(cdata,id).decode('hex')
                                self.t.write(access_cmd)

                        data_flag=1
                        buffer=buffer[dlength:]
                        tstr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+cdata+'\n'
                        #print tstr
                        f.write(tstr)
                        f.flush()
                    else:
                        buffer=buffer[1:]

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ps = AutoTools()
    ps.show()
    sys.exit(app.exec_())
