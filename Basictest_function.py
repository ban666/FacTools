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


class Dt(QThread):
    textOut = pyqtSignal(str)
    terminalOut = pyqtSignal(str)
    writeExcel = pyqtSignal(dict)
    def __init__(self,t,parent=None):
        super(Dt,self).__init__(parent)
        self.content = ''
        self.timeout = 30
        self.channel = '15'
        self.defaultid = '77'
        self.t = t
        self.iddict={}
        self.resultdict={'login':'','status':'','control':'','result':'','starttime':'','endtime':''}
        '''
        self.q = q
        self.p = p
        '''
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

        self.testdict = {
            '01':[self.login_test],
            '04':[self.login_test,self.status_test,self.control_test],
            '03':[self.login_test,self.status_test],
            '06':[self.login_test],
            '0d':[self.login_test,self.status_test],
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
            '03':[32,16,22],
            "04":[28,16,24],
            '0c':[32,16,22],
            '0d':[32,16,22],
            '0e':[76,40,44],
            "11":[26,16,22],
            '14':[26,16,22],
            '15':[28,16,24],
            '16':[30,26,36],
            '17':[30,16,26],
            '18':[30,16,26]
        }

        self.status_testdict={
            '03':[['F10201','F10400'],['请打开门磁','请关闭门磁']],
            "04":[['F102010F','F102000F','F102010F','F1020101'],['请打开调光器','请关闭调光器','请将调光器调到最亮','请将调光器调到最暗']], #调光状态位存疑
            '0c':[['F10401','F10400'],['请触发人体红外报警器','请等待人体红外报警器关闭']],
            '0d':[['F10401','F10400','F10402','F10400'],['请触发烟雾报警','请等待烟雾报警结束','请触发拆除报警','请等待拆除报警结束']],
            '0e':[['0001','0000','0100','0000'],['请触发可燃气体报警','请等待可燃气体报警结束','请触发拆除报警','请等待拆除报警结束']],
            '14':[['F10101','F10100'],['请打开1孔','请关闭1孔']],
            '15':[['F1020100','F1020101','F1020001','F1020000'],['请打开1孔','请打开2孔','请关闭1孔','请关闭2孔']],
            '16':[['F103010000','F103010100','F103010101','F103000101','F103000001','F103000000'],['请打开1孔','请打开2孔','请打开3孔','请关闭1孔','请关闭2孔','请关闭3孔']],
            '17':[['F103010000','F103000100','F103000001'],['请点击打开按钮','请点击暂停按钮','请点击关闭按钮']],
            '18':[['F103010000','F103000100','F103000001'],['请点击打开按钮','请点击暂停按钮','请点击关闭按钮']]
        }
    def set_content(self,content):
        self.content = content

    def emit_data(self,text):
        self.textOut.emit(text)

    def check_content(self):
        if len(self.content)!=18 or not self.devicedict.has_key(self.content[-2:]):
            print '条形码错误，请检查！'.decode('utf-8').encode('gbk')
            return False
        else:
            print '设备mac: %s 设备类型: %s'.decode('utf-8').encode('gbk') % (self.content[:16],self.devicedict[self.content[-2:]].decode('utf-8').encode('gbk'))
            return True

    def clear_q(self,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass

    def clear_whitelist(self,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass
        p.put('null')

    def set_whitelist(self,p):
        while not p.empty():
            try:
                p.get(timeout=0.01)
            except:
                pass
        tstr = self.content[:16]+self.defaultid
        p.put(tstr)
        #print 'put:',tstr

    def check_online(self,q,p):
        s_time = time.time()
        t_info = self.content[:16]+'00'+self.defaultid
        t_data=''
        while True:
            time_range = '{:.2f}'.format(time.time()-s_time)
            try:
                t_data = q.get(timeout=0.01)
            except:
                pass
            if t_data[20:40] == t_info:
                '''
                print '入网时间为: %s'.decode('utf-8').encode('gbk') % str(time_range)
                print '入网测试结果：PASS'.decode('utf-8').encode('gbk')
                '''
                emit_text = u'入网时间为:'+str(time_range)+u', 入网测试结果：PASS'
                self.emit_data(emit_text)
                self.resultdict['login'] = 'OK'
                return True
            if int(float(time_range)) == self.timeout:
                '''
                print '设备在规定时间内未能入网'.decode('utf-8').encode('gbk')
                print '入网测试结果：FAIL'.decode('utf-8').encode('gbk')
                '''
                emit_text = u'设备在规定时间内未能入网,'+u'入网测试结果：FAIL'
                self.emit_data(emit_text)
                self.resultdict['login'] = 'Fail'
                return False
            time.sleep(0.01)

    def login_test(self,q,p):
        emit_text = u'入网测试启动，请将设备上电...'
        self.emit_data(emit_text)
        self.set_whitelist(p)
        result = self.check_online(q,p)
        self.clear_q(p)
        self.iddict={}
        return result

    def status_test(self,q,p):
        '''
        print '状态上传测试启动...'.decode('utf-8').encode('gbk')
        pass
        '''
        emit_text = u'状态上传测试启动，请根据提示进行对应操作...'
        self.emit_data(emit_text)
        result = 0
        type = str(self.content[16:])
        tlen = self.statusdict[type][0]
        sid  = self.statusdict[type][1]
        did  = self.statusdict[type][2]
        status_list = self.status_testdict[type][0]
        msg_list = self.status_testdict[type][1]
        for i in range(len(status_list)):
            self.clear_q(q)
            s_time = time.time()
            self.emit_data(msg_list[i].decode('utf-8'))
            while True:
                t_data = ''
                time_range = time.time()-s_time
                try:
                    t_data = q.get(timeout=0.01)
                    print t_data
                except:
                    pass
                if len(t_data)!=0:
                    print len(t_data) , tlen ,t_data[sid:did] , status_list[i]
                if len(t_data) == tlen and t_data[sid:did] == status_list[i].lower():
                    result = 1
                    emit_text = u'通过！'
                    self.emit_data(emit_text)
                    break
                if int(float(time_range)) == self.timeout:
                    '''
                    print '设备在规定时间内未收到控制响应信息'.decode('utf-8').encode('gbk')
                    print '控制测试结果：FAIL'.decode('utf-8').encode('gbk')
                    '''
                    emit_text = u'设备在规定时间内未收到状态信息,状态上传测试结果：FAIL'
                    self.emit_data(emit_text)
                    self.resultdict['status'] = 'Fail'
                    return False

                time.sleep(0.01)
        if result == 1:
            '''
            print '设备控制测试通过'.decode('utf-8').encode('gbk')
            print '控制测试结果：Pass'.decode('utf-8').encode('gbk')
            '''
            emit_text = u'设备状态上传测试通过,状态上传测试结果：PASS'
            self.emit_data(emit_text)
            self.resultdict['status'] = 'OK'
            return True
        else:
            emit_text = u'设备状态上传测试未通过,状态上传测试结果：BLOCK'
            self.emit_data(emit_text)
            self.resultdict['status'] = 'BLOCK'
            return False

    def control_test(self,q,p):
        '''
        print '控制测试启动...'.decode('utf-8').encode('gbk')
        '''
        emit_text = u'控制测试启动...'
        self.emit_data(emit_text)
        result = 0
        type = str(self.content[16:])
        tlen = self.statusdict[type][0]
        sid  = self.statusdict[type][1]
        did  = self.statusdict[type][2]
        id_type = '00'+self.defaultid+','+type
        tlist = [id_type]
        cmdlist,statuslist = cmdgen.CmdGenerate(tlist).CmdGen()
        cmdlist=[x.decode('hex') for x in cmdlist]
        statuslist = statuslist[0]
        for i in range(len(cmdlist)):
            self.clear_q(q)
            self.t.write(cmdlist[i])
            s_time = time.time()
            while True:
                t_data = ''
                time_range = time.time()-s_time
                try:
                    t_data = q.get(timeout=0.01)
                    print t_data
                except:
                    pass
                #print len(t_data) , tlen ,t_data[sid:did] , statuslist[i]
                if len(t_data) == tlen and t_data[sid:did] == statuslist[i]:
                    result = 1
                    break
                if int(float(time_range)) == self.timeout:
                    '''
                    print '设备在规定时间内未收到控制响应信息'.decode('utf-8').encode('gbk')
                    print '控制测试结果：FAIL'.decode('utf-8').encode('gbk')
                    '''
                    emit_text = u'设备在规定时间内未收到控制响应信息,控制测试结果：FAIL'
                    self.emit_data(emit_text)
                    self.resultdict['control'] = 'Fail'
                    return False

                time.sleep(0.01)
        if result == 1:
            '''
            print '设备控制测试通过'.decode('utf-8').encode('gbk')
            print '控制测试结果：Pass'.decode('utf-8').encode('gbk')
            '''
            emit_text = u'设备控制测试通过,控制测试结果：PASS'
            self.emit_data(emit_text)
            self.resultdict['control'] = 'OK'
            return True
        else:
            emit_text = u'设备控制测试未通过,控制测试结果：BLOCK'
            self.emit_data(emit_text)
            self.resultdict['control'] = 'BLOCK'
            return False

    #Diffrent test for diffrent device
    def test(self,q,p):
        device_type = self.content[16:]
        test_way = self.testdict[device_type]
        for i in test_way:
            result = i(self.content,q,p)
            if result != True:
                return False
        return True

    def judge_result(self,final_result,p):
        emit_text = u'测试结束，请将设备断电！'
        self.emit_data(emit_text)
        if final_result == True:
            emit_text = u'设备mac:'+self.content[:16]+u' 设备类型:'+ self.devicedict[str(self.content[-2:])].decode('utf-8') +u' 的设备测试通过！'
            self.resultdict['result'] = 'OK'
        elif final_result == False:
            emit_text = u'设备mac:'+self.content[:16]+u' 设备类型:'+ self.devicedict[str(self.content[-2:])].decode('utf-8') +u' 的设备测试失败！'
            self.resultdict['result'] = 'Fail'

        else:
            emit_text = u'测试结果异常！'
            self.resultdict['result'] = 'Block'
        self.clear_whitelist(p)
        self.emit_data(emit_text)
        self.resultdict['endtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.writeExcel.emit(self.resultdict)
        print self.resultdict
        self.terminalOut.emit('test')


    def device_test(self,q,p):
        test_list = self.testdict[str(self.content[-2:])]
        result = ''
        self.resultdict['starttime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for i in test_list:
            result = i(q,p)
            if result != True:
                self.judge_result(result,p)
                return False
        self.judge_result(result,p)
        return True

    def com_read(self,q,p,channel):
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
                            iddict_new=''
                            try:
                                iddict_new = p.get(timeout=0.01)
                            except:
                                pass
                            if iddict_new !='':
                                #print 'get',iddict_new
                                self.iddict = {str(iddict_new[:16]):str(iddict_new[16:])}
                            if iddict_new == 'null':
                                self.iddict = {}
                            #print self.iddict
                            #id mac generate
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



if __name__ == '__main__':
    q = Queue()
    p = Queue()
    t = serial.Serial(0,38400)
    t2 = threading.Thread(target=Dt(t).device_test,args=(q,p,))
    t2.start()
    t1 = threading.Thread(target=Dt(t).com_read,args=(q,p,))
    t1.start()
