#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

import sys,os,time

class CmdGenerate:
    def __init__(self,list1):
        self.list1=list1
        self.errdict={
        "04":self.CmdGen_Dg,
        '11':self.CmdGen_Bjq,
        '14':self.CmdGen_Dk,
        '15':self.CmdGen_Kaiguan,
        '16':self.CmdGen_Kaiguan,
        '17':self.CmdGen_Zncl,
        '18':self.CmdGen_Zncl
        }
        self.statusdict={
        "04":[28,16,22,'f10200'],
        "11":[32,16,22,'f10400'],
        '14':[26,16,24,'f10100'],
        '15':[28,16,24,'f1020000'],
        '16':[30,26,36,'f103000000'],
        '17':[30,16,26,'f103000000'],
        '18':[30,16,26,'f103000000']
        }

    def CheckSum(self,data,jz=16):
        sum=0
        for i in range(0,len(data),2):
            sum+=int(data[i:i+2],jz)
        result='{:004x}'.format(sum)
        return result

    def CmdGen_Dk(self,id):
        cmd_list=['000001020101','000001020100','000001020F00','000001020000']
        status_list=['f10101','f10100','f10101','f10100']
        #kg_list=['一开','二开','三开','一关','二关','三关','全开','全关']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list,status_list

    def CmdGen_Kaiguan(self,id):
        cmd_list=['000001020101','000001020201','000001020301','000001020100','000001020200','000001020300','000001020F00','000001020000']
        status_list=['']
        #kg_list=['一开','二开','三开','一关','二关','三关','全开','全关']
        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list

    def CmdGen_Dg(self,id):
        cmd_list=['00000100','00000000','00000100']
        status_list = ['F102010F','F102000F','F102010F']
        for i in range(1,16):
            appendstr=''.join(['000002010','{:x}'.format(i)])
            status_appendstr = ''.join(['F104010','{:x}'.format(i)])
            #kgappendstr=''.join(['调光级别',str(i)])
            cmd_list.append(appendstr)
            status_list.append(status_appendstr)
            #kg_list.append(kgappendstr)
        cmd_list.append('00000100')
        status_list.append('F1040007')
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
        cmd_list=['000001020100','000001020200','000001020300']
		#kg_list=['开','暂停','关']

        cmd_list=[''.join(['0000',id,x]) for x in cmd_list]
        cmd_list=[''.join(['f8e6',x,self.CheckSum(x)]) for x in cmd_list]
        return cmd_list

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

