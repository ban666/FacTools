#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: {liaoben}
# @Date:   2015-03-14 17:06:26
# @Last Modified by:   liaoben
# @Last Modified time: 2015-07-17 15:27:27

import sys,os,ConfigParser
import serial 
import time,threading
from multiprocessing import Process,Queue
import cmdgen
from PyQt4.QtCore import *

def CheckSum(data,jz=16):
    sum=0
    for i in range(0,len(data),2):
        sum+=int(data[i:i+2],jz)
    result='{:004x}'.format(sum)
    return result

def setZigbee(channel='15',panid='3125'):
    tstr=''.join(['000000000000a103',str(channel),panid])
    tstr=''.join(['F8e6',tstr,CheckSum(tstr)])
    return tstr

def deviceAccess(tstr,id):
    info=getDeviceInfo(tstr)
    tstr='000000000000a20a'+info[0]+id+info[1]
    csum=CheckSum(tstr)
    result='f8e6'+tstr+csum
    return result

def getDeviceInfo(tstr):
    mac=tstr[20:36]
    seq=tstr[36:38]
    result=[mac,seq]
    return result


class OldTestFunction(QThread):
    ot_okSignal = pyqtSignal(str)
    ot_controltimesSignal = pyqtSignal(str)
    ot_endtimeSignal = pyqtSignal(str)
    ot_errSignal = pyqtSignal(str)
    ot_terminalSignal = pyqtSignal(str)
    init_Signal = pyqtSignal(dict)
    statusChange_Signal = pyqtSignal(list)
    zigbeefile_Signal = pyqtSignal(str)
    def __init__(self,t,devicelist,parent=None):
        super(OldTestFunction,self).__init__(parent)
        self.content = ''
        self.timeout = 30
        self.channel = '15'
        self.lose_timeout = 300 #待调整
        self.iddict={}
        self.macdict={}
        self.typelist = []
        self.statusdict = {}
        self.control_times = 'null'
        self.end_time = 'null'
        self.t = t
        self.stopflag = False
        self.devicelist = devicelist
        self.devicedict={
            '01':'智能路由节点',
            '02':'智能调光器',
            '04':'智能调光器',
            '03':'智能门磁感应器',
            '06':'智能全向红外网关',
            '0d':'智能烟雾感应器',
            '0c':'人体红外感应器',
            '0e':'可燃气体感应器',
            '14':'智能单开',
            '15':'智能双开',
            '16':'智能三开',
            '11':'智能报警器',
            '13':'红外水晶开关',
            '17':'智能窗帘',
            '18':'智能窗户',
            '20':'情景面板'
            }

        self.device_statusdict={
            "02":[28,16,22],
            '03':[32,16,22],
            "04":[28,16,24],
            '0c':[32,16,22],
            '0d':[32,16,22],
            '0e':[56,20,24],
            "11":[26,16,22],
            '14':[26,16,22],
            '15':[28,16,24],
            '16':[30,16,26],
            '17':[30,16,26],
            '18':[30,16,26],
            '20':[26,16,22]
        }
        self.status_testdict={
            '03':[['F10401','F10400'],['打开','关闭']],
            "02":[['F10201','F10200'],['打开','关闭']],
            "04":[['F1020101', 'F1020001', 'F1020102', 'F1020002', 'F1020103', 'F1020003', 'F1020104', 'F1020004', 'F1020105', 'F1020005', 'F1020106', 'F1020006', 'F1020107', 'F1020007', 'F1020108', 'F1020008', 'F1020109', 'F1020009', 'F102010A', 'F102000A', 'F102010B', 'F102000B', 'F102010C', 'F102000C', 'F102010D', 'F102000D', 'F102010E', 'F102000E', 'F102010F', 'F102000F'] ,['灯光1级','关闭','灯光2级','关闭','灯光3级','关闭','灯光4级','关闭','灯光5级','关闭','灯光6级','关闭','灯光7级','关闭','灯光8级','关闭','灯光9级','关闭','灯光10级','关闭','灯光11级','关闭','灯光12级','关闭','灯光13级','关闭','灯光14级','关闭','灯光15级','关闭']], #调光状态位存疑
            '0c':[['F10401','F10400','F10402','F10403'],['红外报警','正常','防拆报警','防拆+报警']],#防拆状态位
            '0d':[['F10401','F10400','F10402','F10403'],['烟雾报警','正常','防拆报警','防拆+报警']],
            '0e':[['0001','0000','0100','0101'],['可燃报警','正常','防拆报警','防拆+报警']],
            '11':[['F10101','F10100'],['打开','关闭']],
            '14':[['F10101','F10100'],['1开','1关']],
            '15':[['F1020100','F1020101','F1020001','F1020000'],['1开2关','1开2开','1关2开','1关2关']],
            '16':[['F103010000','F103010001','F103010100','F103010101','F103000101','F103000100','F103000001','F103000000'],['1开2关3关','1开2关3开','1开2开3关','1开2开3开','1关2开3开','1关2开3关','1关2关3开','1关2关3关']],
            '17':[['F103010000','F103000100','F103000001'],['打开','暂停','关闭']],
            '18':[['F103010000','F103000100','F103000001'],['打开','暂停','关闭']],
            '20':[['F10101','F10102','F10103','F10104','F10100'],['执行情景1','执行情景2','执行情景3','执行情景4','无情景执行']]
        }
    #generate id for devicelist,send whitelist to zigbee
    def id_gen(self):
        for i in range(len(self.devicelist)):
            mac = str(self.devicelist[i])[:16]
            id = str('{:2x}'.format(i+1))
            typestr = str(self.devicelist[i])[16:18]
            type = self.devicedict[typestr]
            self.iddict[mac] = str('{:02x}'.format(i+1))
            self.statusdict[id] = [str(i),mac,type,'否','','']
            if str(self.devicelist[i])[-1:] == str(2):
                self.typelist.append(str('{:04x}'.format(i+1))+','+typestr)
        print self.statusdict
        self.init_Signal.emit(self.statusdict)

    def clear_q(self,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass

    def gen_cmd_for_oldtest(self):
        print 'typelist:',self.typelist
        cmdg = cmdgen.CmdGenerate(self.typelist)
        cmdlist = cmdg.CmdGenForOldTest()
        return cmdlist

    def run_by_control_times(self,cmdlist):
        try:
            for i in range(int(self.control_times)):
                if self.stopflag == True:
                        break
                for j in cmdlist:
                    if self.stopflag == True:
                            break
                    self.t.write(j.decode('hex'))
                    time.sleep(1)
                self.ot_controltimesSignal.emit(str(i+1))
                print 'control times:',i+1
        except Exception as e:
                print 'run_by_control_times,error!!!!!!',e
                self.ot_terminalSignal.emit('terminal')
                return

    def run_by_end_time(self,cmdlist):
        c_times = 0
        terminal_time = self.sec2time(self.end_time).split(':')[:2]
        while True:
            if self.stopflag == True:
                            break
            try:
                for j in cmdlist:
                    if self.stopflag == True:
                            break
                    now_time = int(time.time())
                    if self.sec2time(now_time).split(':')[:2] == terminal_time:
                        self.ot_terminalSignal.emit('terminal')
                        raise
                    #print cmd
                    self.t.write(j.decode('hex'))
                    time.sleep(1)
                c_times +=1
                self.ot_controltimesSignal.emit(str(c_times))
            except Exception as e:
                print 'run_by_end_time,error!!!!!!',e
                self.ot_terminalSignal.emit('terminal')
                return

    def ana_data(self,q):
        while True:
            try:
                if self.stopflag == True:
                    break
                t_data = q.get(timeout=0.01)
                if t_data != '':
                    self.data_check(str(t_data))
                time.sleep(0.01)
            except Exception as e:
                pass

    def data_check(self,tstr):
        id = tstr[6:8]
        data_len = len(tstr.strip())
        try:
            device_type = tstr[14:16]
            status_len = self.device_statusdict[device_type][0]
            status_str = tstr[self.device_statusdict[device_type][1]:self.device_statusdict[device_type][2]].upper()
        except:
            pass
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if data_len == 42 and tstr[16:20] == 'a209':
            return
        if data_len == 14 and tstr[8:14] == 'access':
            print 'accese'
            self.statusdict[id][3:] = ['是','',nowtime]
            print self.statusdict[id]
            self.statusChange_Signal.emit(self.statusdict[id])
            return
        if data_len == 52:
            print 'accesee'
            self.statusdict[id][3:] = ['是','',nowtime]
            self.statusChange_Signal.emit(self.statusdict[id])
            return
        elif data_len == status_len:
            try:
                index=self.status_testdict[device_type][0].index(status_str)
                device_status = self.status_testdict[device_type][1][index]
                self.statusdict[id][3:] = ['是',device_status,nowtime]
                self.statusChange_Signal.emit(self.statusdict[id])
                print id,device_status
                return
            except Exception as e :
                print 'data_check:',e


    def sec2time(self,sec):
        sec = int(sec)
        h = '{:04d}'.format(sec/3600)
        m = '{:02d}'.format(sec%3600/60)
        s = '{:02d}'.format(sec%60)
        tstr = str(h)+':'+str(m)+':'+str(s)
        return tstr


    def run(self):
        cmdlist = self.gen_cmd_for_oldtest()
        print cmdlist
        if len(cmdlist) == 0:
            return
        if self.control_times!='null':
            self.run_by_control_times(cmdlist)
        else:
            self.run_by_end_time(cmdlist)


    def check_online(self,q):
        s_time = time.time()
        device_num = len(self.statusdict)
        while True:
            if self.stopflag == True:
                self.ot_terminalSignal.emit('terminal')
                return
            check_num = 0
            time_range = '{:.2f}'.format(time.time()-s_time)
            if int(float(time_range)) == int(self.timeout):
                return False
            for i,j in self.statusdict.items():
                if j[3] == '是':
                    check_num +=1
            if check_num == device_num:
                return True
            #print int(float(time_range)),self.timeout

            time.sleep(0.01)

    def login_test(self,q):
        check_result = self.check_online(q)
        if check_result == True:
            self.ot_okSignal.emit('ok')
        elif check_result == False:
            self.ot_okSignal.emit('fail')
        else:
            self.ot_okSignal.emit('block')

    def judge_loseconnect(self):
        stime = time.time()
        while True:
            try:
                if self.stopflag == True:
                    break
                nowtime = time.time()
                if int(nowtime) == self.end_time:
                    self.ot_terminalSignal.emit('terminal')
                    break
                send_str = time.time() - stime
                self.ot_endtimeSignal.emit(self.sec2time(send_str))
                for i,j in self.statusdict.items():
                    if j[3]=='是':
                        endtime = time.mktime(time.strptime(j[-1],"%Y-%m-%d %H:%M:%S"))
                        if time.time() - endtime > self.lose_timeout:
                            j[3] = '掉线'
                            self.statusChange_Signal.emit(j)
                time.sleep(0.5)
            except Exception as e:
                print 'judge_loseconnect',e
            finally:
                pass

    def com_read(self,q,channel,zfile):
        print 'channel:',channel
        fol = os.getcwd()+'/Log/'
        with open(zfile,'w') as f:
            #print file
            while True:
                buffer=''
                try:
                    nowtime = time.time()
                    if int(nowtime) == self.end_time:
                        #self.terminalSignal.emit('terminal')
                        raise

                    rlength=self.t.inWaiting()

                    if rlength>=12:
                        buffer+=self.t.read(rlength).encode('hex')
                    while len(buffer) >= 24:
                        if (buffer[0:4] == 'f8e6'):
                            #init
                            if buffer=='f8e6000000000000a10000a1':
                                self.t.write(setZigbee(channel=channel).decode('hex'))

                            dlength=(int(buffer[18:20],16)+12)*2
                            if (len(buffer)<dlength):
                                break
                            #checksum
                            checksum=CheckSum(buffer[4:dlength-4])
                            if(checksum!=buffer[dlength-4:dlength]):
                                buffer=buffer[dlength:]
                                continue
                            #get correct data
                            cdata=buffer[:dlength]

                            q.put(cdata)
                            if dlength==42 and cdata[16:20]=='a209':
                                print self.iddict
                                mac=cdata[20:36]
                                #print self.iddict
                                if self.iddict.has_key(mac):
                                    id=self.iddict[mac]
                                    print id,mac
                                    access_cmd=deviceAccess(cdata,id).decode('hex')
                                    self.t.write(access_cmd)
                                    q.put('f8e600'+id+'access')

                            buffer=buffer[dlength:]
                            tstr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+cdata+'\n'
                            #print tstr
                            f.write(tstr)
                            f.flush()
                        else:
                            buffer=buffer[1:]
                except Exception as e:
                    pass

                time.sleep(0.05)

class TestThread(threading.Thread):

    def __init__(self,t,channel,thread_num=0, timeout=0.01):
        super(TestThread, self).__init__()
        self.thread_num = thread_num
        self.channel = channel
        self.t = t
        self.stopped = False
        self.timeout = timeout

    def run(self):
        global q,p
        subthread = threading.Thread(target=Dt(self.t).com_read, args=(q,p,self.channel,))
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            subthread.join(self.timeout)

        print('Thread stopped')

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped

if __name__ == '__main__':
    q = Queue()
    whitelist = ['00124b0004f0021b16','00124b0003a60fa614']
    t = ''
    dl = ['1234567980123456160']
    oldtest = OldTestFunction(t,dl)
    b = oldtest.id_gen()
    print b
    '''
    t2 = threading.Thread(target=OldTestFunction(t,whitelist).login_test,args=(q,))

    t1 = threading.Thread(target=DisTestFunction(t,whitelist).com_read,args=(q,'17',))
    t1.start()
    t2.start()
    '''