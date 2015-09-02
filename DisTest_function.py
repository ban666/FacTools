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

def fileGen(confgfile='work.cfg'):
    config=ConfigParser.ConfigParser()
    with open(confgfile,"r") as cfgfile:
        config.readfp(cfgfile)
        work_directory = config.get('conf','work_directory')
        channel =config.get('conf','channel')
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    macfile=work_directory+'Macinfo.txt'
    wfile=work_directory+date+'.txt'
    result = [macfile,wfile,channel]
    return result

def CheckSum(data,jz=16):
    sum=0
    for i in range(0,len(data),2):
        sum+=int(data[i:i+2],jz)
    result='{:004x}'.format(sum)
    return result

def setZigbee(channel='15',panid='3125'):
    tstr=''.join(['000000000000a103',channel,panid])
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


class DisTestFunction(QThread):
    okSignal = pyqtSignal(str)
    controltimesSignal = pyqtSignal(str)
    endtimeSignal = pyqtSignal(str)
    errSignal = pyqtSignal(str)
    def __init__(self,t,whitelist,parent=None):
        super(DisTestFunction,self).__init__(parent)
        self.content = ''
        self.timeout = 30
        self.channel = '15'
        self.iddict={}
        self.typelist = []
        self.control_times = 'null'
        self.end_time = 'null'
        self.t = t
        self.stopflag = False
        self.whitelist=whitelist
        self.id_gen()
        self.devicedict={
            '01':'智能路由节点',
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
            '18':'智能窗户'
            }

    def id_gen(self):
        for i in range(len(self.whitelist)):
            self.iddict[str(self.whitelist[i])[:16]] = str('{:02x}'.format(i+1))
            self.typelist.append(str('{:04x}'.format(i+1))+','+str(self.whitelist[i])[16:])

    def clear_q(self,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass

    def gen_cmd_for_distest(self):
        cmdg = cmdgen.CmdGenerate(self.typelist)
        cmdlist = cmdg.CmdGenForDisTest()
        cmdlist=[x.decode('hex') for x in cmdlist]
        return cmdlist

    def run_by_control_times(self,cmdlist):
        try:
            for i in range(int(self.control_times)):
                if self.stopflag == True:
                    break
                for j in range(len(cmdlist)):
                    self.t.write(cmdlist[j][0].decode('hex'))
                    time.sleep(1)
                for k in range(len(cmdlist)):
                    self.t.write(cmdlist[k][1].decode('hex'))
                    time.sleep(1)
                self.controltimesSignal.emit(str(i+1))
        except Exception as e:
                print 'run_by_control_times,error!!!!!!',e
                return

    def run_by_end_time(self,cmdlist):
        while True:
            now_time = int(time.time())
            if now_time == self.end_time:
                break
            if self.stopflag == True:
                    break
            try:
                for j in range(len(cmdlist)):
                    self.t.write(cmdlist[j][0].decode('hex'))
                    self.endtimeSignal.emit(time.time())
                    time.sleep(1)
                for k in range(len(cmdlist)):
                    self.t.write(cmdlist[k][1].decode('hex'))
                    self.endtimeSignal.emit(time.time())
                    time.sleep(1)
            except Exception as e:
                print 'run_by_end_time,error!!!!!!',e
                return

    def run(self):
        cmdlist = self.gen_cmd_for_distest()
        if self.control_times!='null' and self.end_time!='null':
            self.run_by_end_time(cmdlist)
        elif self.control_times!='null' and self.end_time == 'null':
            self.run_by_control_times(cmdlist)
        elif self.control_times=='null' and self.end_time != 'null':
            self.run_by_control_times(cmdlist)
        else:
            self.errSignal.emit(u'配置出错，请检查！')

    def check_online(self,q):
        s_time = time.time()
        t_info = []
        for (i,j) in self.iddict.items():
            t_info.append(i+'00'+j)
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = q.get(timeout=0.01)
            except:
                pass
            if len(t_info) == 0:
                return True
            if t_data[20:40] in t_info:
                t_info.pop(t_info.index(t_data[20:40]))
                print 'pop:',t_info
            if int(float(time_range)) == self.timeout:
                return False
            time.sleep(0.01)



    def com_read(self,q,channel):
        #set channel
        print 'channel:',channel
        fol = os.getcwd()+'/Log/'
        if not os.path.exists(fol):
            os.mkdir(fol)
        file = fol+'Zigbeelog'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.txt'
        with open(file,'w') as f:
            print file
            while True:
                buffer=''
                try:
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

                            data_flag=1
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
    cmd = DisTestFunction(t,whitelist).gen_cmd_for_distest()
    '''
    t = serial.Serial(0,38400)
    t2 = threading.Thread(target=DisTestFunction(t,whitelist).login_test,args=(q,))

    t1 = threading.Thread(target=DisTestFunction(t,whitelist).com_read,args=(q,'17',))
    t1.start()
    t2.start()
    '''