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



flislist=fileGen()
macfile,wfile,channel=flislist[0],flislist[1],flislist[2]
file=wfile

class Dt:
    def __init__(self,t):
        self.timeout = 60
        self.defaultid = '77'
        self.t = t
        self.iddict ={}
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

    def get_mac(self):
        info = '请扫描条码：'.decode('utf-8').encode('gbk')
        content = raw_input(info)
        return content

    def check_content(self,content):
        if len(content)!=18 or not self.devicedict.has_key(content[-2:]):
            print '条形码错误，请检查！'.decode('utf-8').encode('gbk')
            return False
        else:
            print '设备mac: %s 设备类型: %s'.decode('utf-8').encode('gbk') % (content[:16],self.devicedict[content[-2:]].decode('utf-8').encode('gbk'))
            return True

    def clear_q(self,q):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass

    def set_whitelist(self,content,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass
        tstr = content[:16]+self.defaultid
        p.put(tstr)
        #print 'put:',tstr

    def checkonline(self,content,q):
        s_time = time.time()
        t_info = content[:16]+'00'+self.defaultid
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = q.get(timeout=0.01)
            except:
                pass
            if t_data[20:40] == t_info:
                print '入网时间为: %s'.decode('utf-8').encode('gbk') % str(time_range)
                print '入网测试结果：PASS'.decode('utf-8').encode('gbk')
                return True
            if int(float(time_range)) == self.timeout:
                print '设备在规定时间内未能入网'.decode('utf-8').encode('gbk')
                print '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                return False
            time.sleep(0.01)

    def login_test(self,content,q,p):
        print '入网测试启动...'.decode('utf-8').encode('gbk')
        self.set_whitelist(content,p)
        result = self.checkonline(content,q)
        return result

    def status_test(self):
        print '状态上传测试启动...'.decode('utf-8').encode('gbk')
        pass

    def control_test(self,content,q,p):
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
            self.clear_q(q)
            self.t.write(cmdlist[i])
            s_time = time.time()
            while True:
                time_range = time.time()-s_time
                try:
                    t_data = q.get(timeout=0.01)
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

    #Diffrent test for diffrent device
    def test(self,content,q,p):
        device_type = content[16:]
        test_way = self.testdict[device_type]
        for i in test_way:
            result = i(content,q,p)
            if result != True:
                return False
        return True



    def device_test(self,q,p):
        while True:
            content = self.get_mac()
            c_flag = self.check_content(content)
            if c_flag != True:
                continue
            if raw_input('是否启动测试:'.decode('utf-8').encode('gbk')) != 'y':
                print '本轮测试取消'.decode('utf-8').encode('gbk')
                continue
            if self.login_test(content,q,p) != True:
                continue
            if self.test(content,q,p) != True:
                continue


    def com_read(self,q,p):
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

                time.sleep(0.05)
if __name__ == '__main__':
    q = Queue()
    p = Queue()
    t = serial.Serial(0,38400)
    t2 = threading.Thread(target=Dt(t).device_test,args=(q,p,))
    t2.start()
    t1 = threading.Thread(target=Dt(t).com_read,args=(q,p,))
    t1.start()
