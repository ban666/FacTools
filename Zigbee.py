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
__author__ = 'ban'

class Zigbee(QThread):
    def __init__(self,t,q,p,parent=None):
        super(Zigbee,self).__init__(parent)
        self.t = t
        self.q = q
        self.p = p
        self.iddict ={}
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

    def run(self):
        #set channel
        channel = '15'
        fol = os.getcwd()+'/Log/'
        if not os.path.exists(fol):
            os.mkdir(fol)
        file = fol+'Zigbeelog'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.txt'
        with open(file,'w') as f:
            while True:
                buffer=''
                rlength=self.t.inWaiting()
                if rlength>=12:
                    buffer+=self.t.read(rlength).encode('hex')
                while len(buffer) >= 24:
                    if (buffer[0:4] == 'f8e6'):
                        #init
                        if buffer=='f8e6000000000000a10000a1':
                            self.t.write(self.setZigbee(channel=channel).decode('hex'))

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

                        self.q.put(cdata)
                        iddict_new=''
                        try:
                            iddict_new = self.p.get(timeout=0.01)
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

                time.sleep(0.05)