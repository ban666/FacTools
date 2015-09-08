# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*"]

options = {"py2exe":  
            {"compressed": 1, #压缩  
             "optimize": 2,  
             "ascii": 1,  
             "includes":includes,  
             "bundle_files": 1 #所有文件打包成一个exe文件
            }}
setup(
    options=options,  
    zipfile=None,
    #console=[{"script": "HelloPy2exe.py", "icon_resources": [(1, "pc.ico")]}],
    windows=[{"script": "main.py", "icon_resources": [(1, "pc.ico")]}],
    data_files=[("magic",["App_x86.exe",]),],
    version = "2010.11.01.01", 
    description = "this is a py2exe test", 
    name = "HelloGuys.", 
)