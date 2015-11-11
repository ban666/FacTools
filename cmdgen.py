#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

import sys,os,time

class CmdGenerate:
    def __init__(self,list1):
        self.list1=list1
        self.errdict={
        "02":self.CmdGen_Dg,
        "04":self.CmdGen_Dg,
        '11':self.CmdGen_Bjq,
        '14':self.CmdGen_Sk,
        '15':self.CmdGen_Dk,
        '16':self.CmdGen_Tk,
        '17':self.CmdGen_Zncl,
        '18':self.CmdGen_Zncl
        }
        self.statusdict={
        "02":[28,16,22,'f10200'],
        "04":[28,16,22,'f10200'],
        "11":[32,16,22,'f10400'],
        '14':[26,16,24,'f10100'],
        '15':[28,16,24,'f1020000'],
        '16':[30,16,26,'f103000000'],
        '17':[30,16,26,'f103000000'],
        '18':[30,16,26,'f103000000']
        }
        self.cmddict={
        "02":{1:['000002010f','00000000'],2:['000002010f','00000000'],3:['000002010f','00000000']},
        "04":{1:['000002010f','00000000'],2:['000002010f','00000000'],3:['000002010f','00000000']},
        "11":{1:['0000010101','0000010100'],2:['0000010101','0000010100'],3:['0000010101','0000010100']},
        '14':{1:['000001020101','000001020100'],2:['000001020101','000001020100'],3:['000001020101','000001020100']},
        '15':{1:['000001020101','000001020201','000001020100','000001020200'],2:['000001020F00','000001020000'],3:['000001020101','000001020201','000001020200','000001020100']},
        '16':{1:['000001020101','000001020201','000001020301','000001020100','000001020200','000001020300'],2:['000001020F00','000001020000'],3:['000001020101','000001020201','000001020301','000001020300','000001020200','000001020100']}
        }

    def CheckSum(self,data,jz=16):
        sum=0
        for i in range(0,len(data),2):
            sum+=int(data[i:i+2],jz)
        result='{:004x}'.format(sum)
        return result

    def CmdGen_Sk(self,id):
        cmd_list=['000001020101','000001020100','000001020F00','000001020000']
        status_list=['f10101','f10100','f10101','f10100']
        #kg_list=['一开','二开','三开','一关','二关','三关','全开','全关']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGen_Dk(self,id):
        cmd_list=['000001020101','000001020201','000001020100','000001020200','000001020F00','000001020000']
        status_list=['f1020100','f1020101','f1020001','f1020000','f1020101','f1020000']
        #kg_list=['一开','二开','三开','一关','二关','三关','全开','全关']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGen_Tk(self,id):
        cmd_list=['000001020101','000001020201','000001020301','000001020100','000001020200','000001020300','000001020F00','000001020000']
        status_list=['f103010000','f103010100','f103010101','f103000101','f103000001','f103000000','f103010101','f103000000']
        #kg_list=['一开','二开','三开','一关','二关','三关','全开','全关']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGen_Dg(self,id):
        cmd_list=['000002010f','00000000','00000100']
        status_list = ['f102010f','f102000f','f102010f']
        for i in range(1,16):
            appendstr=''.join(['000002010','{:x}'.format(i)])
            status_appendstr = ''.join(['f102010','{:x}'.format(i)])
            #kgappendstr=''.join(['调光级别',str(i)])
            cmd_list.append(appendstr)
            status_list.append(status_appendstr)
            #kg_list.append(kgappendstr)
        cmd_list.append('00000000')
        status_list.append('f102000f')
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list



    def CmdGen_Bjq(self,id):
        cmd_list=['0000010101','0000010100']
        #kg_list=['开','关']
        status_list=['f10101','f10100']

        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGen_Hwqmsj(self,id):
        cmd_list=['0000010101','0000000100']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list

    def CmdGen_Zncl(self,id):
        cmd_list=['000001020100','000001020300','000001020200']
        status_list = ['f103010000','f103000001','f103000100']
		#kg_list=['开','暂停','关']

        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGenForDisTest(self,gen_type):
        ret_list=[]
        content = self.list1
        for i in content:
            con=i.split(',')
            type=con[1].strip('\n')
            id=con[0]
            print id,type
            if self.cmddict.has_key(type):
                cmd_list=self.cmddict[type][gen_type]
                cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
                cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
                open_list = cmd_list[:len(cmd_list)/2]
                close_list = cmd_list[len(cmd_list)/2:]
                ret_list.append([open_list,close_list])
        return ret_list
    '''
    def CmdGenForDisTest(self,gen_type):
        content = self.list1
        tlist=[]
        if gen_type==1:
            for i in content:
                con=i.split(',')
                type=con[1].strip('\n')
                id=con[0]
                print id,type
                if self.errdict.has_key(type):
                      ret,st=self.errdict[type](id)
                      ret
                      tlist.append(ret[-2:])

        return tlist
    '''
    def CmdGenForOldTest(self):
        content = self.list1
        tlist=[]
        for i in content:
            con=i.split(',')
            type=con[1].strip('\n')
            id=con[0]
            print id,type
            if self.errdict.has_key(type):
                  ret,st=self.errdict[type](id)
                  for j in ret:
                          tlist.append(j)

        return tlist

    def CmdGen(self):
        content=self.list1
        tlist=[]
        rlist=[]
        for i in content:
            con=i.split(',')
            type=con[1].strip('\n')
            id=con[0]

            if self.errdict.has_key(type):
                  ret,st=self.errdict[type](id)
                  #print ret
                  rlist.append(st)
                  for j in ret:
                          tlist.append(j)

        result = [tlist,rlist]
        return result

if __name__ == '__main__':
    lista = ['0001,04']
    listb = ['0003,16']
    a =CmdGenerate(lista)
    b= a.CmdGen()
    c=CmdGenerate(listb)
    d= c.CmdGen()
    print len(b),len(d)
    for i in b:
        for j in i:
            print j